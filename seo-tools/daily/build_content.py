#!/usr/bin/env python3
"""Per-site content intel: articles + next-article gaps -> content.json

Cannibalization guards (portfolio level):
1. Satellites draw only from their own keyword targets, never the shared market pool.
2. A keyword with a designated money page (KT "page") is owned by that site market-wide.
3. Once a focus/support site covers a keyword, same-market siblings see it as covered.
"""
import json, os, re, unicodedata
from urllib.parse import urlparse
from _sites import SITES
BASE = os.path.dirname(os.path.abspath(__file__))
MAP = {dom: f"d_{slug}" for slug, dom, _ in SITES}
KT = json.load(open(os.path.join(BASE, "keyword_targets.json")))
try: CKW = json.load(open(os.path.join(BASE, "content_keywords.json")))
except Exception: CKW = {}
MARKET = {"iptvesp.com": "es", "primeiptv-france.com": "fr", "iptvned.com": "nl", "iptvpix.com": "fr",
          "smarters-live.com": "fr", "iptvshqiptar.com": "sq", "abonnementiptvofficiel.com": "fr",
          "smartersprofrance.fr": "fr", "iptvfranceofficiel.fr": "fr"}
SATS = {"smartersprofrance.fr", "iptvfranceofficiel.fr", "abonnementiptvofficiel.com"}
GENERIC = {"iptv", "de", "la", "le", "el", "en", "the", "a", "for", "und", "met", "voor",
           "2026", "2025", "pro", "tv", "om"}

def deaccent(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()

def kw_toks(s):
    return [t for t in re.split(r"[^a-z0-9]+", deaccent(s)) if len(t) >= 2 and t not in GENERIC]

site_pages, site_arts = {}, {}
for dom, d in MAP.items():
    try:
        c = json.load(open(os.path.join(BASE, d, "crawl.json")))
    except Exception:
        site_pages[dom] = []; site_arts[dom] = []; continue
    pages = [p for p in c["pages"] if p.get("status") == 200 and "text/html" in (p.get("content_type") or "")]
    arts = []
    for p in pages:
        path = urlparse(p["url"]).path
        wc = p.get("word_count") or 0
        if ("/blog" in path or "/articles" in path or "/guides" in path) or \
           (wc >= 500 and path not in ("/", "/contact", "/a-propos", "/about")):
            arts.append({"path": path, "title": p.get("title", ""), "words": wc})
    arts.sort(key=lambda x: -x["words"])
    site_arts[dom] = arts
    ptoks = []
    for p in pages:
        blob = deaccent(urlparse(p["url"]).path + " " + (p.get("title") or ""))
        ptoks.append(set(t for t in re.split(r"[^a-z0-9]+", blob) if len(t) >= 2))
    site_pages[dom] = ptoks

def is_covered(dom, kw):
    kt = kw_toks(kw)
    if not kt: return False
    return any(all(t in pt for t in kt) for pt in site_pages.get(dom, []))

kw_owner = {}
for dom, rows in KT.items():
    for r in rows:
        if r.get("page"):
            kw_owner[(MARKET.get(dom), deaccent(r["kw"]))] = dom

out = {}
for dom in MAP:
    mk = MARKET.get(dom)
    pool = KT.get(dom, []) if dom in SATS else \
        (CKW.get(mk, []) if (CKW.get(mk) and any(r["vol"] for r in CKW.get(mk, []))) else KT.get(dom, []))
    siblings = [s for s in MAP if s != dom and MARKET.get(s) == mk and s not in SATS]
    rec = []
    for r in pool:
        entry = {"kw": r["kw"], "vol": r.get("vol") or 0}
        owner = kw_owner.get((mk, deaccent(r["kw"])))
        if r.get("page"):
            entry.update(covered=True, page=r["page"])
        elif is_covered(dom, r["kw"]):
            entry.update(covered=True)
        elif owner and owner != dom:
            entry.update(covered=True, sibling=owner)
        else:
            sib = next((s for s in siblings if is_covered(s, r["kw"])), None)
            entry.update(covered=True, sibling=sib) if sib else entry.update(covered=False)
        rec.append(entry)
    rec.sort(key=lambda x: (x["covered"], -x["vol"]))
    arts = site_arts.get(dom, [])
    out[dom] = {"articles": arts, "recommend": rec, "n_articles": len(arts),
                "n_thin": sum(1 for a in arts if a["words"] < 600)}
    gap = next((r for r in rec if not r["covered"]), None)
    print(f"{dom}: {len(arts)} articles ({out[dom]['n_thin']} thin<600w) · next-gap: "
          + (f"{gap['kw']} ({gap['vol']}/mo)" if gap else "all targets covered"))

json.dump(out, open(os.path.join(BASE, "content.json"), "w"), indent=1, ensure_ascii=False)
print("saved content.json")
