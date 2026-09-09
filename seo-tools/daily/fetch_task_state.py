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
    # ---- git-side updates: other Claude Code sessions (no browser) append lines to task_updates.jsonl ----
    UPD = os.path.join(BASE, "task_updates.jsonl")
    git_n = 0
    if os.path.exists(UPD):
        for line in open(UPD, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"): continue
            try: u = json.loads(line)
            except Exception: print("task_updates.jsonl: skipped bad line:", line[:80]); continue
            tid, st = str(u.get("id", "")).strip(), str(u.get("state", "completed"))
            if not tid: continue
            when = str(u.get("date") or datetime.date.today().isoformat())
            if tid.startswith("lp-"):
                if st == "completed": links[tid] = 1
                if u.get("url"): link_urls[tid] = u["url"]
                git_n += 1; continue
            cur = tasks.get(tid) if isinstance(tasks.get(tid), dict) else {}
            # the most recent decision wins (git line vs browser tick), ties go to the git line
            if cur.get("state") and (cur.get("completed") or cur.get("updated") or "") > when: continue
            new = {**cur, "state": st, "updated": when, "by": u.get("by", "git"), "note": u.get("note", "")}
            if st == "completed": new["completed"] = when
            if u.get("url"): new["url"] = u["url"]
            if u.get("title") and not new.get("title"): new["title"] = u["title"]
            tasks[tid] = new; git_n += 1
    state = {"fetched": datetime.datetime.utcnow().isoformat(timespec="minutes") + "Z", "ok": True,
             "tasks": tasks, "links": links, "link_urls": link_urls, "git_updates": git_n}
    # push the merged state back so every browser/device sees git-side ticks too (needs write access:
    # role Cloud Datastore User on iptv-sales; read-only Viewer just prints a note)
    if git_n:
        docs = r.json().get("documents", [])
        if docs:
            name = docs[0]["name"]
            def enc(v):
                if isinstance(v, bool): return {"booleanValue": v}
                if isinstance(v, int): return {"integerValue": str(v)}
                if isinstance(v, float): return {"doubleValue": v}
                if isinstance(v, list): return {"arrayValue": {"values": [enc(x) for x in v]}}
                if isinstance(v, dict): return {"mapValue": {"fields": {k: enc(x) for k, x in v.items()}}}
                return {"stringValue": str(v)}
            body = {"fields": {"tasks": enc(tasks), "links": enc(links), "link_urls": enc(link_urls),
                               "updated_at": {"integerValue": str(int(datetime.datetime.utcnow().timestamp() * 1000))}}}
            pr = requests.patch(f"https://firestore.googleapis.com/v1/{name}?updateMask.fieldPaths=tasks&updateMask.fieldPaths=links&updateMask.fieldPaths=link_urls&updateMask.fieldPaths=updated_at",
                                headers={"Authorization": f"Bearer {creds.token}"}, json=body, timeout=30)
            print(f"git updates → Firestore: HTTP {pr.status_code}" + ("" if pr.status_code == 200 else " (grant the service account 'Cloud Datastore User' on iptv-sales to mirror git ticks into the browser dashboard; the audit uses them regardless)"))
    # the checklist IS the ledger: a ticked placement that is not in the CSV yet becomes a pending row
    # (with its URL) — live_verify/donext then fetches it and promotes it to live / decayed.
    import csv
    LEDGER = os.path.join(BASE, "backlink_ledger.csv")
    if os.path.exists(LEDGER):
        rows = list(csv.DictReader(open(LEDGER, encoding="utf-8")))
        fields = ["site", "platform", "slug", "detail", "follow", "status", "verified", "url", "checked", "http"]
        have = {(r["slug"], r["site"]) for r in rows}
        # a ticked placement that already has a ledger row but no URL yet gets the URL attached
        for r in rows:
            lid = f'lp-{r["slug"]}-{r["site"]}'
            if not r.get("url") and link_urls.get(lid): r["url"] = link_urls[lid]; added += 1 if False else 0; r["_touched"] = 1
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
            if slug not in KNOWN and not slug.startswith("gp-") and not link_urls.get(lid): continue
            rows.append({"site": key, "platform": slug.title(), "slug": slug, "detail": "ticked on the dashboard", "follow": "",
                         "status": "pending", "verified": "", "url": link_urls.get(lid, ""), "checked": "", "http": ""}); added += 1
        if added or any(r.pop("_touched", None) for r in rows):
            for r in rows:
                for f in fields: r.setdefault(f, "")
            with open(LEDGER, "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
            print(f"ledger: {added} pending placement(s) added from dashboard ticks")
    done = sum(1 for t in tasks.values() if isinstance(t, dict) and t.get("state") == "completed")
    print(f"cloud state: {len(tasks)} task states ({done} completed) · {len(links)} matrix ticks · {len(link_urls)} placement URLs · {git_n} git-side updates")
except Exception as e:
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    state = {**prev, "ok": False, "error": str(e)[:200], "fetched": prev.get("fetched")}
    print("cloud state unavailable:", str(e)[:120], "— keeping previous snapshot")
json.dump(state, open(OUT, "w"), indent=1)
