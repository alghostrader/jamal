"""Synthetic OHLCV generator for offline pipeline tests.

Regime-switching random walk: alternating quiet/volatile and flat/trending
periods so both strategy branches get exercised. This is for *testing the
plumbing* — synthetic backtest results say nothing about real markets.
"""

import numpy as np
import pandas as pd


def synthetic_ohlcv(n=20000, start_price=75000.0, timeframe_sec=300, seed=7,
                    start="2025-01-01"):
    rng = np.random.default_rng(seed)
    base_vol = 0.0008

    vol_state, trend_state = 0, 0
    drift = 0.0
    opens = np.empty(n)
    highs = np.empty(n)
    lows = np.empty(n)
    closes = np.empty(n)
    volumes = np.empty(n)
    price = start_price

    for i in range(n):
        if rng.random() < 0.002:
            vol_state = 1 - vol_state
        if rng.random() < 0.003:
            trend_state = rng.integers(-1, 2)
            drift = trend_state * rng.uniform(0.00005, 0.0003)
        vol = base_vol * (3.0 if vol_state else 1.0)

        steps = np.exp(rng.normal(drift / 4, vol / 2, 4)).cumprod() * price
        o, c = price, steps[-1]
        opens[i] = o
        closes[i] = c
        highs[i] = max(o, steps.max())
        lows[i] = min(o, steps.min())
        move = abs(np.log(c / o))
        volumes[i] = rng.gamma(2.0, 50.0) * (1 + 400 * move)
        price = c

    times = pd.date_range(start, periods=n, freq=f"{timeframe_sec}s", tz="UTC")
    return pd.DataFrame(
        {"time": times, "open": opens, "high": highs, "low": lows,
         "close": closes, "volume": volumes}
    )
