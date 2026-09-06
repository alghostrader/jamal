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
    tasks, links = {}, {}
    for d in r.json().get("documents", []):
        f = {k: val(v) for k, v in d.get("fields", {}).items()}
        tasks.update(f.get("tasks") or {}); links.update(f.get("links") or {})
    state = {"fetched": datetime.datetime.utcnow().isoformat(timespec="minutes") + "Z", "ok": True,
             "tasks": tasks, "links": links}
    done = sum(1 for t in tasks.values() if isinstance(t, dict) and t.get("state") == "completed")
    print(f"cloud state: {len(tasks)} task states ({done} completed) · {len(links)} matrix ticks")
except Exception as e:
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    state = {**prev, "ok": False, "error": str(e)[:200], "fetched": prev.get("fetched")}
    print("cloud state unavailable:", str(e)[:120], "— keeping previous snapshot")
json.dump(state, open(OUT, "w"), indent=1)
