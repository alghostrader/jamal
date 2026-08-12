#!/usr/bin/env python3
"""Append today's authority + ranking snapshot to history.json (one point per day)."""
import json, os, datetime
from _sites import SITES
BASE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(BASE, "..", "dash", "dash_data.json")))
KT = json.load(open(os.path.join(BASE, "keyword_targets.json")))
P = os.path.join(BASE, "history.json")
try: hist = json.load(open(P))
except Exception: hist = []
today = datetime.date.today().isoformat()
snap = {"date": today, "sites": {}}
for _, dom, _c in SITES:
    dfs = (D["sites"].get(dom, {}) or {}).get("dfs", {}) or {}
    snap["sites"][dom] = {"ref_domains": dfs.get("ref_domains"), "backlinks": dfs.get("backlinks"),
                          "domain_rank": dfs.get("domain_rank"), "spam_score": dfs.get("spam_score"),
                          "ranked_top100": dfs.get("ranked_top100"),
                          "targets_ranking": sum(1 for r in KT.get(dom, []) if r.get("pos"))}
hist = [h for h in hist if h.get("date") != today] + [snap]
hist.sort(key=lambda h: h["date"])
json.dump(hist, open(P, "w"), indent=1)
print(f"history.json now has {len(hist)} day(s); latest {today}")
