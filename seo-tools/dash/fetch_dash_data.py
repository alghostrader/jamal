#!/usr/bin/env python3
"""DataForSEO authority refresh (+ GSC traffic when a service-account key is present).
Writes dash_data.json. Rebuilt 12 Aug 2026 after container recycle."""
import json, os, time, datetime, requests, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "daily"))
from _sites import SITES
BASE = os.path.dirname(os.path.abspath(__file__))
today = datetime.date.today()
start = (today - datetime.timedelta(days=92)).isoformat()
end = (today - datetime.timedelta(days=2)).isoformat()
out = {"generated": today.isoformat(), "window": [start, end], "sites": {}}

# ---- GSC (only if the service-account key was restored) ----
KEY = os.path.join(BASE, "..", "gsc", "sa.json")
gsc_ok = False
if os.path.exists(KEY):
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
        creds = service_account.Credentials.from_service_account_file(
            KEY, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
        creds.refresh(Request())
        H = {"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}
        sl = requests.get("https://www.googleapis.com/webmasters/v3/sites", headers=H, timeout=30)
        accessible = {e["siteUrl"] for e in sl.json().get("siteEntry", [])} if sl.status_code == 200 else set()
        for _, dom, _c in SITES:
            prop = f"sc-domain:{dom}"
            u = f"https://www.googleapis.com/webmasters/v3/sites/{requests.utils.quote(prop, safe='')}/searchAnalytics/query"
            r = requests.post(u, headers=H, json={"startDate": start, "endDate": end,
                                                  "dimensions": ["date"], "rowLimit": 100}, timeout=60)
            rows = r.json().get("rows", []) if r.status_code == 200 else []
            out["sites"][dom] = {"daily": [{"date": x["keys"][0], "clicks": x["clicks"],
                                            "impressions": x["impressions"]} for x in rows],
                                 "in_gsc": prop in accessible, "gsc_query_http": r.status_code}
            print(f"  {dom:28} in_gsc={prop in accessible} rows={len(rows)}")
            time.sleep(0.3)
        gsc_ok = True
    except Exception as e:
        print("GSC unavailable:", str(e)[:120])
if not gsc_ok:
    out["gsc_unavailable"] = "service-account key (gsc/sa.json) not present — traffic history paused"
    print("GSC SKIPPED — no service-account key; traffic metrics will show as unavailable")
for _, dom, _c in SITES:
    out["sites"].setdefault(dom, {"daily": [], "in_gsc": None})

# ---- DataForSEO ----
DFS = (os.environ.get("DFS_LOGIN", ""), os.environ.get("DFS_PASSWORD", ""))
MARKETS = {"iptvpix.com": ("France", "fr"), "primeiptv-france.com": ("France", "fr"),
           "smarters-live.com": ("France", "fr"), "iptvshqiptar.com": ("Albania", "sq"),
           "iptvned.com": ("Netherlands", "nl"), "iptvesp.com": ("Spain", "es"),
           "abonnementiptvofficiel.com": ("France", "fr"), "smartersprofrance.fr": ("France", "fr"),
           "iptvfranceofficiel.fr": ("France", "fr")}
if all(DFS):
    for dom, (loc, lang) in MARKETS.items():
        try:
            b = requests.post("https://api.dataforseo.com/v3/backlinks/summary/live", auth=DFS,
                              json=[{"target": dom, "include_subdomains": True}], timeout=60).json()
            bl = ((b.get("tasks") or [{}])[0].get("result") or [{}])[0] or {}
            k = requests.post("https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live", auth=DFS,
                              json=[{"target": dom, "location_name": loc, "language_code": lang, "limit": 1}],
                              timeout=60).json()
            kr = (((k.get("tasks") or [{}])[0].get("result") or [{}])[0]) or {}
            out["sites"].setdefault(dom, {})["dfs"] = {
                "backlinks": bl.get("backlinks"), "ref_domains": bl.get("referring_domains"),
                "ref_main_domains": bl.get("referring_main_domains"), "domain_rank": bl.get("rank"),
                "spam_score": bl.get("backlinks_spam_score"), "ranked_top100": kr.get("total_count")}
        except Exception as e:
            out["sites"].setdefault(dom, {})["dfs"] = {"error": str(e)[:80]}
        time.sleep(0.3)
else:
    out["dfs_skipped"] = "no credentials in env"

json.dump(out, open(os.path.join(BASE, "dash_data.json"), "w"))
for _, dom, _c in SITES:
    v = out["sites"][dom]; d = v.get("daily", []); dfs = v.get("dfs", {}) or {}
    c7 = sum(x["clicks"] for x in d[-7:]) if d else "—"
    print(f"{dom:<28} 7d clicks={c7}  rd={dfs.get('ref_domains')}  bl={dfs.get('backlinks')}  "
          f"rank={dfs.get('domain_rank')}  spam={dfs.get('spam_score')}  top100={dfs.get('ranked_top100')}")
print("saved dash_data.json")
