"""Event-driven backtester.

Runs the same strategy/risk/broker code as the live engine over historical
candles. No lookahead: signals are computed on candles up to i, entries fill
at candle i+1's open, and stops are checked before take-profits when both
fall inside the same candle (pessimistic).
"""

import numpy as np

from .broker import PaperBroker
from .config import timeframe_seconds
from .risk import RiskManager
from .strategy import make_strategy


def run_backtest(cfg, df, symbol):
    strategy = make_strategy(cfg)
    tf_sec = timeframe_seconds(cfg)
    risk = RiskManager(cfg, tf_sec)
    broker = PaperBroker(cfg)

    equity_curve = []
    blocked = 0

    for i in range(strategy.warmup, len(df) - 1):
        nxt = df.iloc[i + 1]
        ts = nxt["time"]
        last_close = df["close"].iloc[i]

        pos = broker.positions.get(symbol)
        if pos is not None:
            if nxt["low"] <= pos.stop:
                pnl = broker.close(symbol, pos.stop, "stop_loss", ts)
                risk.on_trade_closed(symbol, pnl, ts)
            elif nxt["high"] >= pos.take_profit:
                pnl = broker.close(symbol, pos.take_profit, "take_profit", ts)
                risk.on_trade_closed(symbol, pnl, ts)

        equity = broker.equity({symbol: last_close})
        equity_curve.append(equity)

        if symbol not in broker.positions:
            signal = strategy.evaluate(df.iloc[: i + 1])
            if signal is not None:
                allowed, _ = risk.can_open(symbol, equity, len(broker.positions), ts)
                if not allowed:
                    blocked += 1
                    continue
                qty = risk.position_size(equity, nxt["open"], signal.stop)
                broker.buy(symbol, qty, nxt["open"], signal.stop,
                           signal.take_profit, signal.reason, ts)

    if symbol in broker.positions:
        broker.close(symbol, df["close"].iloc[-1], "backtest_end", df["time"].iloc[-1])
    equity_curve.append(broker.equity({}))

    return summarize(cfg, broker.closed_trades, np.asarray(equity_curve), tf_sec, blocked)


def summarize(cfg, trades, equity_curve, tf_sec, blocked=0):
    start = float(cfg.starting_balance)
    end = float(equity_curve[-1]) if len(equity_curve) else start
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]
    gross_win = sum(t["pnl"] for t in wins)
    gross_loss = abs(sum(t["pnl"] for t in losses))

    running_max = np.maximum.accumulate(equity_curve) if len(equity_curve) else np.array([start])
    max_dd = float(((running_max - equity_curve) / running_max).max()) * 100 if len(equity_curve) else 0.0

    rets = np.diff(equity_curve) / equity_curve[:-1] if len(equity_curve) > 2 else np.array([0.0])
    candles_per_year = (365 * 86400) / tf_sec
    sharpe = float(rets.mean() / rets.std() * np.sqrt(candles_per_year)) if rets.std() > 0 else 0.0

    return {
        "trades": len(trades),
        "win_rate_pct": round(100 * len(wins) / len(trades), 1) if trades else 0.0,
        "net_pnl": round(end - start, 2),
        "return_pct": round(100 * (end / start - 1), 2),
        "profit_factor": round(gross_win / gross_loss, 2) if gross_loss > 0 else float("inf"),
        "max_drawdown_pct": round(max_dd, 2),
        "sharpe": round(sharpe, 2),
        "avg_win": round(gross_win / len(wins), 2) if wins else 0.0,
        "avg_loss": round(-gross_loss / len(losses), 2) if losses else 0.0,
        "signals_blocked_by_risk": blocked,
        "end_equity": round(end, 2),
    }


def print_report(symbol, stats):
    print(f"\n=== Backtest report: {symbol} ===")
    for key, value in stats.items():
        print(f"  {key:26s} {value}")
