import argparse

from .backtest import print_report, run_backtest
from .config import load_config, timeframe_seconds


def main():
    parser = argparse.ArgumentParser(prog="tradebot",
                                     description="Automated crypto trading bot")
    parser.add_argument("--config", default="config.yaml")
    sub = parser.add_subparsers(dest="cmd", required=True)

    bt = sub.add_parser("backtest", help="run the strategy over historical data")
    bt.add_argument("--days", type=int, default=30, help="days of exchange history")
    bt.add_argument("--symbol", help="single symbol override, e.g. BTC/USDT")
    bt.add_argument("--csv", help="backtest a local OHLCV CSV instead of fetching")
    bt.add_argument("--synthetic", action="store_true",
                    help="use generated data (pipeline test only, not a real market)")

    sub.add_parser("run", help="start the paper/live trading engine")

    args = parser.parse_args()
    cfg = load_config(args.config)

    if args.cmd == "run":
        from .engine import Engine
        Engine(cfg).run()
        return

    if args.synthetic:
        from .synth import synthetic_ohlcv
        df = synthetic_ohlcv(timeframe_sec=timeframe_seconds(cfg))
        print("NOTE: synthetic data — this validates the pipeline, not the strategy.")
        print_report("SYNTH/USDT", run_backtest(cfg, df, "SYNTH/USDT"))
        return

    if args.csv:
        from .data import load_csv
        df = load_csv(args.csv)
        print_report(args.csv, run_backtest(cfg, df, args.symbol or "CSV/DATA"))
        return

    from .data import MarketData
    data = MarketData(cfg)
    for symbol in [args.symbol] if args.symbol else cfg.symbols:
        print(f"fetching {args.days}d of {cfg.timeframe} candles for {symbol}...")
        df = data.history(symbol, args.days)
        print(f"  {len(df)} candles")
        print_report(symbol, run_backtest(cfg, df, symbol))


if __name__ == "__main__":
    main()
