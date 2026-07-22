# Running the bot on MetaTrader 5 — step-by-step

The bot connects to MT5 through the **official MetaTrader5 Python package**.
It is not an Expert Advisor (.ex5) — Python runs next to the terminal and
talks to it. Orders carry **server-side SL/TP**, so your stops keep working
even if the bot or your PC connection drops.

**Requirements:** Windows (the MetaTrader5 package does not exist for
macOS/Linux — use a Windows VPS otherwise), an MT5 broker account, and
Python 3.10–3.12 **64-bit**.

> ⚠️ Do the whole tutorial on a **demo account** first. Only move to a real
> account after the demo has run cleanly for a while. All trading is your
> own risk.

---

## Step 1 — Install the MetaTrader 5 terminal

1. Download MT5 from **your broker's website** (or metatrader5.com).
2. Install it and log in. To create a demo account: **File → Open an
   Account → your broker → Demo**, pick a deposit similar to what you'd
   really trade.
3. Verify you see live prices in **Market Watch** (left panel,
   `Ctrl+M` if hidden).

## Step 2 — Enable algorithmic trading

1. In MT5: **Tools → Options → Expert Advisors** → tick
   **"Allow algorithmic trading"** → OK.
2. Make sure the **"Algo Trading"** button in the top toolbar is **green /
   active**. If it's off, every order returns retcode `10027`.

## Step 3 — Install Python (64-bit)

1. Download Python 3.12 (64-bit) from python.org.
2. During install tick **"Add python.exe to PATH"**.
3. Check it in a new Command Prompt / PowerShell:
   ```bat
   python --version
   ```

## Step 4 — Get the bot and install dependencies

```bat
git clone https://github.com/alghostrader/jamal.git
cd jamal
git checkout claude/fable-5-trading-system-q9rs9i
cd trading-system

python -m venv venv
venv\Scripts\activate
pip install -r requirements-mt5.txt
```

(No git? Download the branch as a ZIP from GitHub instead.)

## Step 5 — Find your broker's exact symbol names

Brokers name symbols differently: `BTCUSD`, `BTCUSD.r`, `BTCUSDm`,
`EURUSD`... In MT5's Market Watch, right-click → **Show All**, and note the
exact spelling of what you want to trade.

## Step 6 — Configure the bot

Edit `config.yaml`:

```yaml
mode: paper                # keep paper for now
platform: mt5
symbols:
  - BTCUSD                 # your broker's exact names from step 5
timeframe: 5m
```

The bot talks to the terminal that is already running and logged in — no
passwords needed in that case. (Optionally set `MT5_LOGIN` / `MT5_PASSWORD`
/ `MT5_SERVER` in a `.env` file to have the bot log in itself.)

## Step 7 — Backtest on your broker's data

With the MT5 terminal running:

```bat
python -m tradebot backtest --days 30
```

This pulls history from your broker and reports trades, win rate, profit
factor, max drawdown. If it errors with "symbol not found", fix the name in
`config.yaml` (step 5).

## Step 8 — Paper trade on the live feed

```bat
python -m tradebot run
```

`mode: paper` means simulated money on real MT5 prices — no orders reach
your account. Let it run for days/weeks; results land in `logs/trades.csv`
and `logs/equity.csv`. Keep the MT5 terminal open the whole time.

## Step 9 — Go live on the DEMO account

When paper results look acceptable:

1. Make sure the terminal is logged into your **demo** account.
2. In `config.yaml`:
   ```yaml
   mode: live
   i_understand_live_trading_risk: true
   ```
3. `python -m tradebot run` — real orders now hit the demo account. You'll
   see them in the terminal's **Trade** tab, tagged with the bot's magic
   number, with SL/TP attached server-side.

## Step 10 — Real account (optional, your risk)

Same as step 9 with the terminal logged into the real account. Rules that
keep this survivable:

- Start with money you can afford to lose entirely.
- Keep the PC/VPS and terminal running 24/7 (a Windows VPS near your
  broker's server is the standard setup).
- The bot only manages its own positions (magic number `20260722`); manual
  trades are untouched — but the daily-loss halt reads *account* equity, so
  big manual losses will also pause the bot. That is intentional.
- Stopping the bot (Ctrl+C) closes its open positions so you're flat.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `MT5 initialize failed` | Terminal not running/logged in; or 32-bit Python (must be 64-bit); or set `MT5_TERMINAL_PATH` in `.env` to `terminal64.exe` |
| `symbol 'X' not found` | Use the broker's exact spelling (step 5) |
| Order rejected, retcode `10027` | "Algo Trading" toolbar button is off (step 2) |
| Retcode `10030` invalid fill | Handled automatically (retries FOK); if it persists, your broker uses "Return" filling — say so and we'll add it |
| Retcode `10019` no money | Position size vs your balance/leverage — lower `risk_per_trade_pct` or `max_position_pct` |
| `pip install MetaTrader5` fails | You're not on Windows, or Python is 32-bit |
| Backtest returns few candles | Broker keeps limited M5 history; try a smaller `--days` or a bigger timeframe |

## Limitations to know

- **Long-only** (same as the crypto mode). Shorting MT5 CFDs is possible —
  it can be added, but the strategies are currently long-side.
- Lot sizing assumes symbols quoted in your account currency (BTCUSD /
  EURUSD on a USD account). Cross pairs (e.g. EURGBP on a USD account) will
  size slightly off.
- Non-crypto markets close on weekends; the bot will just idle then.
- This adapter follows the official MetaTrader5 API but was written in a
  Linux environment where it cannot be executed — one more reason the demo
  account comes first. If anything errors on your machine, send me the exact
  message and I'll fix it.
