#!/usr/bin/env python3
"""Crawl -> audit_findings.json (technical defects per site)."""
import json, os, requests
from urllib.parse import urlparse
from _sites import SITES
BASE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/125.0 Mobile SEO-Audit"}

def head(u):
    try:
        r = requests.head(u, headers=UA, timeout=20, allow_redirects=False)
        loc = r.headers.get("location", "")
        return f"{r.status_code}" + (f" -> {loc}" if loc else "")
    except Exception as e:
        return f"err {str(e)[:40]}"

out = {}
for slug, dom, canon in SITES:
    try:
        c = json.load(open(os.path.join(BASE, f"d_{slug}", "crawl.json")))
    except Exception:
        out[dom] = {"pages": 0, "error": "no crawl"}; continue
    pages = c["pages"]; edges = c["edges"]
    by_url = {p["url"]: p for p in pages}
    html200 = [p for p in pages if p.get("status") == 200 and "text/html" in (p.get("content_type") or "")]
    path_of = lambda u: (urlparse(u).path or "/").lstrip("/")
    over = sorted([(len(p.get("title", "")), path_of(p["url"])) for p in html200 if len(p.get("title", "")) > 60], reverse=True)
    tgts = {e[1] for e in edges}
    redirect_links = sorted({path_of(t) for t in tgts if by_url.get(t) and by_url[t].get("redirect_chain")})
    linked404 = {}
    for e in edges:
        t = by_url.get(e[1])
        if t and t.get("status") == 404:
            linked404[path_of(e[1])] = linked404.get(path_of(e[1]), 0) + 1
    reachable = tgts | {p["url"] for p in html200 if (urlparse(p["url"]).path or "/") == "/"}
    sm = set(c.get("sitemap", []))
    orphans = sorted({path_of(p["url"]) for p in html200
                      if p["url"] in sm and p["url"] not in reachable and (urlparse(p["url"]).path or "/") != "/"})
    # canonical mismatch = canonical points to a DIFFERENT PATH. A query-param URL
    # (e.g. /checkout?plan=x) canonicalizing to its own clean path is correct, not a defect.
    canon_mm = []
    for p in html200:
        cn = (p.get("canonical") or "").strip()
        if not cn: continue
        if urlparse(cn).path.rstrip("/") != urlparse(p["url"]).path.rstrip("/"):
            canon_mm.append(path_of(p["url"]))
    f = {"pages": len(html200), "titles_over60": over, "redirect_links": redirect_links,
         "linked404": linked404, "orphans": orphans, "canonical_mismatch": sorted(canon_mm),
         "no_meta_desc": sorted([path_of(p["url"]) for p in html200 if not p.get("meta_description")]),
         "thin": sorted([path_of(p["url"]) for p in html200 if (p.get("word_count") or 0) < 300]),
         "favicon": (lambda s: int(s.split()[0]) if s.split()[0].isdigit() else None)(head(f"https://{canon}/favicon.ico"))}
    if canon.startswith("www."):
        f["apex"] = head(f"https://{dom}/"); f["www"] = head(f"https://{canon}/")
        f["www_redirect"] = "200"
    else:
        f["www_redirect"] = head(f"https://www.{dom}/")
    out[dom] = f
    print(f"{dom}: {f['pages']} pages, titles>60={len(over)}, redirect_links={len(redirect_links)}, "
          f"orphans={len(orphans)}, canon_mm={len(canon_mm)}, 404s={len(linked404)}, "
          f"www={str(f.get('www_redirect'))[:22]}{' apex=' + str(f.get('apex'))[:12] if 'apex' in f else ''}")

json.dump(out, open(os.path.join(BASE, "audit_findings.json"), "w"), indent=1)
print("saved audit_findings.json")
