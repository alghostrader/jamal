import os

import yaml
from dotenv import load_dotenv

TIMEFRAME_SEC = {
    "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
    "1h": 3600, "2h": 7200, "4h": 14400, "1d": 86400,
}


class Cfg(dict):
    """Dict with attribute access, applied recursively."""

    def __getattr__(self, key):
        try:
            value = self[key]
        except KeyError:
            raise AttributeError(key) from None
        return Cfg(value) if isinstance(value, dict) else value


def load_config(path="config.yaml"):
    load_dotenv()
    with open(path) as f:
        cfg = Cfg(yaml.safe_load(f))

    if cfg.mode not in ("paper", "live"):
        raise SystemExit(f"config error: mode must be 'paper' or 'live', got {cfg.mode!r}")
    if cfg.timeframe not in TIMEFRAME_SEC:
        raise SystemExit(f"config error: unsupported timeframe {cfg.timeframe!r}")

    if cfg.mode == "live":
        if not cfg.get("i_understand_live_trading_risk"):
            raise SystemExit(
                "live mode requires 'i_understand_live_trading_risk: true' in config.yaml.\n"
                "Read the README's live trading section first."
            )
        if not os.getenv("EXCHANGE_API_KEY") or not os.getenv("EXCHANGE_API_SECRET"):
            raise SystemExit("live mode requires EXCHANGE_API_KEY and EXCHANGE_API_SECRET in .env")

    return cfg


def timeframe_seconds(cfg):
    return TIMEFRAME_SEC[cfg.timeframe]
