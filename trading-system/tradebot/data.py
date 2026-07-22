"""Market data: live candles via ccxt, historical pagination, CSV loading."""

import time

import ccxt
import pandas as pd

COLUMNS = ["time", "open", "high", "low", "close", "volume"]


def to_df(rows):
    df = pd.DataFrame(rows, columns=COLUMNS)
    df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
    return df


class MarketData:
    def __init__(self, cfg):
        exchange_cls = getattr(ccxt, cfg.exchange)
        self.x = exchange_cls({"enableRateLimit": True})
        self.timeframe = cfg.timeframe

    def candles(self, symbol, limit=200):
        """Most recent candles; the last row is usually still forming."""
        return to_df(self.x.fetch_ohlcv(symbol, self.timeframe, limit=limit))

    def history(self, symbol, days):
        """Paginated fetch of `days` of history."""
        tf_ms = self.x.parse_timeframe(self.timeframe) * 1000
        since = self.x.milliseconds() - days * 86_400_000
        rows = []
        while True:
            batch = self.x.fetch_ohlcv(symbol, self.timeframe, since=since, limit=1000)
            if not batch:
                break
            rows.extend(batch)
            since = batch[-1][0] + tf_ms
            if len(batch) < 1000 or since > self.x.milliseconds():
                break
            time.sleep(self.x.rateLimit / 1000)
        df = to_df(rows)
        return df.drop_duplicates(subset="time").reset_index(drop=True)


def make_data(cfg):
    """Data feed for the configured platform: ccxt exchange or MetaTrader 5."""
    if cfg.get("platform", "ccxt") == "mt5":
        from .mt5_adapter import MT5Data
        return MT5Data(cfg)
    return MarketData(cfg)


def load_csv(path):
    """Load candles from CSV with columns: time, open, high, low, close, volume."""
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise SystemExit(f"CSV {path} is missing columns: {sorted(missing)}")
    df["time"] = pd.to_datetime(df["time"], utc=True, format="mixed")
    return df[COLUMNS].sort_values("time").reset_index(drop=True)
