"""Signal strategies.

Every strategy exposes ``evaluate(df) -> Signal | None`` where ``df`` is a
DataFrame of *closed* candles (columns: time, open, high, low, close, volume).
The engine and the backtester call the exact same code, so backtest behaviour
matches live behaviour candle for candle.

All strategies are long-only: spot accounts cannot short.
"""

from dataclasses import dataclass

import numpy as np

from . import indicators as ta


@dataclass
class Signal:
    side: str          # only 'buy' for now (long entry)
    reason: str
    stop: float
    take_profit: float


class MomentumBreakout:
    """Buy breakouts above the recent high, confirmed by volume, in an uptrend."""

    def __init__(self, p):
        self.p = p
        self.warmup = max(p.ema_slow, p.breakout_lookback, p.atr_period, 20) + 10

    def evaluate(self, df):
        p = self.p
        if len(df) < self.warmup:
            return None
        close = df["close"]
        last_close = close.iloc[-1]
        atr_now = ta.atr(df, p.atr_period).iloc[-1]
        if not np.isfinite(atr_now) or atr_now <= 0:
            return None
        if ta.ema(close, p.ema_fast).iloc[-1] <= ta.ema(close, p.ema_slow).iloc[-1]:
            return None
        breakout_high = df["high"].iloc[-p.breakout_lookback - 1 : -1].max()
        vol_avg = df["volume"].rolling(20).mean().iloc[-1]
        if last_close > breakout_high and df["volume"].iloc[-1] > p.volume_mult * vol_avg:
            stop = last_close - p.stop_atr_mult * atr_now
            take_profit = last_close + p.take_profit_r * (last_close - stop)
            return Signal("buy", "momentum_breakout", stop, take_profit)
        return None


class MeanReversion:
    """Buy oversold dips below the lower Bollinger band, target the middle band."""

    def __init__(self, p):
        self.p = p
        self.warmup = max(p.bb_period, p.rsi_period, p.atr_period) + 10

    def evaluate(self, df):
        p = self.p
        if len(df) < self.warmup:
            return None
        close = df["close"]
        last_close = close.iloc[-1]
        atr_now = ta.atr(df, p.atr_period).iloc[-1]
        if not np.isfinite(atr_now) or atr_now <= 0:
            return None
        mid, _, lower = ta.bollinger(close, p.bb_period, p.bb_std)
        rsi_now = ta.rsi(close, p.rsi_period).iloc[-1]
        if last_close < lower.iloc[-1] and rsi_now < p.rsi_oversold:
            stop = last_close - p.stop_atr_mult * atr_now
            take_profit = mid.iloc[-1]
            if take_profit > last_close:
                return Signal("buy", "mean_reversion", stop, take_profit)
        return None


class RegimeCombo:
    """Route to breakout logic in trending markets, band fades in ranging ones.

    Trend strength is |ema_fast - ema_slow| normalised by ATR: above the
    threshold the market is treated as trending.
    """

    def __init__(self, p):
        self.p = p
        self.momentum = MomentumBreakout(p)
        self.reversion = MeanReversion(p)
        self.warmup = max(self.momentum.warmup, self.reversion.warmup)

    def evaluate(self, df):
        p = self.p
        if len(df) < self.warmup:
            return None
        close = df["close"]
        atr_now = ta.atr(df, p.atr_period).iloc[-1]
        if not np.isfinite(atr_now) or atr_now <= 0:
            return None
        spread = ta.ema(close, p.ema_fast).iloc[-1] - ta.ema(close, p.ema_slow).iloc[-1]
        trending = abs(spread) / atr_now >= p.trend_threshold
        if trending:
            return self.momentum.evaluate(df) if spread > 0 else None
        return self.reversion.evaluate(df)


STRATEGIES = {
    "regime_combo": RegimeCombo,
    "momentum_breakout": MomentumBreakout,
    "mean_reversion": MeanReversion,
}


def make_strategy(cfg):
    p = cfg.strategy
    # risk params are needed for stop/target placement
    p = type(p)({**p, "stop_atr_mult": cfg.risk.stop_atr_mult, "take_profit_r": cfg.risk.take_profit_r})
    try:
        return STRATEGIES[p.name](p)
    except KeyError:
        raise SystemExit(f"config error: unknown strategy {p.name!r}, pick from {list(STRATEGIES)}")
