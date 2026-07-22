# Tradebot — automated crypto scalping/swing bot

An automated trading system that watches crypto markets in real time, finds
entry opportunities, sizes positions by risk, executes trades, and enforces
hard risk limits. Runs against any [ccxt](https://github.com/ccxt/ccxt)
exchange (Binance, Bybit, Kraken, OKX, ...) — or against **MetaTrader 5**
via its official Python API (Windows; see [MT5-SETUP.md](MT5-SETUP.md)).

**Default mode is paper trading**: live market data, simulated money,
realistic fees and slippage. Live trading is opt-in and double-gated.

---

## ⚠️ Honest disclaimer — read this first

- **This bot does not guarantee profits.** No bot can. Short-timeframe
  trading is the hardest game in the market: every round trip pays roughly
  0.2–0.25% in fees + slippage, and you compete with firms co-located next
  to the exchange.
- A profitable backtest does **not** mean profitable live trading
  (overfitting, regime changes, fill quality).
- The correct workflow is: **backtest → paper trade for weeks → tiny live
  size only if paper results hold up**. Skipping steps is how accounts die.
- Anything you run in live mode is entirely **your own risk**.

## Quick start

```bash
cd trading-system
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 1. Backtest on real exchange data (no API keys needed)
python -m tradebot backtest --days 30

# 2. Paper trade on live prices (no API keys needed)
python -m tradebot run
```

Other backtest options:

```bash
python -m tradebot backtest --days 90 --symbol BTC/USDT   # one symbol, more history
python -m tradebot backtest --csv my_candles.csv           # your own OHLCV data
python -m tradebot backtest --synthetic                    # offline pipeline check
```

Trades and equity are logged to `logs/trades.csv` and `logs/equity.csv`.

## How it works

```
MarketData (ccxt) ──► Strategy (signals) ──► RiskManager (gate + size) ──► Broker (fills)
      │                                                                       │
      └────────────── Engine loop: stops / take-profits / logging ◄───────────┘
```

| Module | Role |
|---|---|
| `tradebot/data.py` | live candles, paginated history, CSV loading |
| `tradebot/strategy.py` | signal generation (pluggable, long-only) |
| `tradebot/risk.py` | position sizing, daily loss halt, cooldowns |
| `tradebot/broker.py` | paper fills with fees/slippage; live orders via ccxt |
| `tradebot/engine.py` | live/paper loop: data → signal → risk → order |
| `tradebot/backtest.py` | event-driven backtester using the same code paths |
| `tradebot/synth.py` | synthetic candles for offline pipeline tests |

### Strategy: `regime_combo` (default)

A regime filter (EMA20−EMA50 spread normalised by ATR) decides which edge to
hunt:

- **Trending up** → `momentum_breakout`: buy a close above the 20-candle
  high on above-average volume; stop 1.5 ATR below, take profit at 2R.
- **Ranging** → `mean_reversion`: buy a close below the lower Bollinger band
  with RSI < 30; target the middle band, same ATR stop.

Both are also available standalone via `strategy.name` in `config.yaml`.
Strategies are plain classes with one `evaluate(df)` method — add your own in
`strategy.py` and register it in the `STRATEGIES` dict.

### Risk rules (all enforced in code, all configurable)

- Risk per trade: hitting a stop loses at most `risk_per_trade_pct` of equity
  (default 0.5%).
- Max position size, max concurrent positions.
- **Daily loss halt**: past `max_daily_loss_pct` (default 3%), no new trades
  until the next day.
- Cooldown after a losing trade before re-entering the same symbol.
- Backtester is pessimistic: entries fill at the *next* candle's open, and
  when a candle contains both the stop and the target, the stop wins.

## Going live (only after paper trading convinces you)

1. Create exchange API keys with **trade permission only — never
   withdrawal**. Restrict them to your IP if the exchange supports it.
2. `cp .env.example .env` and fill in the keys.
3. In `config.yaml` set `mode: live` **and**
   `i_understand_live_trading_risk: true` (the bot refuses to start live
   without both).
4. Start with a small balance you can afford to lose entirely.

**Live-mode limitation:** stops and take-profits are *soft* — the bot sends a
market order when the level is crossed, so it must stay running (use a VPS +
`systemd`/`tmux`). If the bot or your connection dies, positions are
unprotected unless you also place exchange-side stop orders manually.

## Notes

- Spot only, long only (spot accounts cannot short).
- The signal timeframe defaults to 5m; 1m is supported but fees hurt more the
  faster you trade.
- This cloud workspace cannot reach exchange APIs (geo-blocked), which is why
  the synthetic mode exists; on your own machine `backtest --days 30` and
  `run` use real market data.
