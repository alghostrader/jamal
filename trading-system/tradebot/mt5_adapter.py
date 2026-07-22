"""MetaTrader 5 integration (Windows only).

Connects to a running, logged-in MT5 terminal through the official
MetaTrader5 Python package. Data comes from your broker's feed; in live mode
orders are sent with server-side SL/TP, so positions stay protected even if
the bot or the connection dies.

Sizing note: lot conversion assumes the symbol is quoted in your account
currency (BTCUSD / EURUSD on a USD account). For cross-currency symbols the
risk-per-trade figure will be off by the conversion rate.
"""

import os
from datetime import datetime, timedelta, timezone

import pandas as pd

try:
    import MetaTrader5 as mt5
except ImportError as exc:
    raise SystemExit(
        "platform: mt5 requires the MetaTrader5 package, which only installs on "
        "64-bit Windows Python: pip install MetaTrader5"
    ) from exc

from .broker import PaperBroker, Position

MAGIC = 20260722  # tags this bot's orders so it never touches manual trades

_connected = False


def _connect():
    global _connected
    if _connected:
        return
    args = [os.environ["MT5_TERMINAL_PATH"]] if os.getenv("MT5_TERMINAL_PATH") else []
    kwargs = {}
    if os.getenv("MT5_LOGIN") and os.getenv("MT5_PASSWORD"):
        kwargs = {"login": int(os.environ["MT5_LOGIN"]), "password": os.environ["MT5_PASSWORD"]}
        if os.getenv("MT5_SERVER"):
            kwargs["server"] = os.environ["MT5_SERVER"]
    if not mt5.initialize(*args, **kwargs):
        raise SystemExit(
            f"MT5 initialize failed: {mt5.last_error()} — is the MetaTrader 5 "
            "terminal installed, running, and logged into an account?"
        )
    _connected = True


def _timeframe(tf):
    return {
        "1m": mt5.TIMEFRAME_M1, "3m": mt5.TIMEFRAME_M3, "5m": mt5.TIMEFRAME_M5,
        "15m": mt5.TIMEFRAME_M15, "30m": mt5.TIMEFRAME_M30, "1h": mt5.TIMEFRAME_H1,
        "2h": mt5.TIMEFRAME_H2, "4h": mt5.TIMEFRAME_H4, "1d": mt5.TIMEFRAME_D1,
    }[tf]


def _rates_to_df(rates, what):
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"no rates for {what}: {mt5.last_error()}")
    raw = pd.DataFrame(rates)
    return pd.DataFrame(
        {
            "time": pd.to_datetime(raw["time"], unit="s", utc=True),
            "open": raw["open"], "high": raw["high"],
            "low": raw["low"], "close": raw["close"],
            "volume": raw["tick_volume"].astype(float),
        }
    )


class MT5Data:
    def __init__(self, cfg):
        _connect()
        self.tf = _timeframe(cfg.timeframe)
        for symbol in cfg.symbols:
            if not mt5.symbol_select(symbol, True):
                raise SystemExit(
                    f"symbol {symbol!r} not found at this broker — check the exact "
                    "spelling in the terminal's Market Watch (right-click → Show All)"
                )

    def candles(self, symbol, limit=200):
        return _rates_to_df(mt5.copy_rates_from_pos(symbol, self.tf, 0, limit), symbol)

    def history(self, symbol, days):
        end = datetime.now(timezone.utc)
        return _rates_to_df(
            mt5.copy_rates_range(symbol, self.tf, end - timedelta(days=days), end), symbol
        )


class MT5Broker(PaperBroker):
    """Real orders through the MT5 terminal, SL/TP held server-side."""

    def __init__(self, cfg, log_dir=None):
        super().__init__(cfg, log_dir)
        _connect()
        account = mt5.account_info()
        if account is None:
            raise SystemExit(f"cannot read MT5 account: {mt5.last_error()}")
        self.balance = float(account.balance)
        self.tickets = {}
        print(
            f"[live-mt5] account {account.login} ({account.server}) "
            f"balance {account.balance:.2f} {account.currency}"
        )

    # -- helpers -------------------------------------------------------------

    def _send(self, request):
        result = mt5.order_send(request)
        if result is not None and result.retcode == mt5.TRADE_RETCODE_INVALID_FILL:
            request["type_filling"] = mt5.ORDER_FILLING_FOK
            result = mt5.order_send(request)
        return result

    def _deal_result(self, ticket, fallback_price):
        pnl, exit_price = 0.0, fallback_price
        for deal in mt5.history_deals_get(position=ticket) or []:
            pnl += deal.profit + deal.commission + deal.swap
            if deal.entry == mt5.DEAL_ENTRY_OUT:
                exit_price = deal.price
        return pnl, exit_price

    def _record_close(self, symbol, pos, pnl, exit_price, reason, ts):
        account = mt5.account_info()
        if account is not None:
            self.balance = float(account.balance)
        self.closed_trades.append(
            {
                "symbol": symbol, "entry": pos.entry_price, "exit": exit_price,
                "qty": pos.qty, "pnl": pnl, "reason": reason,
                "opened_at": pos.opened_at, "closed_at": ts, "signal": pos.reason,
            }
        )
        self._log(ts, symbol, "SELL", pos.qty, exit_price, 0.0, f"{pnl:.2f}", reason)

    # -- PaperBroker interface ----------------------------------------------

    def reconcile(self, symbol, ts):
        """Detect positions the server already closed via SL/TP between polls."""
        ticket = self.tickets.get(symbol)
        if ticket is None or mt5.positions_get(ticket=ticket):
            return None
        pos = self.positions.pop(symbol, None)
        self.tickets.pop(symbol, None)
        if pos is None:
            return None
        pnl, exit_price = self._deal_result(ticket, pos.entry_price)
        self._record_close(symbol, pos, pnl, exit_price, "server_sl_tp", ts)
        print(f"[mt5] server closed {symbol} at {exit_price:.2f} (SL/TP) pnl {pnl:+.2f}")
        return pnl

    def buy(self, symbol, qty, price, stop, take_profit, reason, ts):
        if qty <= 0 or symbol in self.positions:
            return None
        info = mt5.symbol_info(symbol)
        if info is None:
            print(f"[mt5] no symbol info for {symbol}")
            return None
        step = info.volume_step or 0.01
        lots = round(round(qty / info.trade_contract_size / step) * step, 8)
        lots = max(info.volume_min, min(info.volume_max, lots))
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lots,
            "type": mt5.ORDER_TYPE_BUY,
            "sl": round(stop, info.digits),
            "tp": round(take_profit, info.digits),
            "deviation": 20,
            "magic": MAGIC,
            "comment": f"tradebot {reason}"[:31],
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = self._send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            print(
                f"[mt5] BUY {symbol} rejected: retcode="
                f"{getattr(result, 'retcode', mt5.last_error())} "
                f"{getattr(result, 'comment', '')}"
            )
            return None
        fill = result.price or price
        filled_qty = result.volume * info.trade_contract_size
        pos = Position(symbol, filled_qty, fill, filled_qty * fill,
                       stop, take_profit, reason, ts)
        self.positions[symbol] = pos
        mine = [p for p in (mt5.positions_get(symbol=symbol) or []) if p.magic == MAGIC]
        self.tickets[symbol] = mine[-1].ticket if mine else result.order
        account = mt5.account_info()
        if account is not None:
            self.balance = float(account.balance)
        self._log(ts, symbol, "BUY", filled_qty, fill, 0.0, "", reason)
        return pos

    def close(self, symbol, price, reason, ts):
        pos = self.positions.get(symbol)
        if pos is None:
            return None
        ticket = self.tickets.get(symbol)
        live = mt5.positions_get(ticket=ticket) if ticket else None
        if not live:
            return self.reconcile(symbol, ts)
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": live[0].volume,
            "type": mt5.ORDER_TYPE_SELL,
            "position": ticket,
            "deviation": 20,
            "magic": MAGIC,
            "comment": f"tradebot {reason}"[:31],
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = self._send(request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            print(
                f"[mt5] close {symbol} FAILED (retcode="
                f"{getattr(result, 'retcode', mt5.last_error())}) — position still "
                "open but protected by server-side SL/TP"
            )
            return None
        self.positions.pop(symbol, None)
        self.tickets.pop(symbol, None)
        pnl, exit_price = self._deal_result(ticket, result.price or price)
        self._record_close(symbol, pos, pnl, exit_price, reason, ts)
        return pnl

    def equity(self, prices):
        account = mt5.account_info()
        return float(account.equity) if account is not None else self.balance
