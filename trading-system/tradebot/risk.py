"""Risk limits: position sizing, daily loss halt, cooldowns.

The risk manager owns every rule that decides *whether* and *how big*,
so strategies stay pure signal generators.
"""

from datetime import timedelta


class RiskManager:
    def __init__(self, cfg, timeframe_sec):
        r = cfg.risk
        self.risk_per_trade_pct = r.risk_per_trade_pct
        self.max_position_pct = r.max_position_pct
        self.max_open_positions = r.max_open_positions
        self.max_daily_loss_pct = r.max_daily_loss_pct
        self.cooldown = timedelta(seconds=r.cooldown_candles * timeframe_sec)
        self.day = None
        self.day_start_equity = None
        self.halted = False
        self.cooldown_until = {}

    def _roll_day(self, now, equity):
        if now.date() != self.day:
            self.day = now.date()
            self.day_start_equity = equity
            self.halted = False

    def can_open(self, symbol, equity, open_positions, now):
        """Return (allowed, reason_if_not)."""
        self._roll_day(now, equity)
        if equity <= self.day_start_equity * (1 - self.max_daily_loss_pct / 100):
            self.halted = True
        if self.halted:
            return False, "daily loss limit hit — no new trades until tomorrow"
        if open_positions >= self.max_open_positions:
            return False, "max open positions reached"
        until = self.cooldown_until.get(symbol)
        if until and now < until:
            return False, f"cooldown after loss until {until:%H:%M:%S}"
        return True, ""

    def position_size(self, equity, entry, stop):
        """Quantity such that hitting the stop loses risk_per_trade_pct of equity."""
        per_unit_risk = entry - stop
        if per_unit_risk <= 0:
            return 0.0
        qty = equity * (self.risk_per_trade_pct / 100) / per_unit_risk
        max_qty = equity * (self.max_position_pct / 100) / entry
        return min(qty, max_qty)

    def on_trade_closed(self, symbol, pnl, now):
        if pnl < 0:
            self.cooldown_until[symbol] = now + self.cooldown
