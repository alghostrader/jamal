#!/usr/bin/env python3
"""Owner-entered sales from the Sales app (Firestore `trackers/{uid}.sales`) → revenue.json, AGGREGATED per site.
No client names, phone numbers or device keys ever leave Firestore. Source label everywhere: "owner-entered (Sales app)".
Attribution between sites stays UNAVAILABLE — a sale is credited to the site the owner recorded it on."""
import json, os, datetime, requests, collections
from google.oauth2 import service_account
from google.auth.transport.requests import Request
BASE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(BASE, "revenue.json")
from _sites import SITES
TODAY = datetime.date.today()
def val(v):
    for k in ("stringValue", "integerValue", "doubleValue", "booleanValue"):
        if k in v: return v[k]
    if "mapValue" in v: return {k: val(x) for k, x in v["mapValue"].get("fields", {}).items()}
    if "arrayValue" in v: return [val(x) for x in v["arrayValue"].get("values", [])]
    return None
def site_of(key):
    k = (key or "").lower().strip()
    for slug, dom, _ in SITES:
        if k in (slug, dom, dom.split(".")[0]) or k.replace("-", "") == dom.split(".")[0].replace("-", ""): return dom
    for slug, dom, _ in SITES:
        if k and (k in dom or dom.split(".")[0] in k): return dom
    return None
try:
    creds = service_account.Credentials.from_service_account_file(os.path.join(BASE, "..", "gsc", "sa.json"), scopes=["https://www.googleapis.com/auth/datastore"]); creds.refresh(Request())
    H = {"Authorization": f"Bearer {creds.token}"}
    r = requests.get("https://firestore.googleapis.com/v1/projects/iptv-sales/databases/(default)/documents/trackers?pageSize=50", headers=H, timeout=30)
    if r.status_code != 200: raise RuntimeError(f"HTTP {r.status_code}")
    by = collections.defaultdict(lambda: {"sales_7d": 0, "revenue_7d": 0.0, "sales_28d": 0, "revenue_28d": 0.0, "sales_all": 0, "revenue_all": 0.0, "last_sale": None, "unmapped": 0})
    n_rows = 0; unmapped = collections.Counter()
    for doc in r.json().get("documents", []):
        for s in (val(doc["fields"].get("sales", {"arrayValue": {}})) or []):
            if not isinstance(s, dict): continue
            n_rows += 1
            if str(s.get("status", "")).lower() not in ("paid", "renewed", "active", "completed"): continue
            if "test" in str(s.get("client_name", "")).lower(): continue   # test rows never count as revenue
            dom = site_of(s.get("site"))
            if not dom: unmapped[str(s.get("site"))] += 1; continue
            try: d = datetime.date.fromisoformat(str(s.get("sale_date"))[:10])
            except Exception: continue
            try: eur = float(str(s.get("price_eur") or 0).replace(",", "."))
            except Exception: eur = 0.0
            age = (TODAY - d).days
            b = by[dom]; b["sales_all"] += 1; b["revenue_all"] += eur
            if 0 <= age < 28: b["sales_28d"] += 1; b["revenue_28d"] += eur
            if 0 <= age < 7: b["sales_7d"] += 1; b["revenue_7d"] += eur
            if not b["last_sale"] or d.isoformat() > b["last_sale"]: b["last_sale"] = d.isoformat()
    out = {"fetched": TODAY.isoformat(), "ok": True, "source": "owner-entered (Sales app, Firestore trackers)", "attribution": "unavailable",
           "rows_read": n_rows, "unmapped_site_keys": dict(unmapped), "by_site": {k: {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in by.items()},
           "sites_with_sales": len(by), "sites_total": len(SITES)}
    print(f"revenue: {n_rows} rows read · {len(by)} site(s) with paid sales · 28d € {sum(v['revenue_28d'] for v in by.values()):.0f} · unmapped keys {dict(unmapped) or 'none'}")
except Exception as e:
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    out = {**prev, "ok": False, "error": str(e)[:160], "fetched": prev.get("fetched")}
    print("revenue unavailable:", str(e)[:120])
json.dump(out, open(OUT, "w"), indent=1)
