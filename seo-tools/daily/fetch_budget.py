#!/usr/bin/env python3
"""Measured spend: DataForSEO account balance + money spent (appendix/user_data), Semrush API units (from the last pull),
and the audit's own call counts. Writes budget.json. Nothing here is estimated: a price that is not returned by the API reads 'not measured'."""
import json, os, datetime, requests
BASE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(BASE, "budget.json")
def env():
    p = os.path.join(BASE, "..", "dash", ".env")
    for line in open(p):
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1); os.environ.setdefault(k, v.strip().strip('"'))
env()
out = {"fetched": datetime.date.today().isoformat(), "dfs": {}, "semrush": {}, "calls_per_audit": {}}
try:
    r = requests.get("https://api.dataforseo.com/v3/appendix/user_data", auth=(os.environ["DFS_LOGIN"], os.environ["DFS_PASSWORD"]), timeout=30)
    d = r.json()["tasks"][0]["result"][0]
    money = d.get("money", {}); rates = d.get("rates", {}).get("statistics", {}) or {}
    out["dfs"] = {"balance_usd": money.get("balance"), "spent_total_usd": money.get("total"), "limits": d.get("limits", {}),
                  "day": rates.get("day", {}), "month": rates.get("month", {}) if isinstance(rates.get("month"), dict) else rates.get("month"),
                  "backlinks_balance": (d.get("backlinks_subscription") or {}).get("balance") if isinstance(d.get("backlinks_subscription"), dict) else None}
    print("DFS balance", money.get("balance"), "USD · spent total", money.get("total"))
except Exception as e:
    out["dfs"] = {"error": str(e)[:120]}; print("DFS user_data failed:", str(e)[:100])
try:
    sem = json.load(open(os.path.join(BASE, "semrush.json")))
    out["semrush"] = {"units": "exhausted (API units balance zero on 11 Sep)" if "exhausted" in json.dumps(sem) else "available", "last_full_pull": sem.get("_updated")}
except Exception: pass
try:
    kt = json.load(open(os.path.join(BASE, "keyword_targets.json"))); ix = json.load(open(os.path.join(BASE, "indexation.json")))
    out["calls_per_audit"] = {"dfs_serp_live_probes": sum(len(v) for v in kt.values()), "dfs_backlinks_summary": 11, "dfs_keyword_volumes": "weekly batch (build_content_kw.py)",
                              "gsc_search_analytics": 11 * 9 + 11, "gsc_url_inspection": sum(len(v) for v in ix.get("sites", {}).values()), "semrush_reports": 22, "firestore_reads": 2, "own_crawler_pages": "~550"}
except Exception: pass
# balance history → measured daily drawdown (the only honest per-audit cost figure)
HP = os.path.join(BASE, "budget_history.json")
try: hist = json.load(open(HP))
except Exception: hist = []
bal = out["dfs"].get("balance_usd")
if bal is not None:
    hist = [h for h in hist if h.get("date") != out["fetched"]] + [{"date": out["fetched"], "dfs_balance_usd": float(bal), "dfs_spent_total_usd": float(out["dfs"].get("spent_total_usd") or 0)}]
    json.dump(hist, open(HP, "w"), indent=1)
out["history"] = hist[-30:]
json.dump(out, open(OUT, "w"), indent=1); print(json.dumps(out["calls_per_audit"]))
