#!/usr/bin/env python3
"""Read the owner's synced dashboard state (Today/Work ticks + Backlinks matrix) from the
sales project's Firestore (collection seo_state, one doc per signed-in user) using the
monitoring service account (needs Cloud Datastore Viewer on project iptv-sales).
Writes cloud_state.json — consumed by generate_v3.py / v4_pages.py for verification."""
import json, os, datetime, requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
BASE = os.path.dirname(os.path.abspath(__file__))
KEY = os.path.join(BASE, "..", "gsc", "sa.json")
OUT = os.path.join(BASE, "cloud_state.json")
def val(v):
    if "stringValue" in v: return v["stringValue"]
    if "integerValue" in v: return int(v["integerValue"])
    if "doubleValue" in v: return v["doubleValue"]
    if "booleanValue" in v: return v["booleanValue"]
    if "mapValue" in v: return {k: val(x) for k, x in v["mapValue"].get("fields", {}).items()}
    if "arrayValue" in v: return [val(x) for x in v["arrayValue"].get("values", [])]
    return None
try:
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=["https://www.googleapis.com/auth/datastore"])
    creds.refresh(Request())
    r = requests.get("https://firestore.googleapis.com/v1/projects/iptv-sales/databases/(default)/documents/seo_state?pageSize=20",
                     headers={"Authorization": f"Bearer {creds.token}"}, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.json().get('error', {}).get('status')}")
    tasks, links, link_urls = {}, {}, {}
    for d in r.json().get("documents", []):
        f = {k: val(v) for k, v in d.get("fields", {}).items()}
        tasks.update(f.get("tasks") or {}); links.update(f.get("links") or {}); link_urls.update(f.get("link_urls") or {})
    # a task card can also carry the placement URL (Do next → Mark complete on a backlink card)
    for k, t in tasks.items():
        if k.startswith("lp-") and isinstance(t, dict) and t.get("url") and k not in link_urls: link_urls[k] = t["url"]
    state = {"fetched": datetime.datetime.utcnow().isoformat(timespec="minutes") + "Z", "ok": True,
             "tasks": tasks, "links": links, "link_urls": link_urls}
    # the checklist IS the ledger: a ticked placement that is not in the CSV yet becomes a pending row
    # (with its URL) — live_verify/donext then fetches it and promotes it to live / decayed.
    import csv
    LEDGER = os.path.join(BASE, "backlink_ledger.csv")
    if os.path.exists(LEDGER):
        rows = list(csv.DictReader(open(LEDGER, encoding="utf-8")))
        fields = ["site", "platform", "slug", "detail", "follow", "status", "verified", "url", "checked", "http"]
        have = {(r["slug"], r["site"]) for r in rows}
        # only the current target platforms (P1-P3) or ticks that carry a URL — legacy matrix ids from the
        # pre-ledger design are not re-imported as unverified rows
        KNOWN = {"blogger", "wordpress", "medium", "tumblr", "substack", "hotfrog", "cylex", "tupalo", "europages", "infobel",
                 "linktree", "gravatar", "pinterest", "aboutme", "crunchbase"}
        added = 0
        for lid in links:
            m = lid.split("-")
            if len(m) < 3 or lid[:3] != "lp-": continue
            slug, key = "-".join(m[1:-1]), m[-1]
            if (slug, key) in have or key == "one": continue
            if slug not in KNOWN and not link_urls.get(lid): continue
            rows.append({"site": key, "platform": slug.title(), "slug": slug, "detail": "ticked on the dashboard", "follow": "",
                         "status": "pending", "verified": "", "url": link_urls.get(lid, ""), "checked": "", "http": ""}); added += 1
        if added:
            for r in rows:
                for f in fields: r.setdefault(f, "")
            with open(LEDGER, "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
            print(f"ledger: {added} pending placement(s) added from dashboard ticks")
    done = sum(1 for t in tasks.values() if isinstance(t, dict) and t.get("state") == "completed")
    print(f"cloud state: {len(tasks)} task states ({done} completed) · {len(links)} matrix ticks · {len(link_urls)} placement URLs")
except Exception as e:
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    state = {**prev, "ok": False, "error": str(e)[:200], "fetched": prev.get("fetched")}
    print("cloud state unavailable:", str(e)[:120], "— keeping previous snapshot")
json.dump(state, open(OUT, "w"), indent=1)
