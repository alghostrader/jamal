#!/usr/bin/env python3
"""Indexation check via the GSC URL Inspection API for PRIORITY URLs only
(money pages + strategic keyword-target pages + the newest site's core pages).
Quota-aware: ~30 URLs per audit, far under the 2,000/day per-property limit.
Writes indexation.json."""
import json, os, re as RE, datetime, requests
from _sites import SITES
from google.oauth2 import service_account
from google.auth.transport.requests import Request

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = os.path.join(BASE, "..", "gsc", "sa.json")
creds = service_account.Credentials.from_service_account_file(
    KEY, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
creds.refresh(Request())
H = {"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}

KT = json.load(open(os.path.join(BASE, "keyword_targets.json")))
MONEY = {"iptvesp.com": "/suscripciones", "primeiptv-france.com": "/tarifs",
         "iptvned.com": "/abonnementen", "iptvpix.com": "/abonnements",
         "smartersprofrance.fr": "/abonnement-iptv", "iptvfranceofficiel.fr": "/iptv-premium",
         "abonnementiptvofficiel.com": "/test-iptv", "iptvsegura.com": "/planes",
         "rodaktv.com": "/abonament"}
CANON = {d: c for _, d, c in SITES}

targets = {}
for _, dom, _c in SITES:
    urls = set()
    if dom in MONEY:
        urls.add(MONEY[dom])
    urls.add("/")
    for r in KT.get(dom, []):
        p = (r.get("page") or "").split(" ")[0].strip()
        # page hints can be descriptive ("/x (notes)") — keep only clean absolute paths
        if p.startswith("/") and RE.fullmatch(r"/[A-Za-z0-9\-_/.]*", p):
            urls.add(p)
    targets[dom] = sorted(urls)

OUT = {"generated": datetime.date.today().isoformat(), "sites": {}}
n = 0
for dom, paths in targets.items():
    prop = f"sc-domain:{dom}"
    res = {}
    for p in paths:
        full = f"https://{CANON[dom]}{p}"
        body = {"inspectionUrl": full, "siteUrl": prop}
        try:
            r = requests.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                              headers=H, json=body, timeout=60)
        except requests.RequestException:
            res[p] = {"state": "ERROR", "detail": "request failed"}
            continue
        if r.status_code != 200:
            res[p] = {"state": "UNAVAILABLE", "detail": f"http {r.status_code}"}
            continue
        j = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
        res[p] = {"state": j.get("coverageState"), "verdict": j.get("verdict"),
                  "canonical_google": j.get("googleCanonical"),
                  "canonical_user": j.get("userCanonical"),
                  "last_crawl": j.get("lastCrawlTime")}
        n += 1
    OUT["sites"][dom] = res
    ok = sum(1 for v in res.values() if v.get("verdict") == "PASS")
    print(f"{dom}: {ok}/{len(res)} indexed-pass")
json.dump(OUT, open(os.path.join(BASE, "indexation.json"), "w"), indent=1)
print(f"saved indexation.json ({n} inspections)")
