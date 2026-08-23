#!/usr/bin/env python3
"""Re-probe every keyword target's live Google position (DataForSEO SERP live)."""
import json, os, time, requests
AUTH = (os.environ["DFS_LOGIN"], os.environ["DFS_PASSWORD"])
BASE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
LOC = {"iptvesp.com": ("Spain", "es"), "primeiptv-france.com": ("France", "fr"),
       "iptvned.com": ("Netherlands", "nl"), "iptvpix.com": ("France", "fr"),
       "smarters-live.com": ("France", "fr"), "iptvshqiptar.com": ("Albania", "sq"),
       "smartersprofrance.fr": ("France", "fr"), "iptvfranceofficiel.fr": ("France", "fr"),
       "abonnementiptvofficiel.com": ("France", "fr"), "iptvsegura.com": ("Spain", "es")}

def serp_pos(kw, loc, lang, domain):
    last = "no response"
    for attempt in range(4):
        try:
            r = requests.post(API, auth=AUTH, json=[{"keyword": kw, "location_name": loc,
                              "language_code": lang, "depth": 100}], timeout=120)
            d = r.json()
        except Exception as e:
            last = str(e)[:60]; time.sleep(2 * (attempt + 1)); continue
        if d.get("status_code") != 20000:
            last = d.get("status_message"); time.sleep(2 * (attempt + 1)); continue
        t = d["tasks"][0]
        if t.get("status_code") != 20000 or not t.get("result"):
            last = t.get("status_message"); time.sleep(2 * (attempt + 1)); continue
        for it in (t["result"][0].get("items") or []):
            if it.get("type") == "organic" and domain in (it.get("domain") or ""):
                return it.get("rank_absolute"), it.get("relative_url") or "/", None
        return None, None, None
    return None, None, last

KT = json.load(open(os.path.join(BASE, "keyword_targets.json")))
moved = 0
for site, rows in KT.items():
    loc, lang = LOC[site]
    for r in rows:
        old = r.get("pos")
        pos, url, err = serp_pos(r["kw"], loc, lang, site)
        if err:
            print(f"  {site} · {r['kw']!r}: probe error ({err}) — keeping pos={old}"); continue
        r["pos"] = pos
        if url: r["url"] = url
        elif "url" in r: del r["url"]
        if pos != old:
            moved += 1
            print(f"  MOVED {site} · {r['kw']!r}: {old} -> {pos} {url or ''}")
        time.sleep(0.4)
json.dump(KT, open(os.path.join(BASE, "keyword_targets.json"), "w"), indent=1, ensure_ascii=False)
print(f"saved keyword_targets.json — {sum(len(v) for v in KT.values())} checked, {moved} moved")
