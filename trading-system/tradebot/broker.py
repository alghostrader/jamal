"""Order execution and portfolio state.

PaperBroker simulates fills on live prices (fees + slippage included) so the
paper account behaves like a pessimistic real one. LiveBroker sends real
market orders through ccxt but reuses all of PaperBroker's accounting.
"""

import csv
import os
from dataclasses import dataclass

import ccxt


@dataclass
class Position:
    symbol: str
    qty: float
    entry_price: float
    cost: float                # cash spent including fees
    stop: float
    take_profit: float
    reason: str
    opened_at: object


class PaperBroker:
    def __init__(self, cfg, log_dir=None):
        self.balance = float(cfg.starting_balance)
        self.fee_bps = cfg.fees.taker_bps
        self.slip_bps = cfg.fees.slippage_bps
        self.positions = {}
        self.closed_trades = []
        self._log_path = None
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            self._log_path = os.path.join(log_dir, "trades.csv")
            if not os.path.exists(self._log_path):
                with open(self._log_path, "w", newline="") as f:
                    csv.writer(f).writerow(
                        ["time", "symbol", "side", "qty", "price", "fee", "pnl", "reason", "balance"]
                    )

    # -- fills ---------------------------------------------------------------

    def _fill_buy(self, symbol, qty, price):
        fill = price * (1 + self.slip_bps / 1e4)
        return qty, fill

    def _fill_sell(self, symbol, qty, price):
        fill = price * (1 - self.slip_bps / 1e4)
        return qty, fill

    # -- API -----------------------------------------------------------------

    def buy(self, symbol, qty, price, stop, take_profit, reason, ts):
        if qty <= 0 or symbol in self.positions:
            return None
        qty, fill = self._fill_buy(symbol, qty, price)
        notional = qty * fill
        fee = notional * self.fee_bps / 1e4
        if notional + fee > self.balance:
            qty = self.balance / (fill * (1 + self.fee_bps / 1e4)) * 0.999
            notional = qty * fill
            fee = notional * self.fee_bps / 1e4
            if qty <= 0:
                return None
        self.balance -= notional + fee
        pos = Position(symbol, qty, fill, notional + fee, stop, take_profit, reason, ts)
        self.positions[symbol] = pos
        self._log(ts, symbol, "BUY", qty, fill, fee, "", reason)
        return pos

    def close(self, symbol, price, reason, ts):
        pos = self.positions.pop(symbol, None)
        if pos is None:
            return None
        qty, fill = self._fill_sell(symbol, pos.qty, price)
        proceeds = qty * fill
        fee = proceeds * self.fee_bps / 1e4
        self.balance += proceeds - fee
        pnl = proceeds - fee - pos.cost
        self.closed_trades.append(
            {
                "symbol": symbol,
                "entry": pos.entry_price,
                "exit": fill,
                "qty": qty,
                "pnl": pnl,
                "reason": reason,
                "opened_at": pos.opened_at,
                "closed_at": ts,
                "signal": pos.reason,
            }
        )
        self._log(ts, symbol, "SELL", qty, fill, fee, f"{pnl:.2f}", reason)
        return pnl

    def equity(self, prices):
        return self.balance + sum(
            p.qty * prices.get(s, p.entry_price) for s, p in self.positions.items()
        )

    def reconcile(self, symbol, ts):
        """Hook for brokers whose positions can close server-side (MT5)."""
        return None

    def _log(self, ts, symbol, side, qty, price, fee, pnl, reason):
        if self._log_path:
            with open(self._log_path, "a", newline="") as f:
                csv.writer(f).writerow(
                    [ts, symbol, side, f"{qty:.8f}", f"{price:.2f}", f"{fee:.4f}", pnl, reason, f"{self.balance:.2f}"]
                )


class LiveBroker(PaperBroker):
    """Same accounting as PaperBroker, but fills come from real market orders.

    Stops and take-profits are 'soft': the engine closes positions with market
    orders when levels are crossed, so the bot must stay running. If that is
    not acceptable, place exchange-side OCO orders manually.
    """

    def __init__(self, cfg, log_dir=None):
        super().__init__(cfg, log_dir)
        exchange_cls = getattr(ccxt, cfg.exchange)
        self.x = exchange_cls(
            {
                "apiKey": os.getenv("EXCHANGE_API_KEY"),
                "secret": os.getenv("EXCHANGE_API_SECRET"),
                "enableRateLimit": True,
            }
        )
        self.x.load_markets()
        quote = cfg.symbols[0].split("/")[1]
        self.balance = float(self.x.fetch_balance()["free"].get(quote, 0.0))
        print(f"[live] connected to {cfg.exchange}, free {quote}: {self.balance:.2f}")

    def _order(self, side, symbol, qty, fallback_price):
        qty = float(self.x.amount_to_precision(symbol, qty))
        order = self.x.create_order(symbol, "market", side, qty)
        order = self.x.fetch_order(order["id"], symbol)
        fill = order.get("average") or fallback_price
        filled = order.get("filled") or qty
        return filled, fill

    def _fill_buy(self, symbol, qty, price):
        return self._order("buy", symbol, qty, price)

    def _fill_sell(self, symbol, qty, price):
        return self._order("sell", symbol, qty, price)


def make_broker(cfg, log_dir=None):
    if cfg.mode == "live":
        if cfg.get("platform", "ccxt") == "mt5":
            from .mt5_adapter import MT5Broker
            return MT5Broker(cfg, log_dir)
        return LiveBroker(cfg, log_dir)
    return PaperBroker(cfg, log_dir)
