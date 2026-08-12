#!/usr/bin/env python3
"""BFS technical-SEO crawler. Usage: crawler.py <slug> <canonical-host>
Writes d_<slug>/crawl.json  ·  rebuilt 12 Aug 2026 after container recycle."""
import json, re, sys, os, time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

SLUG, CANON = sys.argv[1], sys.argv[2]          # e.g. esp iptvesp.com  /  spf www.smartersprofrance.fr
HOST = CANON.replace("www.", "")
BASE = f"https://{CANON}"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"d_{SLUG}")
os.makedirs(OUT, exist_ok=True)
MAX_PAGES = 200
UA = ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/125.0.0.0 Mobile Safari/537.36 SEO-Audit")
S = requests.Session(); S.headers["User-Agent"] = UA

def norm(url):
    url, _ = urldefrag(url)
    p = urlparse(url)
    if p.scheme not in ("http", "https"): return None
    if p.netloc.replace("www.", "") != HOST: return None
    path = p.path or "/"
    if path != "/" and path.endswith("/"): path = path.rstrip("/")
    return f"https://{CANON}{path}" + (f"?{p.query}" if p.query else "")

# sitemap (best effort) — used for orphan detection
sitemap = set()
try:
    r = S.get(f"{BASE}/sitemap.xml", timeout=25)
    for loc in re.findall(r"<loc>([^<]+)</loc>", r.text):
        if loc.endswith(".xml"):
            try:
                r2 = S.get(loc, timeout=25)
                for l2 in re.findall(r"<loc>([^<]+)</loc>", r2.text):
                    n = norm(l2)
                    if n: sitemap.add(n)
            except Exception: pass
        else:
            n = norm(loc)
            if n: sitemap.add(n)
except Exception: pass

pages, edges = {}, []
q = deque([(BASE + "/", 0)]); seen = {BASE + "/"}
while q and len(pages) < MAX_PAGES:
    url, depth = q.popleft()
    try:
        r = S.get(url, timeout=25, allow_redirects=True)
    except Exception as e:
        pages[url] = {"url": url, "depth": depth, "error": str(e)[:120]}; continue
    d = {"url": url, "final_url": norm(r.url) or r.url, "depth": depth, "status": r.status_code,
         "redirect_chain": [(h.status_code, h.url) for h in r.history],
         "content_type": r.headers.get("content-type", ""),
         "x_robots_tag": r.headers.get("x-robots-tag", ""),
         "size_bytes": len(r.content), "elapsed_s": round(r.elapsed.total_seconds(), 2)}
    if r.status_code != 200 or "text/html" not in d["content_type"]:
        pages[url] = d; continue
    soup = BeautifulSoup(r.text, "lxml")
    t = soup.find("title"); d["title"] = t.get_text(strip=True) if t else ""
    md = soup.find("meta", attrs={"name": "description"})
    d["meta_description"] = (md.get("content") or "").strip() if md else ""
    mr = soup.find("meta", attrs={"name": "robots"})
    d["meta_robots"] = (mr.get("content") or "") if mr else ""
    can = soup.find("link", rel="canonical"); d["canonical"] = can.get("href", "") if can else ""
    d["h1"] = [h.get_text(" ", strip=True)[:120] for h in soup.find_all("h1")]
    types = []
    for sc in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string or "{}")
            for item in (data if isinstance(data, list) else [data]):
                if isinstance(item, dict):
                    ty = item.get("@type")
                    types += ty if isinstance(ty, list) else [ty] if ty else []
                    for g in (item.get("@graph") or []):
                        if isinstance(g, dict) and g.get("@type"): types.append(g["@type"])
        except Exception: pass
    d["jsonld_types"] = sorted({str(x) for x in types if x})
    body = soup.find("body")
    d["word_count"] = len((body.get_text(" ", strip=True) if body else "").split())
    for a in soup.find_all("a", href=True):
        tgt = norm(urljoin(url, a["href"]))
        if not tgt: continue
        edges.append((url, tgt, a.get_text(" ", strip=True)[:80]))
        if tgt not in seen and len(seen) < MAX_PAGES * 2:
            seen.add(tgt); q.append((tgt, depth + 1))
    pages[url] = d
    time.sleep(0.15)

# probe any sitemap URLs never linked (orphan candidates)
for u in list(sitemap)[:MAX_PAGES]:
    if u not in pages:
        try:
            r = S.get(u, timeout=25, allow_redirects=True)
            pages[u] = {"url": u, "depth": 99, "status": r.status_code,
                        "content_type": r.headers.get("content-type", ""),
                        "title": (BeautifulSoup(r.text, "lxml").find("title").get_text(strip=True)
                                  if r.status_code == 200 and "text/html" in r.headers.get("content-type", "") else ""),
                        "redirect_chain": [(h.status_code, h.url) for h in r.history],
                        "word_count": len(BeautifulSoup(r.text, "lxml").get_text(" ", strip=True).split())
                                      if r.status_code == 200 else 0}
        except Exception: pass

json.dump({"host": HOST, "canonical_host": CANON, "pages": list(pages.values()),
           "edges": edges, "sitemap": sorted(sitemap)},
          open(os.path.join(OUT, "crawl.json"), "w"))
print(f"{SLUG}: {len(pages)} pages, {len(edges)} edges, sitemap {len(sitemap)}")
