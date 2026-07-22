"""Live/paper trading loop.

Every cycle: refresh candles for each symbol, enforce stops/take-profits on
open positions at the latest price, and evaluate the strategy once per newly
closed candle. Ctrl+C stops the bot and prints a session summary.
"""

import csv
import os
import time
from datetime import datetime, timezone

from .backtest import summarize
from .broker import make_broker
from .config import timeframe_seconds
from .data import make_data
from .risk import RiskManager
from .strategy import make_strategy


def now_utc():
    return datetime.now(timezone.utc)


class Engine:
    def __init__(self, cfg, data=None):
        self.cfg = cfg
        self.data = data or make_data(cfg)
        self.strategy = make_strategy(cfg)
        self.tf_sec = timeframe_seconds(cfg)
        self.risk = RiskManager(cfg, self.tf_sec)
        log_dir = cfg.logging.dir
        self.broker = make_broker(cfg, log_dir)
        self.equity_log = os.path.join(log_dir, "equity.csv")
        os.makedirs(log_dir, exist_ok=True)
        if not os.path.exists(self.equity_log):
            with open(self.equity_log, "w", newline="") as f:
                csv.writer(f).writerow(["time", "equity", "open_positions"])
        self.last_candle = {}
        self.prices = {}

    def run(self, max_cycles=None):
        cfg = self.cfg
        mode = cfg.mode.upper()
        print(f"[{mode}] {cfg.exchange} {cfg.symbols} {cfg.timeframe} "
              f"strategy={cfg.strategy.name} — Ctrl+C to stop")
        if cfg.mode == "live":
            print("[LIVE] REAL ORDERS WILL BE SENT. Stops are soft — keep the bot running.")

        cycles = 0
        try:
            while max_cycles is None or cycles < max_cycles:
                cycles += 1
                for symbol in cfg.symbols:
                    try:
                        self._step(symbol)
                    except Exception as exc:  # keep the loop alive on feed hiccups
                        print(f"[warn] {symbol}: {type(exc).__name__}: {exc}")
                self._heartbeat(cycles)
                time.sleep(cfg.poll_interval_sec)
        except KeyboardInterrupt:
            print("\nstopping...")
        self._summary()

    def _step(self, symbol):
        df = self.data.candles(symbol, self.cfg.history_candles)
        if len(df) < 2:
            return
        price = float(df["close"].iloc[-1])
        self.prices[symbol] = price
        ts = now_utc()

        pnl = self.broker.reconcile(symbol, ts)
        if pnl is not None:
            self.risk.on_trade_closed(symbol, pnl, ts)

        pos = self.broker.positions.get(symbol)
        if pos is not None:
            if price <= pos.stop:
                pnl = self.broker.close(symbol, price, "stop_loss", ts)
                self.risk.on_trade_closed(symbol, pnl, ts)
                print(f"[{ts:%H:%M:%S}] {symbol} STOP hit @ {price:.2f} pnl {pnl:+.2f}")
            elif price >= pos.take_profit:
                pnl = self.broker.close(symbol, price, "take_profit", ts)
                self.risk.on_trade_closed(symbol, pnl, ts)
                print(f"[{ts:%H:%M:%S}] {symbol} TAKE PROFIT @ {price:.2f} pnl {pnl:+.2f}")

        closed = df.iloc[:-1]  # drop the still-forming candle
        newest = closed["time"].iloc[-1]
        if self.last_candle.get(symbol) == newest:
            return
        self.last_candle[symbol] = newest

        if symbol in self.broker.positions:
            return
        signal = self.strategy.evaluate(closed)
        if signal is None:
            return
        equity = self.broker.equity(self.prices)
        allowed, why = self.risk.can_open(symbol, equity, len(self.broker.positions), ts)
        if not allowed:
            print(f"[{ts:%H:%M:%S}] {symbol} signal {signal.reason} skipped: {why}")
            return
        qty = self.risk.position_size(equity, price, signal.stop)
        pos = self.broker.buy(symbol, qty, price, signal.stop, signal.take_profit,
                              signal.reason, ts)
        if pos is not None:
            print(f"[{ts:%H:%M:%S}] {symbol} BUY {pos.qty:.6f} @ {pos.entry_price:.2f} "
                  f"({signal.reason}) stop {pos.stop:.2f} tp {pos.take_profit:.2f}")

    def _heartbeat(self, cycles):
        if cycles % 20 != 1:
            return
        ts = now_utc()
        equity = self.broker.equity(self.prices)
        with open(self.equity_log, "a", newline="") as f:
            csv.writer(f).writerow([ts.isoformat(), f"{equity:.2f}", len(self.broker.positions)])
        print(f"[{ts:%H:%M:%S}] equity {equity:.2f} | open {list(self.broker.positions)} "
              f"| closed trades {len(self.broker.closed_trades)}")

    def _summary(self):
        for symbol in list(self.broker.positions):
            price = self.prices.get(symbol)
            if price:
                self.broker.close(symbol, price, "session_end", now_utc())
        equity = self.broker.equity(self.prices)
        stats = summarize(self.cfg, self.broker.closed_trades,
                          [float(self.cfg.starting_balance), equity], self.tf_sec)
        print("\n=== Session summary ===")
        for key, value in stats.items():
            if key not in ("max_drawdown_pct", "sharpe"):  # meaningless on 2 points
                print(f"  {key:26s} {value}")
