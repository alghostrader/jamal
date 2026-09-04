#!/usr/bin/env python3
"""Deep GSC pull for the analytics dashboard: per-site query/page tables for the
last 28 complete days vs the previous 28, device + country splits, and 7/28/90d
totals with previous-period comparisons. Writes gsc_details.json.

Quota math: 8 searchanalytics requests per site x 11 sites = 88 calls per audit,
well inside the 1,200/min per-property limit. GSC data lags ~2 days, so windows
end at today-3 (always complete days -> comparisons are complete-vs-complete)."""
import json, os, datetime, requests
from _sites import SITES
from google.oauth2 import service_account
from google.auth.transport.requests import Request

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = os.path.join(BASE, "..", "gsc", "sa.json")
creds = service_account.Credentials.from_service_account_file(
    KEY, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
creds.refresh(Request())
H = {"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}

today = datetime.date.today()
END = today - datetime.timedelta(days=3)          # last complete GSC day
def win(days, back=0):
    e = END - datetime.timedelta(days=back * days)
    s = e - datetime.timedelta(days=days - 1)
    return s.isoformat(), e.isoformat()

def q(dom, body):
    prop = requests.utils.quote(f"sc-domain:{dom}", safe="")
    u = f"https://www.googleapis.com/webmasters/v3/sites/{prop}/searchAnalytics/query"
    for attempt in range(3):
        try:
            r = requests.post(u, headers=H, json=body, timeout=60)
            if r.status_code == 200:
                return r.json().get("rows", [])
            if r.status_code in (403, 404):
                return None
        except requests.RequestException:
            pass
    return None

def rowmap(rows):
    return {r["keys"][0]: {"clicks": r["clicks"], "impressions": r["impressions"],
                           "ctr": r["ctr"], "position": r["position"]} for r in (rows or [])}

OUT = {"generated": today.isoformat(), "window_end": END.isoformat(), "sites": {}}
c28s, c28e = win(28); p28s, p28e = win(28, 1)
for _, dom, _c in SITES:
    d = {}
    probe = q(dom, {"startDate": c28s, "endDate": c28e, "rowLimit": 1})
    if probe is None:
        OUT["sites"][dom] = {"in_gsc": False}
        print(f"{dom}: not accessible in GSC")
        continue
    # totals for 7/28/90 with previous windows (site-level, complete days)
    tot = {}
    for days in (7, 28, 90):
        cs, ce = win(days); ps, pe = win(days, 1)
        cur = q(dom, {"startDate": cs, "endDate": ce, "rowLimit": 1}) or []
        prv = q(dom, {"startDate": ps, "endDate": pe, "rowLimit": 1}) or []
        def tt(rows):
            if not rows: return {"clicks": 0, "impressions": 0, "ctr": 0, "position": None}
            r = rows[0]
            return {"clicks": r["clicks"], "impressions": r["impressions"],
                    "ctr": r["ctr"], "position": r["position"]}
        tot[str(days)] = {"cur": tt(cur), "prev": tt(prv), "cur_range": [cs, ce], "prev_range": [ps, pe]}
    d["totals"] = tot
    # query + page tables, 28d complete vs previous 28d
    d["queries"] = {"cur": rowmap(q(dom, {"startDate": c28s, "endDate": c28e,
                                          "dimensions": ["query"], "rowLimit": 250})),
                    "prev": rowmap(q(dom, {"startDate": p28s, "endDate": p28e,
                                           "dimensions": ["query"], "rowLimit": 250}))}
    d["pages"] = {"cur": rowmap(q(dom, {"startDate": c28s, "endDate": c28e,
                                        "dimensions": ["page"], "rowLimit": 250})),
                  "prev": rowmap(q(dom, {"startDate": p28s, "endDate": p28e,
                                         "dimensions": ["page"], "rowLimit": 250}))}
    d["device"] = rowmap(q(dom, {"startDate": c28s, "endDate": c28e,
                                 "dimensions": ["device"], "rowLimit": 10}))
    d["country"] = rowmap(q(dom, {"startDate": c28s, "endDate": c28e,
                                  "dimensions": ["country"], "rowLimit": 15}))
    d["in_gsc"] = True
    OUT["sites"][dom] = d
    t28 = tot["28"]["cur"]
    print(f"{dom}: 28d clicks={t28['clicks']} q={len(d['queries']['cur'])} pages={len(d['pages']['cur'])}")
OUT["ranges"] = {"cur28": [c28s, c28e], "prev28": [p28s, p28e]}
json.dump(OUT, open(os.path.join(BASE, "gsc_details.json"), "w"))
print("saved gsc_details.json")
