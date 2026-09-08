#!/usr/bin/env python3
"""Live verification for the Do-next board.

"Done" on the dashboard means LIVE-VERIFIED, never merely committed:
  (a) the site's latest Vercel production deploy is READY  (Vercel API, optional token), and
  (b) the change is confirmed on the live URL by fetching it:
        content   -> URL is 200 and the keyword / section is present
        technical -> the defect pages no longer show the defect (e.g. thin pages now >= 300 words)
        backlink  -> the placement URL is 200 and links to the site (dofollow unless noted)
Results are cached in live_verify.json (per task id / per ledger row) and consumed by v4_pages.py.

Vercel: set VERCEL_TOKEN (and VERCEL_TEAM_ID if the projects live in a team) in dash/.env.
Without a token the deploy step is *inferred* from the live fetch (200 = deployed) and BLOCKED
deploys cannot be detected — the board says so instead of guessing.
"""
import json, os, re, sys, datetime, html as H
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "live_verify.json")
UA = {"User-Agent": "Mozilla/5.0 (compatible; iptv-portfolio-verify/1.0; +https://iptv.alghostrader.com)"}
TODAY = datetime.date.today().isoformat()


def _env():
    p = os.path.join(BASE, "..", "dash", ".env")
    if os.path.exists(p):
        for line in open(p):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
_env()


def fetch(url, timeout=12):
    try:
        r = requests.get(url, headers=UA, timeout=timeout, allow_redirects=True)
        return r.status_code, r.text if "html" in (r.headers.get("content-type") or "") else "", r.url
    except Exception as e:
        return 0, "", url


def norm(s):
    s = (s or "").lower()
    for a, b in (("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("ç", "c"), ("ñ", "n"), ("ó", "o"), ("í", "i"),
                 ("á", "a"), ("ú", "u"), ("ł", "l"), ("ą", "a"), ("ę", "e"), ("ś", "s"), ("ż", "z"), ("ź", "z"),
                 ("ć", "c"), ("ń", "n"), ("ë", "e"), ("ü", "u"), ("ö", "o")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def page_text(html):
    try:
        soup = BeautifulSoup(html, "lxml")
        for t in soup(["script", "style", "noscript"]): t.decompose()
        return soup.get_text(" ", strip=True)
    except Exception:
        return re.sub(r"<[^>]+>", " ", html)


def keyword_present(html, kw):
    """True if all significant words of the keyword occur in the page text (order-free, accent-free)."""
    txt = norm(page_text(html))
    words = [w for w in norm(kw).split() if len(w) > 2]
    return bool(words) and all(w in txt for w in words)


def modified_after(html, date_iso):
    """True if the page declares a modified/published date >= date_iso (schema/OG/meta)."""
    dates = re.findall(r'(?:dateModified|datePublished|modified_time|published_time|lastmod)["\']?\s*[:=]\s*["\']?(\d{4}-\d{2}-\d{2})', html)
    return any(d >= date_iso for d in dates)


# ---------------- Vercel ----------------
def vercel_states(domains):
    """{domain: {state, url, inspector, at}} for the latest production deploy of each site.
    Requires VERCEL_TOKEN. Returns {} (and a reason) when unavailable."""
    tok = os.environ.get("VERCEL_TOKEN")
    if not tok:
        return {}, "no VERCEL_TOKEN in dash/.env — deploy state inferred from the live fetch"
    team = os.environ.get("VERCEL_TEAM_ID")
    out = {}
    try:
        url = "https://api.vercel.com/v9/projects?limit=100" + (f"&teamId={team}" if team else "")
        r = requests.get(url, headers={"Authorization": f"Bearer {tok}"}, timeout=20)
        if r.status_code != 200:
            return {}, f"Vercel API HTTP {r.status_code}"
        for p in r.json().get("projects", []):
            deps = p.get("latestDeployments") or []
            if not deps: continue
            d = deps[0]
            aliases = [a.lower() for a in (d.get("alias") or [])]
            for dom in domains:
                if any(dom in a for a in aliases) or dom.split(".")[0] in (p.get("name") or ""):
                    out[dom] = {"state": d.get("readyState") or d.get("state"), "url": d.get("url"),
                                "inspector": f'https://vercel.com/{(p.get("accountId") or "")}/{p.get("name")}/{d.get("id", "")}'.replace("//", "/").replace("https:/", "https://"),
                                "project": p.get("name"), "at": d.get("createdAt")}
        return out, f"Vercel API: {len(out)} of {len(domains)} sites matched"
    except Exception as e:
        return {}, f"Vercel API error: {str(e)[:80]}"


# ---------------- task checks ----------------
def check_content(t):
    """Content gap / decay / striking distance: URL 200 + keyword present (+ modified after completion for refreshes)."""
    url = t.get("target_url")
    if not url or url.endswith("(set the live URL)"):
        return dict(deployed=False, live=False, detail="no live URL yet — set it on the card, the next audit fetches it")
    st, html, final = fetch(url)
    if st != 200:
        return dict(deployed=False, live=False, http=st, detail=f"live URL returned HTTP {st or 'unreachable'}")
    kw = t.get("keyword") or ""
    if kw and not keyword_present(html, kw):
        return dict(deployed=True, live=False, http=200, detail=f"page is live but “{kw}” is not on it yet")
    # ENHANCE / refresh tasks: the keyword was already on the page before the work — proof of the change is a
    # modified date on/after the day the task was marked built (schema dateModified / og:updated_time / lastmod)
    if t.get("action") == "ENHANCE" or t.get("kind") in ("Content decay", "Striking distance", "CTR gap", "Rank recovery"):
        done = t.get("completed")
        if not done:
            return dict(deployed=True, live=False, http=200, detail="page is live; waiting for the completion date to compare the modified date")
        if not modified_after(html, done):
            has_any = bool(re.search(r"dateModified|modified_time|datePublished|lastmod", html))
            return dict(deployed=True, live=False, http=200,
                        detail=(f"page is live but its modified date is before {done}" if has_any else "page is live but declares no modified date — add dateModified / og:updated_time so the change can be verified"))
        return dict(deployed=True, live=True, http=200, detail=f"keyword present + modified on/after {done}")
    return dict(deployed=True, live=True, http=200, detail=("keyword present on the live page" if kw else "live URL responds 200"))


def check_thin(t, crawl_pages):
    """THIN PAGES: refetch the pages the crawl flagged (<300 words) and recount live."""
    urls = [p["url"] for p in crawl_pages if (p.get("word_count") or 0) < 300 and p.get("status") == 200][:8]
    if not urls:
        return dict(deployed=True, live=True, detail="no thin pages left in the crawl")
    still = []
    with ThreadPoolExecutor(6) as ex:
        for u, (st, html, _) in zip(urls, ex.map(fetch, urls)):
            if st == 200 and len(page_text(html).split()) < 300: still.append(u)
            elif st == 0: still.append(u)
    if still:
        return dict(deployed=True, live=False, detail=f"{len(still)} page(s) still under 300 words live: " + ", ".join(re.sub(r"https?://[^/]+", "", u) or "/" for u in still[:4]))
    return dict(deployed=True, live=True, detail=f"all {len(urls)} flagged pages now ≥300 words live")


def check_redirect(t, canon_host):
    dom = t["site"]
    try:
        r = requests.head(f"https://{'www.' + dom if not canon_host.startswith('www.') else dom}/", headers=UA, timeout=10, allow_redirects=False)
        ok = r.status_code in (301, 308)
        return dict(deployed=True, live=ok, http=r.status_code, detail=f"host redirect is {r.status_code}" + ("" if ok else " (needs 308)"))
    except Exception as e:
        return dict(deployed=False, live=False, detail=f"redirect check failed: {str(e)[:60]}")


def check_backlink(t):
    url = t.get("target_url")
    if not url:
        return dict(deployed=False, live=False, detail="no placement URL logged — tick it on Backlinks and paste the URL")
    st, html, _ = fetch(url)
    if st != 200:
        return dict(deployed=False, live=False, http=st, detail=f"placement URL returned HTTP {st or 'unreachable'}" + (" — DECAYED" if st in (404, 410) else ""))
    site = t["site"]
    soup = BeautifulSoup(html, "lxml")
    links = [a for a in soup.find_all("a", href=True) if site in a["href"]]
    if not links:
        return dict(deployed=True, live=False, http=200, detail=f"page is live but has no link to {site}")
    dofollow = any("nofollow" not in (a.get("rel") or []) for a in links)
    return dict(deployed=True, live=True, http=200, dofollow=dofollow,
                detail=f"link to {site} is live ({'dofollow' if dofollow else 'nofollow'})")


def verify_tasks(tasks, crawl_by_site, canon, vercel=None):
    """tasks: list of task dicts (Do-next model) that the owner marked built. Returns {id: result}."""
    vercel = vercel or {}
    out = {}
    for t in tasks:
        kind = t.get("kind") or t.get("type")
        if kind == "Backlink":
            r = check_backlink(t)
        elif kind == "Authority gap":
            n = t.get("new_links") or 0
            r = dict(deployed=n > 0, live=n > 0, detail=(f"{n} new live placement(s) logged for this site since completion" if n else "no new live placement logged for this site since completion (tick it on Backlinks with its URL)"))
        elif kind == "Technical fix":
            cat = (t.get("category") or "").upper()
            if "THIN" in cat: r = check_thin(t, crawl_by_site.get(t["site"], []))
            elif "REDIRECT" in cat: r = check_redirect(t, canon.get(t["site"], t["site"]))
            else: r = dict(deployed=bool(t.get("defect_gone")), live=bool(t.get("defect_gone")),
                           detail="defect gone from this audit's crawl" if t.get("defect_gone") else "defect still present in this audit's crawl")
        elif kind == "Indexation":
            ok = bool(t.get("indexed"))
            r = dict(deployed=ok, live=ok, detail="page(s) PASS in GSC URL Inspection" if ok else "still not indexed (URL Inspection)")
        else:
            r = check_content(t)
        v = vercel.get(t["site"])
        if v:
            r["vercel"] = v["state"]
            if v["state"] in ("BLOCKED", "ERROR", "CANCELED"):
                r["deployed"] = False; r["live"] = False; r["blocked"] = True
                r["detail"] = f"Vercel deploy {v['state']} — " + r.get("detail", "")
            elif v["state"] == "READY":
                r["deployed"] = True
        r["checked"] = TODAY
        out[t["id"]] = r
    return out


def load_cache():
    try: return json.load(open(CACHE))
    except Exception: return {"tasks": {}, "links": {}, "vercel": {}, "note": ""}


def save_cache(c):
    json.dump(c, open(CACHE, "w"), indent=1)


if __name__ == "__main__":
    # CLI: python3 live_verify.py <url> [keyword]  -> quick manual check
    if len(sys.argv) > 1:
        st, html, final = fetch(sys.argv[1])
        print(st, final, ("keyword present" if len(sys.argv) > 2 and keyword_present(html, sys.argv[2]) else ""), len(page_text(html).split()), "words")
