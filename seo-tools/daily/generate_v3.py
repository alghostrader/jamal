#!/usr/bin/env python3
"""IPTV portfolio SEO dashboard generator — multi-page static build.
Rebuilt 12 Aug 2026 after container recycle. Degrades gracefully when GSC is unavailable."""
import json, os, re as RE, math, html as H
from _sites import SITES, DOM2SLUG
CANON = {d: c for _, d, c in SITES}

STAMP = os.environ.get("DASH_STAMP", "")
BASE = os.path.dirname(os.path.abspath(__file__))
L = lambda n, d: (json.load(open(os.path.join(BASE, n))) if os.path.exists(os.path.join(BASE, n)) else d)
D = json.load(open(os.path.join(BASE, "..", "dash", "dash_data.json")))
F = L("audit_findings.json", {})
KT = L("keyword_targets.json", {})
CT = L("content.json", {})
SEM = L("semrush.json", {})
HIST = L("history.json", [])
CHECKED = set(L("checkbox_state.json", {}).get("checked", []))
PREV = L("prev_snapshot.json", None)
GOALS = L("goals.json", {"goals": []})
STYLE = open(os.path.join(BASE, "_styles.html")).read()

ALL = [d for _, d, _ in SITES]
NSITES = len(ALL)
SATELLITES = ["smartersprofrance.fr", "iptvfranceofficiel.fr", "abonnementiptvofficiel.com"]
SLUG = {s: s.replace(".com", "").replace(".", "-") for s in ALL}
ABBR = {"iptvesp.com": "esp", "primeiptv-france.com": "prime", "iptvned.com": "ned", "iptvpix.com": "pix",
        "smarters-live.com": "slive", "iptvshqiptar.com": "shqip", "smartersprofrance.fr": "spf",
        "iptvfranceofficiel.fr": "ifo", "abonnementiptvofficiel.com": "aio", "iptvsegura.com": "segura"}
LANG = {"iptvesp.com": ("Spanish", "es"), "primeiptv-france.com": ("French", "fr"), "iptvned.com": ("Dutch", "nl"),
        "iptvpix.com": ("French", "fr"), "smarters-live.com": ("French", "fr"), "iptvshqiptar.com": ("Albanian", "sq"),
        "smartersprofrance.fr": ("French", "fr"), "iptvfranceofficiel.fr": ("French", "fr"),
        "abonnementiptvofficiel.com": ("French", "fr"), "iptvsegura.com": ("Spanish", "es")}
MONEY = {"iptvesp.com": "/suscripciones", "primeiptv-france.com": "/abonnement", "iptvned.com": "/abonnementen",
         "iptvpix.com": "/abonnements", "smarters-live.com": "https://primeiptv-france.com/abonnement (funnel to the flagship)",
         "iptvshqiptar.com": "the subscription page", "smartersprofrance.fr": "/abonnement-iptv",
         "iptvfranceofficiel.fr": "/iptv-premium", "abonnementiptvofficiel.com": "/test-iptv", "iptvsegura.com": "/planes"}
CTRY = {"iptvesp.com": ("\U0001F1EA\U0001F1F8", "Spain"), "primeiptv-france.com": ("\U0001F1EB\U0001F1F7", "France"),
        "iptvpix.com": ("\U0001F1EB\U0001F1F7", "France"), "smarters-live.com": ("\U0001F1EB\U0001F1F7", "France"),
        "iptvned.com": ("\U0001F1F3\U0001F1F1", "Netherlands"), "iptvshqiptar.com": ("\U0001F1E6\U0001F1F1", "Albania"),
        "smartersprofrance.fr": ("\U0001F1EB\U0001F1F7", "France"), "iptvfranceofficiel.fr": ("\U0001F1EB\U0001F1F7", "France"),
        "abonnementiptvofficiel.com": ("\U0001F1EB\U0001F1F7", "France"), "iptvsegura.com": ("\U0001F1EA\U0001F1F8", "Spain")}
gen = D["generated"]
GSC_OFF = bool(D.get("gsc_unavailable"))
STAMP_TXT = STAMP or gen

dfs_of = lambda s: (D["sites"].get(s, {}).get("dfs", {}) or {})
def daily_of(s): return D["sites"].get(s, {}).get("daily", []) or []
# When DataForSEO is unreachable (no credit) positions can't be re-probed — label them honestly.
DFS_DOWN = all((D["sites"].get(s, {}).get("dfs") or {}).get("ref_domains") is None for s in D["sites"]) if D["sites"] else False
POS_SRC = ("positions from last probe 3 Sep — DFS paused, GSC cross-checked today" if DFS_DOWN
           else "live positions from this audit")
def nrank(s): return sum(1 for r in KT.get(s, []) if r.get("pos"))

# ---------------- icons ----------------
ICONS = {
 "home": '<path d="m3 10 9-7 9 7"/><path d="M5 9v11h14V9"/><path d="M9 20v-6h6v6"/>',
 "zap": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "trend": '<path d="M3 17 9 11l4 4 8-8"/><path d="M17 7h4v4"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
 "gem": '<path d="M6 3h12l3 6-9 12L3 9z"/><path d="M3 9h18"/>',
 "award": '<circle cx="12" cy="9" r="6"/><path d="m9 14-1.5 7L12 18l4.5 3L15 14"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/>',
 "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10c1 1 1.5 2 1.5 3h5c0-1 .5-2 1.5-3a6 6 0 0 0-4-10z"/>',
 "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
 "clipboard": '<rect x="8" y="3" width="8" height="4" rx="1"/><path d="M16 5h2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2"/>',
 "bell": '<path d="M6 9a6 6 0 0 1 12 0c0 5 2 6 2 6H4s2-1 2-6z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
 "refresh": '<path d="M21 12a9 9 0 1 1-2.6-6.4M21 4v5h-5"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "link": '<path d="M9 15 15 9"/><path d="M11 6.5 12.5 5a4 4 0 0 1 5.7 5.7l-1.5 1.5"/><path d="M13 17.5 11.5 19a4 4 0 0 1-5.7-5.7l1.5-1.5"/>',
 "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "warn": '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/>',
 "chart": '<path d="M3 3v18h18"/><path d="M8 17v-5M13 17V8M18 17v-8"/>',
 "ext": '<path d="M14 4h6v6"/><path d="M20 4 10 14"/><path d="M20 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h5"/>',
 "layers": '<path d="m12 2 9 5-9 5-9-5z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
}
def icon(n): return (f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
                     f'stroke-linecap="round" stroke-linejoin="round">{ICONS.get(n,"")}</svg>')
def ext(s): return (f'<a class="extlink" href="https://{s}/" target="_blank" rel="noopener" '
                    f'title="Open {s}" aria-label="Open {s}">{icon("ext")}</a>')
EMO = {"\U0001F3E0":"home","\U0001F680":"zap","\U0001F4C8":"trend","\U0001F30D":"globe","\U0001F4CA":"chart",
 "\U0001F48E":"gem","\U0001F3C6":"award","\U0001F3AF":"target","\U0001F4C4":"file","\U0001F4A1":"bulb",
 "✍️":"pen","✍":"pen","\U0001F4DD":"clipboard","\U0001F4CB":"clipboard","\U0001F6A8":"bell","\U0001F514":"bell",
 "\U0001F504":"refresh","\U0001F441️":"eye","\U0001F441":"eye","\U0001F517":"link"}
def flat(h):
    for e, n in EMO.items():
        if e in h: h = h.replace(e, icon(n))
    return h

def _spam_cls(v):
    v = v or 0
    return "good" if v < 40 else "ok" if v < 60 else "far"

def spark(vals, w=150, h=38, color="var(--t)"):
    vals = [v or 0 for v in vals]
    if len(vals) < 2 or max(vals) == 0:
        return (f'<svg class="spk" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
                f'<line x1="3" y1="{h//2}" x2="{w-3}" y2="{h//2}" stroke="var(--divider)" stroke-width="2" stroke-linecap="round"/></svg>')
    n = len(vals); mx = max(vals); pad = 4
    X = lambda i: pad + (w - 2*pad) * (i/(n-1))
    Y = lambda v: pad + (h - 2*pad) * (1 - v/mx)
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    return (f'<svg class="spk" width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
            f'<polygon points="{pad},{h-pad} {pts} {w-pad},{h-pad}" fill="{color}" opacity=".13"/>'
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
            f'<circle cx="{X(n-1):.1f}" cy="{Y(vals[-1]):.1f}" r="2.6" fill="{color}"/></svg>')

def donut(val, mx, center, label, color="var(--t)", r=30, sw=7):
    C = 2*math.pi*r; pct = 0 if not mx else max(0, min(1, val/mx)); off = C*(1-pct)
    size = (r+sw)*2+2; cx = size/2
    return (f'<div class="gauge"><svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<circle cx="{cx}" cy="{cx}" r="{r}" fill="none" stroke="var(--surface)" stroke-width="{sw}"/>'
            f'<circle class="gaugeArc" cx="{cx}" cy="{cx}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-dasharray="{C:.1f}" stroke-dashoffset="{off:.1f}"/>'
            f'<text class="gaugeC" x="{cx}" y="{cx+5}" text-anchor="middle">{center}</text></svg>'
            f'<span class="gaugeL">{label}</span></div>')

# ---------------- FIX PROMPTS ----------------
PROMPT_HEADER = """>>> TARGET WEBSITE: {site} <<<
Before writing any code, switch to the {site} project/repo in this workspace. Every path, route and commit below applies to THAT project only. Do NOT modify any other site in the portfolio.

You are a senior full-stack engineer fixing verified SEO items on {site} (Next.js on Vercel). Work through the numbered items in order. One commit per item: fix({slug}): <item> [daily-{date}]. After deploying each item run its verification. Do not touch robots.txt, canonicals, hreflang, existing redirects, or checkout noindex — they are verified correct.

"""

def kt_item(site, n):
    rows = KT.get(site, [])
    if not rows: return None
    def rk(r):
        p = r.get("pos")
        return f"currently #{p}" if p else "not in top 100"
    lines = "\n".join(f"     - \"{r['kw']}\" — {(str(format(r['vol'], ',')) + '/mo') if r.get('vol') else 'niche volume'} — {rk(r)}"
                      + (f" — OWNED BY {r['page']}: strengthen that page, never a parallel article" if r.get("page") else "")
                      for r in rows)
    lead = rows[0]
    return (f"""{n}. KEYWORD TARGETS (strategic — the money terms this site should own).
   Strengthen one page per term, biggest volume first. Primary: \"{lead['kw']}\" ({(format(lead['vol'], ',') + '/mo') if lead.get('vol') else 'niche volume'}).
{lines}
   Rules: one strong page per term (title + H1 keyword-first, 700+ words, schema, 2+ internal links in); never spin up a second page for a term that already has one; re-check positions after the next audit.""")

def tech_items(site):
    f = F.get(site, {}); p = []
    over = f.get("titles_over60", [])
    if over:
        p.append(f"""{len(p)+1}. TITLES (P1). {len(over)} page(s) exceed 60 characters: {'; '.join(f'{u} ({n})' for n,u in over)}.
   Rewrite keyword-first to <= 60 chars including the template suffix; deploy; verify by crawl.""")
    rl = f.get("redirect_links", [])
    if rl:
        p.append(f"""{len(p)+1}. LINK HYGIENE (P2). {len(rl)} internal link target(s) route through redirects: {', '.join(rl[:8])}.
   Point the hrefs at the final URLs; verify zero 3xx internal link targets.""")
    if f.get("linked404"):
        p.append(f"""{len(p)+1}. BROKEN LINKS (P1). Internal links point at 404s: {', '.join(list(f['linked404'])[:8])}.
   Repoint or remove them; verify zero linked 404s by crawl.""")
    if f.get("orphans"):
        p.append(f"""{len(p)+1}. ORPHANS (P2). In sitemap but not internally linked: {', '.join(f['orphans'][:8])}.
   Add >= 2 contextual internal links to each from relevant pages.""")
    if str(f.get("www_redirect", "")).startswith("307") or str(f.get("apex", "")).startswith("307"):
        p.append(f"""{len(p)+1}. REDIRECT (P1). A host redirect is 307 (temporary). In Vercel -> Settings -> Domains set it to permanent (308). Verify with curl -sI.""")
    if f.get("favicon") not in (200, None):
        p.append(f"""{len(p)+1}. FAVICON (P2). /favicon.ico returns {f.get('favicon')}. Ship a real favicon.ico in public/. Verify 200.""")
    thin = f.get("thin", [])
    if len(thin) > 2:
        p.append(f"""{len(p)+1}. THIN PAGES (P2). {len(thin)} page(s) under 300 words: {', '.join(thin[:6])}.
   Expand each to answer its query properly, or consolidate/noindex if they serve no search intent.""")
    return p

LANE = {
 "iptvesp.com": "Spanish market: listas/telegram cluster + the money page. Do not target French or Dutch terms.",
 "primeiptv-france.com": "FR flagship: head terms (abonnement iptv, iptv france, meilleur iptv) belong HERE. All FR outreach links point here.",
 "iptvned.com": "Dutch market: kopen/aanbieders + the legal-B2B cluster.",
 "iptvpix.com": "FR content/recovery: guides and explainers. No restructuring while the recovery runs.",
 "smarters-live.com": "The app hub: application iptv / iptv smarters pro / device guides. Sale funnels to primeiptv.",
 "iptvshqiptar.com": "Albanian market only: iptv shqip / shqiptare / shqiptar.",
 "smartersprofrance.fr": "Satellite: iptv smarters install & configuration long-tail ONLY. Never generic app or abonnement terms.",
 "iptvfranceofficiel.fr": "Satellite: iptv premium / HDR quality angle. Head terms stay with the flagship.",
 "abonnementiptvofficiel.com": "Satellite: trial & deal intent (test, essai, pas cher) + boitier hardware.",
 "iptvsegura.com": "ES safety/trust lane: es-seguro, estafas, legalidad, riesgos angles + guides, funnel to /planes. NEVER the ES head terms or the telegram LISTS cluster (iptvesp owns those) — the riesgos angle only.",
}

def site_prompt(site):
    p = tech_items(site)
    if site == "abonnementiptvofficiel.com":
        ranked = [r for r in KT.get(site, []) if r.get("pos")]
        if ranked:
            p.append(f"""{len(p)+1}. PROTECT LIVE RANKINGS (P0). Live-verified: {', '.join(f'"{r["kw"]}" #{r["pos"]}' for r in ranked)}.
   Do not restructure, retitle or change slugs/canonicals on the ranking pages. Support them from AROUND: 2-3 internal links in from blog posts with natural anchors, and freshness on the LINKING posts.""")
        else:
            p.append(f"""{len(p)+1}. RANKING WATCH (P0 — DO NOT TOUCH the money pages). /test-iptv and /boitier-iptv were re-evaluating after the 1 Aug rewrite. Keep them frozen; support with internal links only. Positions are re-probed every audit.""")
    if site == "iptvpix.com":
        p.append(f"""{len(p)+1}. RECOVERY — keep going, don't restructure. DataForSEO now reports a Domain Rank of {dfs_of(site).get('domain_rank')} (the only measurable one in the portfolio) and Semrush lists the domain again after a full absence.
   Steps: (a) in GSC -> Pages, strengthen anything still 'Crawled – currently not indexed' (unique intro + 2 internal links in), then Request Indexing; (b) keep adding internal links from the strongest pages; (c) no slug, canonical or architecture changes while the recovery runs.""")
    if not p:
        p.append("1. NOTHING OPEN ON THE TECH SIDE. Crawl is clean: titles, internal links, orphans, canonicals, redirects and favicon all verified today. Do not invent work here — spend the cycle on content and links instead.")
    kt = kt_item(site, len(p)+1)
    if kt: p.append(kt)
    p.append(f"""{len(p)+1}. LANE DISCIPLINE (anti-cannibalization, portfolio rule). {LANE[site]}
   Before creating ANY new page, search this repo for an existing page targeting the same intent. If one exists, strengthen it instead. One keyword -> one page -> one site.""")
    return PROMPT_HEADER.format(site=site, slug=site.split(".")[0], date=gen) + "\n\n".join(p)

prompts = {s: site_prompt(s) for s in ALL}

# ---------------- article prompts (with market reservation) ----------------
MK = lambda s: LANG[s][1]
CONTENT_PRIO = ["smarters-live.com", "primeiptv-france.com", "iptvesp.com", "iptvned.com", "iptvpix.com",
                "abonnementiptvofficiel.com", "iptvfranceofficiel.fr", "smartersprofrance.fr", "iptvshqiptar.com", "iptvsegura.com"]
RESERVED = {}
for _s in SATELLITES + [x for x in ALL if x not in SATELLITES]:
    for _r in KT.get(_s, []):
        RESERVED.setdefault((MK(_s), _r["kw"]), _s)
for _s in sorted(ALL, key=lambda x: CONTENT_PRIO.index(x) if x in CONTENT_PRIO else 99):
    for _r in CT.get(_s, {}).get("recommend", []):
        if not _r["covered"]:
            RESERVED.setdefault((MK(_s), _r["kw"]), _s)
def reserved_for(s, kw): return RESERVED.get((MK(s), kw)) in (None, s)

def next_article_prompt(s):
    c = CT.get(s, {}); rec = c.get("recommend", [])
    gap = next((r for r in rec if not r["covered"] and reserved_for(s, r["kw"])), None)
    if not gap: return None
    lang, _ = LANG[s]; money = MONEY[s]
    existing = ", ".join(a["path"] for a in c.get("articles", [])[:4]) or "(none crawled)"
    vol = f"{gap['vol']:,}/mo" if gap["vol"] else "low volume but on-intent"
    return (f""">>> TARGET WEBSITE: {s} <<<
Before writing, switch to the {s} project/repo in this workspace. Publish only on {s}.

You are an expert {lang} SEO copywriter for {s} (IPTV service, Next.js on Vercel). Write ONE new
article in {lang} targeting: "{gap['kw']}" (search volume {vol}).

STEP 0 — ANTI-CANNIBALIZATION CHECK (do this FIRST): search this repo's pages/blog for an existing
article targeting "{gap['kw']}" (search slugs and titles for its distinctive tokens). If one exists:
STOP — report the URL and, at most, strengthen it. Only proceed if genuinely absent.

REQUIREMENTS:
1. Write entirely in {lang} — native tone, not translated.
2. Title <= 60 chars, keyword-first, includes "{gap['kw']}". H1 matches.
3. Answer the real intent behind "{gap['kw']}" (how-to / comparison / troubleshooting as fits). Specific and current (2026).
4. 1,200-1,800 words: intro that answers up front + 5-7 H2 sections + a short FAQ.
5. Internal links: once to the subscription page ({money}) with a natural anchor, plus 2-3 of these
   related articles where relevant: {existing}.
6. Net-new angle — must not duplicate an existing article's angle.
7. SEO: unique meta description <= 160 chars; Article + FAQPage JSON-LD; descriptive alt text; one clear CTA.
8. Structure it so AI engines can cite it: numbered steps, direct answers, a specification/comparison table
   where it fits. ChatGPT already cites this portfolio — that is a real traffic channel.
9. Honest and compliant: licensed-use framing, no piracy claims, no channel or brand trademarks.

Deliver as a ready-to-publish page in the site's blog structure, add it to sitemap.xml, then verify the
live URL returns 200 with the rendered title <= 60 chars. Commit: feat(blog): {gap['kw']} article.""")

# ---------------- recommendations ----------------
def _recs():
    R = {s: [] for s in ALL}
    for s in ALL:
        f = F.get(s, {}); dfs = dfs_of(s); sm = SEM.get(s) or {}
        rd = dfs.get("ref_domains")
        if f.get("titles_over60"): R[s].append(("OPEN", f"{len(f['titles_over60'])} title(s) over 60 chars"))
        if f.get("redirect_links"): R[s].append(("OPEN", f"{len(f['redirect_links'])} internal link(s) via redirect"))
        if f.get("linked404"): R[s].append(("OPEN", f"{len(f['linked404'])} internal link(s) to 404"))
        if rd is not None and rd <= 5:
            R[s].append(("P0", f"Only {rd} referring domains — links are the ceiling for this site"))
        nr = nrank(s)
        if nr: R[s].append(("KPI", f"{nr} keyword target(s) ranking in the top 100 — protect and push"))
    R["iptvesp.com"].append(("DO", "Add a conversion module (pricing + CTA) inside the Telegram post — it holds most of the traffic"))
    R["primeiptv-france.com"].append(("P0", "Concentrate French content, links and cross-references here — it is the flagship"))
    R["iptvned.com"].append(("DO", "Interlink the legal-B2B posts with the legal landing — the replacement play for the faded news query"))
    R["iptvpix.com"].append(("WATCH", "Recovery: Domain Rank measurable + back in Semrush. No restructuring; keep adding internal links"))
    R["smarters-live.com"].append(("DO", "'iptv smarters pro' (49,500/mo) hub + tools are LIVE — now rank them: internal links + referring domains"))
    R["iptvshqiptar.com"].append(("KPI", "First live rankings landed — keep publishing core Albanian content + light link tier"))
    R["smartersprofrance.fr"].append(("DO", "Install library + configuration hub live; first ranked keywords appearing — keep to install/config lane"))
    R["iptvfranceofficiel.fr"].append(("DO", "Retitle /application-iptv off the head term (smarters-live owns that lane); premium/HDR content only"))
    R["abonnementiptvofficiel.com"].append(("P0", "Money pages FROZEN while positions re-evaluate — support with internal links only"))
    return R
RECS = _recs()

# ---------------- alerts ----------------
def alerts():
    A = []
    prev = HIST[-2] if len(HIST) >= 2 else None
    # DataForSEO outage: when the account has no credit every DFS field comes back None.
    # Surface one loud alert instead of letting "—" cells pass silently, and keep the
    # open aio spam watch visible (it cannot be re-checked while DFS is down).
    if all(dfs_of(s).get("ref_domains") is None for s in ALL):
        A.append(("crit", "DataForSEO account is OUT OF CREDIT (balance −$0.07) — live SERP probes, DFS authority "
                          "and search volumes are paused. Keyword positions shown are from the last successful probe "
                          "(3 Sep), cross-checked against GSC today. Top up at app.dataforseo.com, then rerun the audit. "
                          "The aio spam-score watch (48→58) stays open — it cannot be re-checked until then."))
    # Rank-loss annotations: when GSC (Google's own report) contradicts a probe-based
    # loss, the owner-side evidence wins and the alert is downgraded to a watch.
    # A None value = suppress silently, no alert at all (verdict settled, owner informed).
    # esp "iptv españa": resolved 15 Aug as a false alarm — probes recorded a datacenter-only
    # #4 that GSC shows real users never saw (~0 impressions, avg pos 42-68 all August);
    # nothing user-facing was lost. Do not re-alert on this keyword's probe churn.
    RANK_NOTES = {
        ("iptvesp.com", "iptv españa"): None,
    }
    rank_alerted = set()
    if PREV:
        for s in ALL:
            pa = PREV.get("sites", {}).get(s, {}).get("positions", {})
            for r in KT.get(s, []):
                op, np = pa.get(r["kw"]), r.get("pos")
                if op is not None and op <= 10 and np is None:
                    rank_alerted.add((s, r["kw"]))
                    if (s, r["kw"]) in RANK_NOTES:
                        note = RANK_NOTES[(s, r["kw"])]
                        if note:
                            A.append(("warn", f'{s}: "{r["kw"]}" no longer found in probe top 100 (probes said #{op}). {note}'))
                        # None → settled false alarm, suppress silently
                    else:
                        A.append(("crit", f'{s}: "{r["kw"]}" fell out of the top 100 (was #{op}) — twice-confirmed in live SERPs. '
                                          f'Before treating as real: cross-check GSC impressions/position for the exact query '
                                          f'(probe positions can be datacenter artifacts). No panic-edits.'))
    # Standing watches: annotated keywords with a visible note stay on the dashboard while
    # probes still find nothing, even after the diff baseline moved past the original drop.
    for (s, kw), note in RANK_NOTES.items():
        if (s, kw) in rank_alerted or not note: continue
        cur = next((r.get("pos") for r in KT.get(s, []) if r["kw"] == kw), "absent")
        if cur is None:
            A.append(("warn", f'{s}: "{kw}" — probe top 100: absent. {note}'))
    for s in ALL:
        f = F.get(s, {}); dfs = dfs_of(s); sm = SEM.get(s) or {}
        rd, sp = dfs.get("ref_domains"), dfs.get("spam_score")
        if f.get("titles_over60"): A.append(("warn", f"{s}: {len(f['titles_over60'])} title(s) over 60 chars — rewrite keyword-first"))
        if f.get("redirect_links"): A.append(("warn", f"{s}: {len(f['redirect_links'])} internal link(s) route via redirects"))
        if f.get("linked404"): A.append(("crit", f"{s}: internal links point to 404 pages — repoint them"))
        if f.get("orphans"): A.append(("warn", f"{s}: {len(f['orphans'])} orphan page(s) — add internal links"))
        if str(f.get("www_redirect", "")).startswith("307") or str(f.get("apex", "")).startswith("307"):
            A.append(("warn", f"{s}: host redirect is 307 — set it to 308 (permanent)"))
        canon_www = CANON.get(s, s).startswith("www.")
        www_status = str(f.get("www_redirect", ""))
        apex_status = str(f.get("apex", ""))
        if canon_www:
            # correct setup: apex 308 -> www, www serves 200
            if apex_status == "200":
                A.append(("warn", f"{s}: apex serves 200 but the canonical host is www — set a 308 apex→www redirect (duplicate-host risk)"))
        else:
            if www_status == "200":
                A.append(("warn", f"{s}: www serves 200 but the canonical host is the apex — set a 308 www→apex redirect (duplicate-host risk)"))
        if not GSC_OFF and not D["sites"].get(s, {}).get("in_gsc"):
            A.append(("crit", f"{s} is NOT in Search Console (verified via sites.list) — add the sc-domain property, "
                              f"submit sitemap.xml, and add the monitoring service account as a user. "
                              f"Until then the dashboard cannot track its traffic."))
        if f.get("favicon") not in (200, None): A.append(("warn", f"{s}: /favicon.ico returns {f.get('favicon')}"))
        if rd is not None and rd <= 5:
            A.append(("warn", f"{s}: only {rd} referring domains — authority is the ceiling; run the Backlinks steps"))
        sp_hist = [h["sites"].get(s, {}).get("spam_score") for h in HIST if s in h.get("sites", {})]
        sp_hist = [x for x in sp_hist if x is not None]
        if sp is not None and sp_hist and sp - sp_hist[0] >= 4:
            A.append(("warn", f"{s}: spam score jumped {sp_hist[0]}→{sp} (+{sp - sp_hist[0]}) — pause this site's tier-2 link work and review the newest links"))
        # note: a high-but-stable score is third-party bot spam (identical domains portfolio-wide);
        # Google discounts it, sc-domain properties can't disavow, and it is NOT from our outreach — no alert.
        if prev:
            p = prev.get("sites", {}).get(s, {})
            if p.get("ref_domains") is not None and rd is not None and rd > p["ref_domains"]:
                A.append(("good", f"{s}: referring domains {p['ref_domains']}→{rd} — authority building ✓"))
    if GSC_OFF:
        A.insert(0, ("crit", "Search Console traffic is PAUSED — the service-account key was lost when the container recycled. "
                             "Re-upload gsc/sa.json (or re-share the key) to restore clicks/impressions history."))
    seen = set(); out = []
    for lv, t in A:
        if t not in seen: seen.add(t); out.append((lv, t))
    return sorted(out, key=lambda x: {"crit": 0, "warn": 1, "good": 2}.get(x[0], 3))

def alerts_card():
    A = alerts()
    if not A:
        return f'<div class="card"><h2>{icon("bell")} Urgent — fix now</h2><p class="sub" style="margin:0">Nothing urgent. ✓</p></div>'
    lbl = {"crit": "URGENT", "warn": "FIX", "good": "WIN"}
    ico = {"crit": icon("warn"), "warn": icon("warn"), "good": icon("check")}
    items = "".join(f'<div class="alert {lv}"><span class="ai">{ico[lv]}</span>'
                    f'<span><b>{lbl[lv]}</b> · {H.escape(t)}</span></div>' for lv, t in A)
    nfix = sum(1 for lv, _ in A if lv in ("crit", "warn"))
    cls = "card alertcard" if any(lv == "crit" for lv, _ in A) else "card"
    return (f'<div class="{cls}"><h2>{icon("bell")} Urgent — fix now '
            f'<span style="font-weight:400;color:var(--n600)">· {nfix} to fix</span></h2>{items}</div>')

# ---------------- daily queue ----------------
PLATFORM_BATCH = f""">>> LINK PLATFORM BATCH — [PLATFORM NAME] × all {NSITES} websites <<<
(You have Chrome access. Owner does ONLY two things: account creation/login and the final publish click.)

Work through all {NSITES} sites, one at a time, on [PLATFORM NAME]:
{' · '.join(ALL)}

For EACH site, in Chrome:
1. Open the platform's profile/page creation flow.
2. Prepare EVERYTHING yourself: brand name, URL (https://<site>/), a one-sentence description in the
   site's language (consistent for that site everywhere), category, country; grab a logo/screenshot if needed.
3. STOP only at account creation/login and the final publish click — say "ready", wait, then continue.
4. Log every created profile URL in a running table.

RULES: identical name/URL/description per site across platforms · brand or naked-URL anchors ONLY, never
money keywords · skip anything demanding real business documents or verification · if the platform
moderates IPTV brands, note it, skip, move on · report the URL table when done."""

WEB20_GENERIC = """>>> WEB 2.0 POST — [WEBSITE] on [PLATFORM] <<<
(Rotate: Overblog / Canalblog / WordPress.com / Blogger / Tumblr / Medium / Substack.)

Write ONE original article in [WEBSITE]'s language, 900-1,100 words, for the Web 2.0 blog (NOT the site).
Topic: an angle NOT already covered on [WEBSITE] — device walk-through, troubleshooting, cost comparison.

RULES:
1. 100% original — never copied from the site or another Web 2.0 post.
2. Exactly ONE contextual link to https://[WEBSITE]/ — anchor = brand name or naked URL, never a money keyword.
3. 1-2 internal links to other posts on the same Web 2.0 blog if they exist.
4. Helpful, specific, 2026-current; licensed-use framing; no piracy claims; no trademarks.
5. Cap 3-5 posts per month per site — check the log before publishing."""

SOS_PITCH = """JOURNALIST PITCH TEMPLATE — Source of Sources / Featured / Qwoted
(Identity: streaming-technology & cord-cutting cost expert. NEVER "IPTV subscription seller".)

SUBJECT: Re: [their query title]

Hi [first name],

[1 sentence that directly answers their question — the quotable line.]

[2-3 sentences of substance: a number, a country comparison, or a practical tip.]

If useful, we maintain a free device-compatibility checker and a bandwidth calculator, free to cite: [tool URL].

Credentials: [name], founder of [brand] ([site]), a licensed-content IPTV service operating in
Spain/France/Netherlands. Happy to expand before your deadline.

RULES: only reply when genuinely on-topic · answer within hours · 2-3 pitches/week max · plain text."""

OUTREACH_TPL = """RECLAIM & LISTICLE OUTREACH TEMPLATES (weekly, 5 emails max)

A) UNLINKED MENTION →
Subject: Thanks for mentioning [brand]
Hi [name] — saw you mentioned [brand] in [article URL]. Thanks! Would you mind linking the mention to
https://[site]/ so your readers can find it? Happy to return the favour with a quote or data. — [name]

B) LISTICLE ("best IPTV apps / meilleur IPTV / beste IPTV" pages ranking top-20) →
Subject: Addition for your [title] list
Hi [name] — nice roundup. One gap: [specific missing thing]. We built a free [device-compatibility checker /
bandwidth calculator] your readers might use: [tool URL]. Either way, one factual correction: [tiny correction]. — [name]

C) BROKEN LINK →
Subject: Dead link in [article]
Hi [name] — the link to [dead URL] in [article] returns 404. We keep a live equivalent here: [our URL]. — [name]"""


def role_header(emoji, role, who, count, cls=""):
    return (f'<div class="rolehead {cls}"><span class="roleemoji">{emoji}</span>'
            f'<div><h2 style="margin:0">{role}</h2><span class="rolesub">{who}</span></div>'
            f'<span class="rolecount">{count} task(s)</span></div>')

def prompt_card(title, text, note=""):
    return (f'<div class="card pcard"><div class="phead"><h2>{icon("clipboard")} {title}</h2>'
            f'<button class="copybtn" data-copy>Copy prompt</button></div>'
            + (f'<p class="sub">{note}</p>' if note else "")
            + f'<pre class="ptext">{H.escape(text)}</pre></div>')

def build_work():
    cols = []
    dev = [(s, prompts[s]) for s in ALL if tech_items(s)]
    dev_cards = "".join(
        f'<div class="task"><div class="meta"><span class="tag warn">FIX</span> {s}</div>'
        f'<div style="font-size:14px;line-height:1.4">{H.escape(tech_items(s)[0].split(chr(10))[0][:110])}</div>'
        f'<div class="pcard" style="margin:0"><details><summary class="linkbtn" style="cursor:pointer">Show prompt</summary>'
        f'<pre class="ptext">{H.escape(p)}</pre></details>'
        f'<div style="margin-top:8px"><button class="btn sm" data-copy>Copy prompt</button></div></div></div>'
        for s, p in dev) or '<div class="task"><div style="font-size:14px;color:var(--n600)">Nothing — zero defects. ✓</div></div>'
    cols.append(("Developer", len(dev), dev_cards))
    cands = []
    for s in CONTENT_PRIO:
        rec = CT.get(s, {}).get("recommend", [])
        gp = next((r for r in rec if not r["covered"] and reserved_for(s, r["kw"])), None)
        if gp: cands.append((gp["vol"] or 0, s, gp))
    cands.sort(reverse=True, key=lambda x: x[0])
    cont_cards = ""
    if cands:
        _, s, gp = cands[0]
        vol = f"{gp['vol']:,}/mo" if gp["vol"] else "niche"
        seq = (f'Write today\u2019s article with the 5-skill pipeline. Site: {s}. Brief: seo-tools/briefs/{DOM2SLUG[s]}/site-brief.md\n\n'
               f'1. /keyword-fanout-map  "{gp["kw"]}"  \u2014 {CTRY[s][1]}, {LANG[s][0]}\n'
               f'2. /seo-content-writer \u2014 check no same-market duplicate first; STOP if one exists\n'
               f'3. /onpage-optimizer \u2014 on the draft\n4. /internal-link-architect \u2014 money page {MONEY[s]} first\n'
               f'5. Publish + sitemap + request indexing.')
        cont_cards = (f'<div class="task"><div class="meta"><span class="tag pos">WRITE</span> {s}</div>'
                      f'<div style="font-size:14px">\u201c{H.escape(gp["kw"])}\u201d \u2014 {vol}. Today\u2019s one article.</div>'
                      f'<div class="pcard" style="margin:0"><details><summary class="linkbtn" style="cursor:pointer">Show workflow</summary>'
                      f'<pre class="ptext">{H.escape(seq)}</pre></details>'
                      f'<div style="margin-top:8px"><button class="btn sm" data-copy>Copy prompt</button></div></div></div>')
        for _, s2, gp2 in cands[1:4]:
            v2 = f"{gp2['vol']:,}/mo" if gp2["vol"] else "niche"
            cont_cards += (f'<div class="task" style="opacity:.75"><div class="meta"><span class="tag neu">QUEUED</span> {s2}</div>'
                           f'<div style="font-size:13px">\u201c{H.escape(gp2["kw"])}\u201d \u2014 {v2}</div></div>')
    cols.append(("Content", 1, cont_cards))
    link_cards = (f'<div class="task"><div class="meta"><span class="tag neu">LINKS</span> all {NSITES} sites</div>'
                  f'<div style="font-size:14px">One platform row on the <a class="slink" href="links">Backlinks matrix</a>. 30 minutes \u2014 the #1 lever.</div>'
                  f'<div class="pcard" style="margin:0"><details><summary class="linkbtn" style="cursor:pointer">Show batch prompt</summary>'
                  f'<pre class="ptext">{H.escape(PLATFORM_BATCH)}</pre></details>'
                  f'<div style="margin-top:8px"><button class="btn sm" data-copy>Copy prompt</button></div></div></div>')
    cols.append(("Links", 1, link_cards))
    owner = []
    if not D["sites"].get("iptvsegura.com", {}).get("in_gsc"):
        owner.append("iptvsegura: add the monitoring service account in Search Console (Restricted)")
    owner.append("Weekly: send Claude the sales numbers per site")
    owner.append("Review the \u26a0\ufe0f fields in seo-tools/briefs/")
    own_cards = "".join(f'<div class="task"><div class="meta"><span class="tag neu">OWNER</span></div>'
                        f'<div style="font-size:14px">{t}</div></div>' for t in owner)
    cols.append(("Owner", len(owner), own_cards))
    total = sum(n for _, n, _ in cols)
    hdr = (f'<div class="hdr"><div><h1>Work \u2014 {total} tasks</h1>'
           f'<p class="sub">Organised by role. Tasks auto-clear when the next audit verifies them done.</p></div></div>')
    kan = "".join(f'<div><h3>{r} <span class="cnt">{n}</span></h3>{cardshtml}</div>' for r, n, cardshtml in cols)
    return hdr + f'<div class="kanban">{kan}</div>'

def daily_plan():
    cards = []; n = 0
    def pcard(num, title, text, note=""):
        return (f'<div class="card pcard"><div class="phead"><h2>{icon("clipboard")} Step {num} · {title}</h2>'
                f'<button class="copybtn" data-copy>Copy prompt</button></div>'
                + (f'<p class="sub">{note}</p>' if note else "")
                + f'<pre class="ptext">{H.escape(text)}</pre></div>')
    def infocard(num, title, inner):
        return f'<div class="card"><h2>{icon("check")} Step {num} · {title}</h2>{inner}</div>'

    owner = []
    if GSC_OFF:
        owner.append("RESTORE SEARCH CONSOLE ACCESS — the monitoring service-account key was lost when the workspace "
                     "recycled. Re-share the gsc/sa.json key (or create a new service account and grant it read access "
                     "to all portfolio properties). Until then the dashboard has no clicks/impressions data.")
    owner.append("iptvpix.com — GSC → Pages: how many 'Crawled – currently not indexed' remain? (weekly recovery check)")
    owner.append("Request indexing for any article published since the last audit")
    owner.append("NEW: review the 9 site-briefs at seo-tools/briefs/ — confirm the ⚠️ fields (competitors, price "
                 "positioning, CTA wording, author identity). The content skills read these files as law.")
    n += 1
    cards.append(infocard(n, "Owner tasks — you, in the browser",
        '<ul class="lcl" style="margin-top:8px">' + "".join(f"<li>{H.escape(t)}</li>" for t in owner) + "</ul>"))

    # open technical work, only where real
    for s in ALL:
        if tech_items(s):
            n += 1
            cards.append(pcard(n, f"Technical — {s}", prompts[s],
                note="Crawl-verified open items on this site. This step disappears once the next audit confirms them fixed."))

    # content: one article, biggest reserved gap
    cands = []
    for s in CONTENT_PRIO:
        rec = CT.get(s, {}).get("recommend", [])
        g = next((r for r in rec if not r["covered"] and reserved_for(s, r["kw"])), None)
        if g: cands.append((g["vol"] or 0, s, g))
    if cands:
        cands.sort(reverse=True, key=lambda x: x[0])
        _, s, g = cands[0]
        nap = next_article_prompt(s)
        if nap:
            n += 1
            cards.append(pcard(n, f"Content — one article on {s}", nap,
                note=f'Target: "{g["kw"]}" ({g["vol"]:,}/mo) — the biggest genuinely-uncovered gap in the portfolio. '
                     f'<b>Preferred path:</b> the 5-skill pipeline on the <a class="slink" href="{SLUG[s]}">{s}</a> page '
                     f'(brief-driven, anti-cannibalization built in). This one-shot prompt is the no-skills fallback.'))

    n += 1
    cards.append(pcard(n, f"Links — next platform batch (all {NSITES} sites)", PLATFORM_BATCH,
        note='Open <a class="slink" href="links">Backlinks</a>, take the topmost row that is not complete and not '
             '⏳ rate-limited, put its name into [PLATFORM NAME], run the batch, tick the boxes, then Copy progress.'))

    howto = ('<div class="card"><p class="sub" style="margin:0">'
             '<b>How it works:</b> run the steps top to bottom, one copy-paste at a time — each prompt names its target website. '
             'Done? Say <b>"update the dashboard"</b> and I re-audit, verify, and rebuild the queue. '
             'Not a step here = not today\'s job.</p></div>')
    return "".join(cards) + howto

TODAY_HTML = daily_plan()
_steps = RE.findall(r"Step (\d+) · ([^<]+)", TODAY_HTML)

# ---------------- shell ----------------
def sidebar(cur):
    top = [("./", "home", "Portfolio", None), ("today", "zap", "Work", "today"),
           ("trends", "trend", "Trends", "trends"), ("links", "link", "Backlinks", "links"),
           ("plan", "file", "Plan", "plan"), ("sales", "gem", "Sales", "sales")]
    nav = "".join(f'<a class="navitem{" on" if cur==k else ""}" href="{h}"><span class="navicon">{icon(i)}</span>{l}</a>'
                  for h, i, l, k in top)
    sites = "".join(f'<a class="navitem site{" on" if cur==s else ""}" href="{SLUG[s]}">'
                    f'<span class="dot s{i+1}"></span>{s.replace(".com","")}</a>' for i, s in enumerate(ALL))
    mark = '<svg class="ic" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2l8 10-8 10-8-10z"/></svg>'
    return (f'<aside class="side"><a class="brand" href="./"><span class="brandmark">{mark}</span><span>IPTV<b>SEO</b></span></a>'
            f'<nav class="nav">{nav}<div class="navsec">Sites</div>{sites}</nav>'
            f'<div class="sidefoot">Updated<br>{H.escape(STAMP_TXT)}</div></aside>')

HEAD_META = ('<meta name="viewport" content="width=device-width, initial-scale=1">'
             '<meta name="robots" content="noindex, nofollow">'
             '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 '
             'viewBox=%220 0 24 24%22%3E%3Cpath fill=%22%23cc785c%22 d=%22M12 2l8 10-8 10-8-10z%22/%3E%3C/svg%3E">')

def topbar(cur):
    NAV = [("./", "Overview", None), ("today", "Work", "today"), ("trends", "Trends", "trends"),
           ("links", "Backlinks", "links"), ("plan", "Plan", "plan"), ("sales", "Sales", "sales"),
           ("replies", "Replies", "replies"), ("settings", "Settings", "settings")]
    pills = "".join(f'<a href="{h}" class="{"on" if cur == k else ""}">{l}</a>' for h, l, k in NAV)
    chips = "".join(f'<a class="schip{" on" if cur == s else ""}" href="{SLUG[s]}">'
                    f'<span class="dot s{i+1}"></span>{ABBR[s]}</a>' for i, s in enumerate(ALL))
    return (f'<header class="topbar"><div class="tb1">'
            f'<a class="brand" href="./"><span class="brandmark">i</span>'
            f'<span class="wordmark">IPTV <b>Portfolio</b></span></a>'
            f'<nav class="navpills">{pills}</nav><span class="tbspacer"></span>'
            f'<span class="auditstat">Audit {H.escape(STAMP_TXT)}</span>'
            f'<button class="runbtn" id="runaudit" title="Copies the audit request — paste it to Claude">Run audit</button>'
            f'</div><div class="tb2"><span class="lbl">Sites</span>{chips}</div></header>')

RUN_JS = """<script>
const rb = document.getElementById("runaudit");
if (rb) rb.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText("Full audit and update the dashboard please"); } catch(e){}
  rb.textContent = "Copied — paste to Claude"; setTimeout(() => rb.textContent = "Run audit", 2600);
});
</script>"""

def shell(title, body, cur=None, extra_js=""):
    return f'''<title>{title}</title>
{HEAD_META}
{STYLE}
<div class="viz-root">
{topbar(cur)}
<main><div class="wrap">
{flat(body)}
</div></main>
</div>
{RUN_JS}{extra_js}'''

COPY_JS = """<script>
document.querySelectorAll("[data-copy]").forEach(btn=>btn.addEventListener("click",async ()=>{
  const txt = btn.closest(".pcard").querySelector(".ptext").textContent;
  try{ await navigator.clipboard.writeText(txt); }
  catch(e){ const ta=document.createElement("textarea"); ta.value=txt; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove(); }
  const old=btn.textContent; btn.textContent="Copied ✓"; btn.classList.add("ok");
  setTimeout(()=>{btn.textContent=old; btn.classList.remove("ok");},1600);
}));
</script>"""

LINKS_JS = """<script>
(function(){
  document.querySelectorAll('input.lpx').forEach(function(cb){
    if(localStorage.getItem('lp:'+cb.id)==='1') cb.checked=true;
    cb.addEventListener('change',function(){localStorage.setItem('lp:'+cb.id,cb.checked?'1':'0');count(cb.closest('tr'));});
  });
  function count(row){if(!row)return;var t=row.querySelectorAll('input.lpx').length,d=row.querySelectorAll('input.lpx:checked').length;
    var c=row.querySelector('.lpcount');if(c){c.textContent=d+'/'+t;c.style.setProperty('color',(d===t&&t>0)?'var(--up)':'','important');}}
  document.querySelectorAll('tr').forEach(count);
  var cp=document.getElementById('copyprog');
  if(cp) cp.addEventListener('click', async function(){
    var ids=[]; document.querySelectorAll('input.lpx').forEach(function(cb){ if(cb.checked) ids.push(cb.id); });
    var txt='DASHBOARD PROGRESS v1 ('+ids.length+' checked): '+ids.join(',');
    try{ await navigator.clipboard.writeText(txt); }
    catch(e){ var ta=document.createElement('textarea'); ta.value=txt; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); }
    var old=cp.textContent; cp.textContent='Copied '+ids.length+' ✓'; cp.classList.add('ok');
    setTimeout(function(){cp.textContent=old; cp.classList.remove('ok');},2200);
  });
})();
</script>"""

# ---------------- home components ----------------
def area_chart(vals, dates, w=560, h=210, color="var(--s1)", cid="ac", label="Traffic"):
    vals = [v or 0 for v in vals]
    if len(vals) < 2: return ""
    n = len(vals); mx = max(vals) or 1
    padL, padR, padT, padB = 8, 8, 12, 22
    X = lambda i: padL + (w - padL - padR) * (i/(n-1))
    Y = lambda v: padT + (h - padT - padB) * (1 - v/mx)
    grid = ""
    for t in range(4):
        val = round(mx * (3-t) / 3); yy = padT + (h-padT-padB) * (t/3)
        grid += (f'<line x1="{padL}" x2="{w-padR}" y1="{yy:.0f}" y2="{yy:.0f}" stroke="var(--rule)" stroke-width="1"/>'
                 f'<text x="{padL}" y="{yy-3:.0f}" fill="var(--n600)" font-size="9.5" font-family="ui-monospace,monospace">{val:,}</text>')
    st = max(1, n // 6)
    xlab = "".join(f'<text x="{X(i):.0f}" y="{h-6}" fill="var(--n600)" font-size="9.5" text-anchor="middle" font-family="ui-monospace,monospace">{dates[i][5:]}</text>'
                   for i in range(0, n, st))
    line = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    area = f'{padL},{Y(0):.1f} ' + line + f' {X(n-1):.1f},{Y(0):.1f}'
    return (f'<svg width="100%" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" role="img" aria-label="{label}">'
            f'<defs><linearGradient id="{cid}" x1="0" x2="0" y1="0" y2="1">'
            f'<stop offset="0" stop-color="{color}" stop-opacity=".3"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>'
            f'{grid}<polygon points="{area}" fill="url(#{cid})"/>'
            f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="{X(n-1):.1f}" cy="{Y(vals[-1]):.1f}" r="3.6" fill="{color}"/>{xlab}</svg>')

def _port_series():
    dates = []
    for s in ALL:
        ds = [x["date"] for x in daily_of(s)]
        if len(ds) > len(dates): dates = ds
    m = {d: 0 for d in dates}
    for s in ALL:
        for x in daily_of(s):
            if x["date"] in m: m[x["date"]] += x["clicks"]
    return dates, [m[d] for d in dates]

def traffic_chart_card():
    dates, vals = _port_series()
    if len(vals) < 2: return ""
    wk = sum(vals[-7:]); prev = sum(vals[-14:-7])
    d = wk - prev
    dtxt = f'<span class="tmDelta {"up" if d>=0 else "down"}">{"+" if d>=0 else ""}{d} vs prior week</span>'
    return (f'<div class="card"><h2>{icon("trend")} Traffic — all sites · 90 days</h2>'
            f'<p class="sub">GSC clicks/day summed across the portfolio. Last 7 days: <b>{wk}</b> {dtxt}</p>'
            f'{area_chart(vals, dates, cid="acport", label="Portfolio clicks")}</div>')

def wk7(s):
    d = daily_of(s)
    return sum(x["clicks"] for x in d[-7:]) if d else 0

def _cur_snapshot():
    snap = {"_stamp": STAMP_TXT, "sites": {}}
    for s in ALL:
        sm = SEM.get(s) or {}
        snap["sites"][s] = {
            "clicks7d": wk7(s),
            "sem_rd": sm.get("ref_domains"),
            "dfs_rd": dfs_of(s).get("ref_domains"),
            "top100": dfs_of(s).get("ranked_top100"),
            "pages": F.get(s, {}).get("pages"),
            "positions": {r["kw"]: r.get("pos") for r in KT.get(s, [])},
        }
    return snap
CUR_SNAP = _cur_snapshot()

def changes_card():
    if not PREV:
        return (f'<div class="card"><h2>{icon("refresh")} What changed this update</h2>'
                '<p class="sub" style="margin:0">Baseline saved — from the next audit on, this panel lists exactly what moved.</p></div>')
    ch = []
    for s in ALL:
        a = PREV.get("sites", {}).get(s, {}); b = CUR_SNAP["sites"][s]
        if not a: continue
        short = s.replace(".com", "")
        if b["clicks7d"] != a.get("clicks7d") and a.get("clicks7d") is not None:
            d = b["clicks7d"] - a["clicks7d"]
            ch.append(("good" if d > 0 else "down", f"{short}: clicks/7d {a['clicks7d']} -> {b['clicks7d']} ({'+' if d>0 else ''}{d})"))
        for key, lbl in (("sem_rd", "ref. domains (Semrush)"), ("top100", "keywords in top 100")):
            if b.get(key) is not None and a.get(key) is not None and b[key] != a[key]:
                d = b[key] - a[key]
                ch.append(("good" if d > 0 else "down", f"{short}: {lbl} {a[key]} -> {b[key]} ({'+' if d>0 else ''}{d})"))
        # per-keyword moves live on the Rankings board (movement arrows) — not repeated here
        if b.get("pages") and a.get("pages") and b["pages"] != a["pages"]:
            d = b["pages"] - a["pages"]
            ch.append(("info", f"{short}: {a['pages']} -> {b['pages']} pages ({'+' if d>0 else ''}{d})"))
    prev_stamp = PREV.get("_stamp", "")
    if not ch:
        return (f'<div class="card"><h2>{icon("refresh")} What changed this update</h2>'
                f'<p class="sub" style="margin:0">No measurable change since {H.escape(prev_stamp)} — normal on a same-day re-run.</p></div>')
    order = {"good": 0, "info": 1, "down": 2}
    ch.sort(key=lambda x: order[x[0]])
    items = "".join(f'<li class="chg {k}">{H.escape(t)}</li>' for k, t in ch)
    return (f'<div class="card"><h2>{icon("refresh")} What changed this update</h2>'
            f'<p class="sub">Since {H.escape(prev_stamp)} — {len(ch)} change(s).</p>'
            f'<ul class="chglist">{items}</ul></div>')

def goals_card():
    gs = GOALS.get("goals", [])
    if not gs: return ""
    def current(gid):
        if gid == "clicks": return sum(wk7(s) for s in ALL)
        if gid == "top10": return sum(1 for s in ALL for r in KT.get(s, []) if r.get("pos") and r["pos"] <= 10)
        if gid == "prime_rd": return (SEM.get("primeiptv-france.com") or {}).get("ref_domains") or 0
        if gid == "earning": return sum(1 for s in ALL if wk7(s) > 0)
        return 0
    tiles = ""
    for g in gs:
        cur, tgt = current(g["id"]), g["target"]
        pct = max(2, min(100, round(100 * cur / tgt))) if tgt else 0
        done = cur >= tgt
        tiles += (f'<div class="goal"><span class="ovlabel">{H.escape(g["label"])}</span>'
                  f'<span class="goalv">{cur:,}<span class="goalt"> / {tgt:,}</span>'
                  + (' <span class="krank good">DONE ✓</span>' if done else '') + '</span>'
                  f'<div class="ctryTrack"><div class="ctryFill" style="width:{pct}%"></div></div>'
                  f'<span class="ovsub">{pct}% · due {H.escape(g["due"])}</span></div>')
    return (f'<div class="card" style="border-left:4px solid var(--s3)"><h2>{icon("target")} North Star — the goals'
            f'<span style="font-weight:400;color:var(--n600);font-size:12px"> · set {H.escape(GOALS.get("set_on",""))}, change them anytime</span></h2>'
            f'<div class="goalgrid">{tiles}</div></div>')

def weekly_scorecard():
    import datetime as _dt
    dates, vals = _port_series()
    if len(vals) < 14: return ""
    imap = {}
    for s in ALL:
        for x in daily_of(s):
            imap[x["date"]] = imap.get(x["date"], 0) + x["impressions"]
    weeks = {}
    for d, v in zip(dates, vals):
        dt = _dt.date.fromisoformat(d)
        monday = dt - _dt.timedelta(days=dt.weekday())
        wkey = monday.isoformat()
        weeks.setdefault(wkey, {"c": 0, "i": 0, "days": 0})
        weeks[wkey]["c"] += v; weeks[wkey]["i"] += imap.get(d, 0); weeks[wkey]["days"] += 1
    rows = sorted(weeks.items())[-10:]
    prevc = None; out_rows = []
    for wkey, w in rows:
        d = (w["c"] - prevc) if prevc is not None else None
        dtxt = "—" if d is None else f'<span class="tmDelta {"up" if d>=0 else "down"}">{"+" if d>0 else ""}{d}</span>'
        partial = " <span style=\'color:var(--n600)\'>(partial)</span>" if w["days"] < 7 else ""
        out_rows.append(f'<tr><td>wk of {wkey[5:]}{partial}</td><td>{w["c"]:,}</td><td>{dtxt}</td><td>{w["i"]:,}</td></tr>')
        if w["days"] == 7: prevc = w["c"]
    body = "".join(reversed(out_rows))
    return (f'<div class="card"><h2>{icon("chart")} Weekly scorecard — read down the column</h2>'
            f'<p class="sub">Portfolio totals per ISO week (GSC). The clicks column should grow — that is the whole game.</p>'
            f'<div class="overflow"><table><thead><tr><th>week</th><th>clicks</th><th>Δ</th><th>impressions</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div></div>')

def action_strip():
    if not _steps: return ""
    chips = "".join(f'<a class="astep" href="today"><span class="an">{n}</span>'
                    f'<span class="at">{H.escape(t.strip())}</span></a>' for n, t in _steps)
    return (f'<div class="card actcard"><div class="phead" style="margin-bottom:10px">'
            f'<h2>{icon("zap")} Do this today — {len(_steps)} step(s)</h2>'
            f'<a class="copybtn" style="text-decoration:none" href="today">Open the queue →</a></div>'
            f'<div class="actrow">{chips}</div></div>')

def rankings_board():
    rows = []
    for s in ALL:
        for r in KT.get(s, []):
            if r.get("pos"):
                rows.append((r["pos"], r["kw"], r.get("vol") or 0, s, r.get("url", "")))
    total = sum(len(KT.get(s, [])) for s in ALL)
    rows.sort()
    pb = lambda p: f'<span class="krank {"good" if p<=10 else "ok" if p<=30 else "far"}">#{p}</span>'
    if rows:
        body = "".join(f'<tr><td>{pb(p)}</td><td>{H.escape(k)}</td><td>{v:,}</td>'
                       f'<td><a class="slink" href="{SLUG[s]}">{s.replace(".com","")}</a></td>'
                       f'<td style="color:var(--n600)">{H.escape(u)}</td></tr>' for p, k, v, s, u in rows)
        tbl = (f'<div class="overflow"><table><thead><tr><th>pos</th><th>keyword</th><th>vol/mo</th>'
               f'<th>site</th><th>page</th></tr></thead><tbody>{body}</tbody></table></div>')
    else:
        tbl = '<p class="sub" style="margin:0">No targets in the top 100 yet.</p>'
    return (f'<div class="card"><h2>{icon("trend")} Rankings — {len(rows)}/{total} targets in the top 100</h2>'
            f'<p class="sub">Every keyword target, live-probed this audit. Sorted best first.</p>{tbl}</div>')

def ai_search_card():
    vis, cited_only, total = [], [], 0
    for s in ALL:
        sm = SEM.get(s) or {}
        v, c = sm.get("ai_visibility", 0) or 0, sm.get("ai_cited_pages", 0) or 0
        total += c
        if v > 0: vis.append((v, c, s, sm.get("ai_note", "")))
        elif c > 0: cited_only.append((c, s))
    if not vis and not cited_only: return ""
    vis.sort(reverse=True)
    rows = "".join(f'<tr><td><a class="slink" href="{SLUG[s]}">{s.replace(".com","")}</a></td><td>{v}</td>'
                   f'<td>{c} <span style="color:var(--n600)">({H.escape(n)})</span></td></tr>' for v, c, s, n in vis)
    tbl = (f'<div class="overflow"><table><thead><tr><th>site</th><th>visibility</th><th>cited pages</th></tr></thead>'
           f'<tbody>{rows}</tbody></table></div>') if rows else ""
    cited_only.sort(reverse=True)
    also = ('<p class="sub" style="margin:8px 0 0">Cited without visibility yet (all ChatGPT): '
            + " · ".join(f'<a class="slink" href="{SLUG[s]}">{s.replace(".com","")}</a> {c}' for c, s in cited_only)
            + '</p>') if cited_only else ""
    return (f'<div class="card"><h2>{icon("zap")} AI search</h2>'
            f'<p class="sub"><b>{total} pages cited</b> in AI answers (Semrush owner snapshot 2 Aug) — nearly all by ChatGPT; '
            f'Gemini &amp; AI Mode cite nobody in the niche yet. Structured guides + tools are what gets cited.</p>{tbl}{also}'
            '<p class="sub" style="margin:8px 0 0">Cross-check 14 Aug: the DataForSEO LLM-mentions corpus (sampled popular prompts) records '
            '<b>0 mentions</b> for all portfolio domains — the niche is cited via long-tail questions, not popular prompts. '
            'Run <code>/ai-visibility-checker</code> for a live per-query gap list.</p></div>')

def authority_table():
    rows = ""
    for s in ALL:
        dfs = dfs_of(s); sm = SEM.get(s) or {}
        rd, sp = dfs.get("ref_domains"), dfs.get("spam_score")
        hist = [h["sites"].get(s, {}).get("ref_domains") for h in HIST if s in h.get("sites", {})]
        hist = [x for x in hist if x is not None]
        base = hist[0] if hist else rd
        d = (rd or 0) - (base or 0)
        dtxt = f"+{d}" if d > 0 else (str(d) if d < 0 else "±0")
        rows += (f'<tr><td><a class="slink" href="{SLUG[s]}">{s}</a>{ext(s)}</td>'
                 f'<td>{dfs.get("domain_rank") if dfs.get("domain_rank") is not None else "—"}</td>'
                 f'<td>{rd if rd is not None else "—"}</td><td>{dtxt}</td>'
                 f'<td>{sm.get("authority_score","—")}</td><td>{sm.get("ref_domains","—")}</td>'
                 f'<td>{dfs.get("ranked_top100") if dfs.get("ranked_top100") is not None else "—"}</td>'
                 f'<td><span class="krank {_spam_cls(sp)}">{sp if sp is not None else "—"}</span></td></tr>')
    return (f'<div class="card"><h2>{icon("award")} Authority &amp; visibility — two independent indexes</h2>'
            f'<p class="sub">DataForSEO live each audit (Domain Rank 0–1000; 0 = below measurable threshold) · '
            f'Semrush owner-verified ({H.escape(SEM.get("_updated",""))}). <b>Spam +4 pts on a site = pause its link work.</b></p>'
            f'<div class="overflow"><table><thead><tr><th>site</th><th>DFS rank</th><th>DFS ref.dom</th><th>change</th>'
            f'<th>Semrush AS</th><th>SR ref.dom</th><th>top-100 kw</th><th>spam</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div></div>')

def gauges_card():
    tot = ok = 0
    import sitecards as _sc
    for s in ALL:
        for _, o in _sc._health(s, F):
            tot += 1; ok += 1 if o else 0
    tech = round(100*ok/tot) if tot else 0
    ranked_sites = sum(1 for s in ALL if nrank(s) > 0)
    tgt_total = sum(len(KT.get(s, [])) for s in ALL)
    tgt_rank = sum(nrank(s) for s in ALL)
    g = (donut(tech, 100, f"{tech}%", "Tech health", color="var(--s1)")
         + donut(ranked_sites, NSITES, f"{ranked_sites}/{NSITES}", "Sites ranking", color="var(--s3)")
         + donut(tgt_rank, tgt_total, f"{tgt_rank}/{tgt_total}", "Targets in top 100", color="var(--s6)"))
    return f'<div class="card"><h2>{icon("chart")} Portfolio health</h2><div class="gauges">{g}</div></div>'

def opportunity_card():
    gaps, held = [], {}
    for s, v in CT.items():
        for r in v.get("recommend", []):
            vol = r.get("vol") or 0
            if not vol: continue
            if r["covered"]:
                if not r.get("sibling") and (r["kw"] not in held or vol > held[r["kw"]][0]):
                    held[r["kw"]] = (vol, s)
            elif reserved_for(s, r["kw"]):
                gaps.append((vol, r["kw"], s))
    gaps.sort(reverse=True)
    kt_owner = {}
    for s2, rows in KT.items():
        for r in rows: kt_owner.setdefault((MK(s2), r["kw"]), s2)
    held = {k: (v, kt_owner.get((MK(s), k), s)) for k, (v, s) in held.items()}
    ranked_kws = {r["kw"] for rows in KT.values() for r in rows if r.get("pos")}
    if gaps and gaps[0][0] >= 1500:
        vol, kw, s = gaps[0]
        txt = (f'“{H.escape(kw)}” — the biggest genuinely-uncovered gap in the portfolio. Write it on '
               f'<a class="slink" href="{SLUG[s]}">{s.replace(".com","")}</a> — queued on <a class="slink" href="today">Today</a>.')
        num = f"{vol:,}"
    else:
        c = sorted(((v, k, s) for k, (v, s) in held.items() if k not in ranked_kws), reverse=True)
        if not c: return ""
        vol, kw, s = c[0]; num = f"{vol:,}"
        run = " · ".join(f'“{H.escape(k)}” {v:,}' for v, k, _ in c[1:3])
        txt = (f'“{H.escape(kw)}” — the target page on <a class="slink" href="{SLUG[s]}">{s.replace(".com","")}</a> is LIVE ✓ '
               f'but not yet in the top 100. Content is done; <b>authority is the unlock</b> — every referring domain from the '
               f'<a class="slink" href="links">Backlinks</a> matrix moves it. Next: {run}.')
    return (f'<div class="card oppcard"><h2>{icon("gem")} Biggest opportunity</h2>'
            f'<div class="oppNum">{num}<span style="font-size:14px;color:var(--n600);font-weight:600"> /mo</span></div>'
            f'<p class="sub" style="margin:0">{txt}</p></div>')

def country_card():
    agg = {}
    for s in ALL:
        flag, name = CTRY[s]
        val = nrank(s) if GSC_OFF else sum(x["clicks"] for x in daily_of(s))
        agg.setdefault(name, [flag, 0])[1] += val
    rows = sorted(agg.items(), key=lambda kv: -kv[1][1])
    mx = max((v[1] for _, v in rows), default=0) or 1
    tot = sum(v[1] for _, v in rows) or 1
    body = ""
    for name, (flag, c) in rows:
        body += (f'<div class="ctryRow"><span class="ctryFlag">{flag}</span><div class="ctryBarWrap">'
                 f'<div class="ctryName"><span>{name}</span><span>{round(100*c/tot)}%</span></div>'
                 f'<div class="ctryTrack"><div class="ctryFill" style="width:{max(3,round(100*c/mx))}%"></div></div></div>'
                 f'<span class="ctryVal">{c:,}</span></div>')
    title = "Ranking targets by country" if GSC_OFF else "Clicks by country · 90d"
    return f'<div class="card"><h2>{icon("globe")} {title}</h2><div class="ctry">{body}</div></div>'


# ---------------- mission control (v4 home) ----------------

def tile(cls, label, num, sub="", delta=None):
    d = ""
    if delta is not None:
        up = delta >= 0
        d = f'<span class="tileDelta {"up" if up else "down"}">{"▲" if up else "▼"} {abs(delta):,} vs last week</span>'
    return (f'<div class="card tile {cls}"><span class="kpiL">{label}</span>'
            f'<span class="tileNum">{num}</span>'
            + (f'<span class="tileLbl">{sub}</span>' if sub else "") + d + '</div>')

def board_row1():
    dates, vals = _port_series()
    wk = sum(vals[-7:]) if vals else 0
    pw = sum(vals[-14:-7]) if len(vals) >= 14 else 0
    n_rank = sum(nrank(s) for s in ALL)
    top10 = goal_current("top10")
    chart = area_chart(vals[-30:], dates[-30:], w=520, h=150, color="var(--t)", cid="acbrd", label="Clicks 30d") if len(vals) >= 8 else ""
    tgt = next((x["target"] for x in GOALS.get("goals", []) if x["id"] == "clicks"), 0)
    pct = max(3, min(100, round(100 * wk / tgt))) if tgt else 0
    clicks_tile = (f'<div class="card tile t3"><span class="kpiL">CLICKS · PAST 7 DAYS</span>'
                   f'<span class="tileNum">{wk:,}</span>'
                   f'<span class="tileDelta {"up" if wk-pw>=0 else "down"}">{"▲" if wk-pw>=0 else "▼"} {abs(wk-pw):,} vs last week</span>'
                   f'<div class="ctryTrack" style="margin-top:10px"><div class="ctryFill" style="width:{pct}%"></div></div>'
                   f'<span class="tileLbl">{pct}% of the {tgt:,}/week goal</span></div>')
    return ('<div class="board">'
            + clicks_tile
            + f'<div class="card t5"><span class="kpiL">CLICKS · 30 DAYS</span><div style="margin-top:8px">{chart}</div></div>'
            + tile("t4", "TARGETS IN TOP 100", f'{n_rank}<small> / 58</small>', f"{top10} on page 1")
            + '</div>')

def board_goals():
    t = ""
    for gl in GOALS.get("goals", []):
        if gl["id"] == "clicks": continue
        cur, tgt = goal_current(gl["id"]), gl["target"]
        pct = max(3, min(100, round(100 * cur / tgt))) if tgt else 0
        done = cur >= tgt
        foot = "done, goal complete" if done else f"{pct}% - due {gl.get('due', '')}"
        barcol = "var(--up)" if done else "var(--t)"
        t += (f'<div class="card tile t4"><span class="kpiL">{H.escape(gl["label"]).upper()}</span>'
              f'<span class="tileNum">{cur:,}<small> / {tgt:,}</small></span>'
              f'<div class="ctryTrack" style="margin-top:10px"><div class="ctryFill" style="width:{pct}%;background:{barcol}"></div></div>'
              f'<span class="tileLbl">{H.escape(foot)}{" ✓" if done else ""}</span></div>')
    return f'<div class="board">{t}</div>'

def league_barlist():
    rows = []
    mx = 1
    for s in ALL:
        d = daily_of(s)
        wk = sum(x["clicks"] for x in d[-7:]) if d else 0
        pw = sum(x["clicks"] for x in d[-14:-7]) if len(d) >= 14 else 0
        best = None
        for r in KT.get(s, []):
            if r.get("pos") and (best is None or r["pos"] < best[0]): best = (r["pos"], r["kw"])
        rows.append((wk, wk - pw, best, s)); mx = max(mx, wk)
    rows.sort(key=lambda x: -x[0])
    out = ""
    for wk, d, best, s in rows:
        col = f"var(--s{ALL.index(s)+1})"
        dtxt = f'<span class="tileDelta {"up" if d>=0 else "down"}" style="margin:0">{"▲" if d>=0 else "▼"}{abs(d)}</span>' if (wk or d) else ""
        btxt = f'#{best[0]} {H.escape(best[1][:24])}' if best else "no rankings yet"
        rd = (SEM.get(s) or {}).get("ref_domains")
        out += (f'<a class="bl" href="{SLUG[s]}"><div class="blTop"><span class="dot" style="background:{col}"></span>'
                f'<span class="blName">{s.replace(".com","").replace(".fr","")}</span>'
                f'<span class="blSub">{btxt} · {rd if rd is not None else "—"} rd</span>'
                f'{dtxt}<span class="blVal">{wk:,}</span></div>'
                f'<div class="blBar"><div class="blFill" style="width:{max(2, round(100*wk/mx))}%;background:{col}"></div></div></a>')
    return (f'<div class="card t6"><h2>{icon("award")} Traffic by site — 7 days</h2>'
            f'<div class="barlist">{out}</div></div>')

def board_row2():
    return ('<div class="board">' + league_barlist()
            + f'<div class="t6">{tier_board()}</div>' + '</div>')

def board_row3():
    return ('<div class="board">'
            f'<div class="t6">{changes_card()}</div>'
            f'<div class="t6">{milestones_card()}</div>'
            '</div>')

def _dyn_top100():
    return f"{sum(dfs_of(s).get('ranked_top100') or 0 for s in ALL):,}"
def _dyn_rd():
    return f"{sum((SEM.get(s) or {}).get('ref_domains') or 0 for s in ALL)}"
def statusline():
    n_crit = sum(1 for lv, _ in alerts() if lv == "crit")
    n_warn = sum(1 for lv, _ in alerts() if lv == "warn")
    if n_crit: cls, txt = "crit", f"{n_crit} urgent + {n_warn} minor to fix — details below"
    elif n_warn: cls, txt = "warn", f"all clear except {n_warn} minor item(s) — details below"
    else: cls, txt = "ok", "ALL CLEAR — zero technical defects across the portfolio"
    return (f'<div class="statusline {cls}"><span class="stdot"></span><b>{txt}</b>'
            f'<span class="stmeta">{NSITES} sites · 58 keywords probed · {H.escape(STAMP_TXT)}</span></div>')

def goal_current(gid):
    if gid == "clicks": return sum(wk7(s) for s in ALL)
    if gid == "top10": return sum(1 for s in ALL for r in KT.get(s, []) if r.get("pos") and r["pos"] <= 10)
    if gid == "prime_rd": return (SEM.get("primeiptv-france.com") or {}).get("ref_domains") or 0
    if gid == "earning": return sum(1 for s in ALL if wk7(s) > 0)
    return 0

def hero_v4():
    dates, vals = _port_series()
    wk = sum(vals[-7:]) if vals else 0
    prev = sum(vals[-14:-7]) if len(vals) >= 14 else 0
    d = wk - prev
    pills = ""
    for gl in GOALS.get("goals", []):
        cur, tgt = goal_current(gl["id"]), gl["target"]
        pct = max(3, min(100, round(100 * cur / tgt))) if tgt else 0
        done = cur >= tgt
        pills += (f'<div class="gpill{" done" if done else ""}"><span class="gpillL">{H.escape(gl["label"])}'
                  + (' ✓' if done else '') + '</span>'
                  f'<span class="gpillV">{cur:,} / {tgt:,}</span>'
                  f'<div class="ctryTrack"><div class="ctryFill" style="width:{pct}%"></div></div></div>')
    spark_html = spark(vals[-30:], color="var(--t)") if len(vals) >= 8 else ""
    return (f'<div class="hero"><div class="heroGrid"><div class="heroMain">'
            f'<h1>IPTV Portfolio</h1>'
            f'<div class="heroNum">{wk:,}<span class="heroUnit">clicks / week</span></div>'
            f'<span class="kdelta {"up" if d>=0 else "down"}">{"▲" if d>=0 else "▼"} {abs(d)} vs prior week</span>'
            f'<div class="heroSpark">{spark_html}</div></div>'
            f'<div class="gpills">{pills}</div></div></div>'
            )

def attention_card():
    items = [(lv, t) for lv, t in alerts() if lv in ("crit", "warn")]
    if not items: return ""
    rows = "".join(f'<div class="alert {lv}"><b>{"URGENT" if lv == "crit" else "FIX"}</b> · {t}</div>' for lv, t in items)
    return (f'<div class="card" id="attention"><h2>{icon("warn")} Needs attention — {len(items)} item(s)</h2>{rows}</div>')


def work_strip():
    n_dev = sum(1 for s in ALL if tech_items(s))
    n_owner = 2 + (0 if D["sites"].get("iptvsegura.com", {}).get("in_gsc") else 1)
    parts = [("🔧 Developer", n_dev), ("✍️ Content", 1), ("🔗 Links", 1), ("👤 Owner", n_owner)]
    chips = "".join(f'<span class="wchip">{lbl} <b>{n}</b></span>' for lbl, n in parts if n)
    total = sum(n for _, n in parts)
    return (f'<a class="card workstrip" href="today"><div><h2 style="margin:0">{icon("zap")} {total} tasks on the Work page</h2>'
            f'<p class="sub" style="margin:4px 0 0">Organized by role — everyone finds their list in one place.</p></div>'
            f'<div class="wchips">{chips}</div><span class="srarrow">{icon("arrow")}</span></a>')

def moves_card():
    moves = []
    for lv, t in alerts():
        if lv == "crit":
            moves.append(("fix", "Fix the urgent item", t[:120], "today")); break
    moves.append(("links", "One platform row on Backlinks", "The single highest-leverage 30 minutes — every row moved rankings within days.", "links"))
    cands = []
    for s in CONTENT_PRIO:
        rec = CT.get(s, {}).get("recommend", [])
        gp = next((r for r in rec if not r["covered"] and reserved_for(s, r["kw"])), None)
        if gp: cands.append((gp["vol"] or 0, s, gp))
    if cands:
        cands.sort(reverse=True, key=lambda x: x[0])
        _, s, gp = cands[0]
        vol = f"{gp['vol']:,}/mo" if gp['vol'] else "niche"
        moves.append(("write", f"One article: \u201c{gp['kw']}\u201d", f"{vol} · reserved for {s} · 5-skill pipeline on its page.", SLUG[s]))
    moves.append(("index", "Request indexing for yesterday\u2019s pages", "GSC \u2192 URL inspection \u2192 Request indexing. Cuts discovery from weeks to days on low-authority sites.", "today"))
    body = "".join(f'<a class="move" href="{href}"><span class="moveN">{i+1}</span><div class="moveT"><b>{H.escape(t)}</b>'
                   f'<span>{H.escape(d)}</span></div><span class="srarrow">{icon("arrow")}</span></a>'
                   for i, (k, t, d, href) in enumerate(moves[:3]))
    return (f'<div class="card movecard"><h2>{icon("zap")} Today\u2019s three moves</h2>'
            f'<p class="sub">Do these in order — everything else is optional. The full queue lives in <a class="slink" href="today">Today</a>.</p>'
            f'<div class="movegrid">{body}</div></div>')

def league_table():
    rows = []
    for s in ALL:
        d = daily_of(s)
        wk = sum(x["clicks"] for x in d[-7:]) if d else 0
        pw = sum(x["clicks"] for x in d[-14:-7]) if len(d) >= 14 else 0
        best = None
        for r in KT.get(s, []):
            if r.get("pos") and (best is None or r["pos"] < best[0]): best = (r["pos"], r["kw"])
        rows.append((wk, wk - pw, best, s))
    rows.sort(key=lambda x: -x[0])
    out = ""
    for i, (wk, d, best, s) in enumerate(rows):
        cfg = _sc.CONFIG[s]
        dot = f'<span class="dot s{ALL.index(s)+1}"></span>'
        spk = spark([x["clicks"] for x in daily_of(s)[-14:]], color=f"var(--s{ALL.index(s)+1})") if daily_of(s) else '<span class="stmeta">no GSC yet</span>'
        dtxt = f'<span class="kdelta {"up" if d>=0 else "down"}">{"▲" if d>=0 else "▼"}{abs(d)}</span>' if wk or d else ""
        btxt = f'<span class="krank {"good" if best[0]<=10 else "ok" if best[0]<=30 else "far"}">#{best[0]}</span> <span class="lgkw">{H.escape(best[1][:26])}</span>' if best else '<span class="stmeta">no rankings yet</span>'
        rd = (SEM.get(s) or {}).get("ref_domains")
        out += (f'<a class="lgrow" href="{SLUG[s]}"><span class="lgpos">{i+1}</span>{dot}'
                f'<span class="lgname">{s.replace(".com","").replace(".fr","")}</span>'
                f'<span class="lgspark">{spk}</span>'
                f'<span class="lgclicks">{wk:,}<small>/7d</small> {dtxt}</span>'
                f'<span class="lgbest">{btxt}</span>'
                f'<span class="lgrd">{rd if rd is not None else "—"}<small> rd</small></span>'
                f'<span class="badge b-{cfg["tone"]}">{cfg["badge"]} {cfg["status"]}</span></a>')
    return (f'<div class="card"><h2>{icon("award")} The league — ranked by traffic</h2>'
            f'<p class="sub">14-day trend · clicks/week with change · best live ranking · referring domains (Semrush) · status. Tap a row for the full site page.</p>'
            f'<div class="league">{out}</div></div>')

def tier_board():
    prev_pos = {}
    if PREV:
        for s in ALL:
            for kw, p in PREV.get("sites", {}).get(s, {}).get("positions", {}).items():
                prev_pos[(s, kw)] = p
    tiers = [("Page 1", 1, 10, "good"), ("Page 2\u20133", 11, 30, "ok"), ("Climbing", 31, 60, "far"), ("Deep", 61, 100, "far")]
    ranked, absent = [], 0
    for s in ALL:
        for r in KT.get(s, []):
            if r.get("pos"): ranked.append((r["pos"], r["kw"], s))
            else: absent += 1
    ranked.sort()
    cols = ""
    for name, lo, hi, cls in tiers:
        chips = ""
        for p, kw, s in ranked:
            if lo <= p <= hi:
                op = prev_pos.get((s, kw))
                mv = ""
                if op and op != p: mv = f'<i class="{"tup" if p < op else "tdn"}">{"▲" if p < op else "▼"}{abs(op-p)}</i>'
                elif op is None and PREV: mv = '<i class="tup">NEW</i>'
                chips += (f'<span class="tchip"><span class="dot s{ALL.index(s)+1}"></span>'
                          f'{H.escape(kw[:30])} <b class="krank {cls}">#{p}</b>{mv}</span>')
        n = sum(1 for p, _, _ in ranked if lo <= p <= hi)
        if not chips: chips = '<span class="stmeta">none</span>'
        cols += (f'<div class="tiercol"><div class="tierhead">{name} <b>{n}</b></div>'
                 f'<div class="tierchips">{chips}</div></div>')
    return (f'<div class="card"><h2>{icon("trend")} Rankings board — {len(ranked)}/{len(ranked)+absent} targets in the top 100</h2>'
            f'<p class="sub">Colored dot = which site. Arrows = movement since the last audit. {absent} target(s) still outside the top 100.</p>'
            f'<div class="tiers">{cols}</div></div>')

MILESTONES = [
 ("1 Sep", "primeiptv referring-domains goal COMPLETE: 31/30, a month early"),
 ("1 Sep", "\u201cmeilleur boitier iptv\u201d reaches PAGE 1 (#8) \u2014 from #62 in two weeks"),
 ("1 Sep", "\u201clistas iptv espa\u00f1a telegram\u201d back at #1 after the DMCA wobble"),
 ("28 Aug", "iptvshqiptar enters the top 10 (#9)"),
 ("25 Aug", "iptvsegura ranks on page 1 (\u201cestafas iptv\u201d #8) at 3 days old"),
 ("22 Aug", "\u201cessai iptv 7 jours\u201d completes its freeze recovery: #69 \u2192 #4"),
 ("22 Aug", "iptvsegura.com joins as the 10th site \u2014 ES safety lane"),
 ("17 Aug", "smartersprofrance earns its first clicks ever"),
]
def milestones_card():
    rows = "".join(f'<div class="mile"><span class="miledate">{d}</span><span>{t}</span></div>' for d, t in MILESTONES)
    return (f'<div class="card"><h2>{icon("gem")} Milestones — the journey so far</h2><div class="miles">{rows}</div></div>')

def _kpi(ic, label, value, foot="", urg=False):
    return (f'<div class="kpi{" urg" if urg else ""}"><div class="kpiHd"><span class="kpiIcon">{ic}</span>'
            f'<span class="kpiL">{label}</span></div><span class="kpiV">{value}</span>'
            + (f'<span class="kpiFoot">{foot}</span>' if foot else "") + "</div>")

# ---------------- pages ----------------
OUT = os.path.join(BASE, "out")
os.makedirs(OUT, exist_ok=True)
for f_ in os.listdir(OUT):
    if f_.endswith(".html"): os.remove(os.path.join(OUT, f_))
import sitecards as _sc
_sc.POS_LABEL = 'Rankings · last probe 3 Sep (DFS paused)' if DFS_DOWN else 'Live rankings'

tot_rd = sum(dfs_of(s).get("ref_domains") or 0 for s in ALL)
tot_top100 = sum(dfs_of(s).get("ranked_top100") or 0 for s in ALL)
tot_rank = sum(nrank(s) for s in ALL)
n_fix = sum(1 for lv, _ in alerts() if lv in ("crit", "warn"))
head = (f'<div class="hero"><div class="heroTop"><div><h1>IPTV Portfolio</h1>'
        f'<p class="meta" style="margin:8px 0 0">Last updated <span class="freshpill">{H.escape(STAMP_TXT)}</span> · '
        f'{NSITES} active sites · crawl + rankings live{" · GSC traffic paused" if GSC_OFF else ""}</p></div></div>'
        f'<div class="kpibar">'
        + _kpi(icon("trend"), "Keywords · top 100", f"{tot_top100:,}", "DataForSEO, all sites")
        + _kpi(icon("target"), "Targets ranking", f"{tot_rank}", "of the tracked money terms")
        + _kpi(icon("link"), "Referring domains", f"{tot_rd}", "the authority ceiling")
        + _kpi(icon("bell"), "Urgent to fix", f"{n_fix}", "see alerts below ↓", urg=True)
        + "</div></div>")

rows = ""
for s in ALL:
    cfg = _sc.CONFIG[s]; dfs = dfs_of(s)
    nr = nrank(s)
    meta = f'{dfs.get("ranked_top100") if dfs.get("ranked_top100") is not None else "—"} kw top-100'
    rows += (f'<div class="siterow"><a class="srmain" href="{SLUG[s]}">'
             f'<span class="badge b-{cfg["tone"]}">{cfg["badge"]} {cfg["status"]}</span>'
             f'<span class="srname">{s}</span><span class="srmeta">{meta}</span>'
             f'<span class="srmeta" style="min-width:80px">{nr or "—"} ranking</span>'
             f'<span class="srarrow">{icon("arrow")}</span></a>{ext(s)}</div>')
sitelist = (f'<div class="card"><h2>Websites</h2><p class="sub">Status · keywords in the top 100 · ranking targets. '
            f'Tap for the full page; {icon("ext")} opens the live site.</p><div class="sitelist">{rows}</div></div>')

control = (f'<div class="grid2"><div>{traffic_chart_card()}{ai_search_card()}</div>'
           f'<div class="rail">{country_card()}{gauges_card()}{opportunity_card()}</div></div>')

# ═══════════ ORGANIC SCREENS ═══════════
def sdot(s): return f'<span class="dot s{ALL.index(s)+1}"></span>'

def spark_svg(vals, color="#c67139", w=72, hgt=22, sw=1.75):
    vals = [v or 0 for v in (vals or [])][-12:]
    if len(vals) < 2: return ""
    mx = max(vals) or 1
    pts = " ".join(f"{i*(w/(len(vals)-1)):.1f},{hgt-2-(v/mx)*(hgt-4):.1f}" for i, v in enumerate(vals))
    return f'<svg width="{w}" height="{hgt}"><polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}"/></svg>'

def phase_tag(s):
    st = _sc.CONFIG[s]["status"]
    cls = "pos" if st in ("ACCELERATING", "FLAGSHIP", "GROW") else ("warn" if st in ("WATCH", "RECOVERING") else "neu")
    return f'<span class="tag {cls}">{st}</span>'

def ov_alert_banners():
    out = ""
    for lv, t in alerts():
        if lv not in ("crit", "warn"): continue
        site = next((s for s in ALL if s in t), None)
        btn = f'<a class="btn" href="{SLUG[site]}">Open site</a>' if site else ""
        out += (f'<div class="card warn alertbanner"><span class="alertbang">!</span>'
                f'<div style="flex:1"><div class="kick w">Needs attention</div>'
                f'<div style="font-size:15px;margin-top:2px">{t}</div></div>{btn}'
                f'<a class="btn primary" href="today">Open Work</a></div>')
    return out

def ov_north_star():
    cards = ""
    ndone = 0
    for gl in GOALS.get("goals", []):
        cur, tgt = goal_current(gl["id"]), gl["target"]
        pct = max(3, min(100, round(100 * cur / tgt))) if tgt else 0
        done = cur >= tgt; ndone += done
        cards += (f'<div class="card"><div class="kick n">{H.escape(gl["label"])}</div>'
                  f'<div style="margin:6px 0 10px"><span class="big num">{cur:,}</span>'
                  f'<span style="color:var(--n600);font-size:14px"> / {tgt:,}</span></div>'
                  f'<div class="bar"><i class="{"done" if done else ""}" style="width:{pct}%"></i></div>'
                  f'<div style="display:flex;justify-content:space-between;font-size:12px;color:var(--n600);margin-top:8px">'
                  f'<span>{"goal complete" if done else str(pct) + "%"}</span><span>{"done ✓" if done else "due " + H.escape(gl.get("due", ""))}</span></div></div>')
    head = (f'<div class="rowflex" style="justify-content:space-between;margin-bottom:12px"><h2>North star — {len(GOALS.get("goals", []))} goals</h2>'
            f'<span style="font-size:12px;color:var(--n600)">set {H.escape(GOALS.get("set_on", ""))} · {ndone} complete</span></div>')
    return head + f'<div class="grid g4" style="margin-top:0">{cards}</div>'

def ov_sites_table():
    rows = []
    for s in ALL:
        d = daily_of(s)
        wk = sum(x["clicks"] for x in d[-7:]) if d else 0
        pw = sum(x["clicks"] for x in d[-14:-7]) if len(d) >= 14 else 0
        best = None
        for r in KT.get(s, []):
            if r.get("pos") and (best is None or r["pos"] < best[0]): best = (r["pos"], r["kw"])
        rows.append((wk, wk - pw, best, s))
    rows.sort(key=lambda x: -x[0])
    body = ""
    for wk, dl, best, s in rows:
        sm = SEM.get(s) or {}; sp = dfs_of(s).get("spam_score")
        dtxt = f'<span class="{"up" if dl > 0 else "down" if dl < 0 else "flat"}">{"▲ " + str(dl) if dl > 0 else "▼ " + str(abs(dl)) if dl < 0 else "—"}</span>'
        sp_html = (f'<span class="tag warn">{sp}</span>' if (sp or 0) >= 58 else
                   f'<span class="down">{sp}</span>' if (sp or 0) >= 50 else
                   f'<span style="color:var(--n700)">{sp}</span>' if sp is not None else '<span class="flat">—</span>')
        btxt = f'#{best[0]} {H.escape(best[1])}' if best else "—"
        clk30 = [x["clicks"] for x in daily_of(s)[-30:]]
        body += (f'<tr><td><a href="{SLUG[s]}" style="text-decoration:none;color:var(--ink)">{sdot(s)} {ABBR[s]}</a></td>'
                 f'<td>{phase_tag(s)}</td><td style="text-align:right;font-weight:600">{wk:,}</td><td>{dtxt}</td>'
                 f'<td>{spark_svg(clk30)}</td>'
                 f'<td style="font-size:12px;color:var(--n700);max-width:170px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{btxt}</td>'
                 f'<td>{sm.get("ref_domains") if sm.get("ref_domains") is not None else "—"}</td><td>{sp_html}</td></tr>')
    return (f'<div class="card table"><div class="cardhead"><h2>Sites — 7 days</h2></div>'
            f'<div class="overflow"><table><thead><tr><th>Site</th><th>Phase</th><th style="text-align:right">Clicks</th>'
            f'<th>Δ wk</th><th>30d</th><th>Best rank</th><th>Ref.dom</th><th>Spam</th></tr></thead><tbody>{body}</tbody></table></div></div>')

def ov_rankings_card():
    ranked = []
    prev_pos = {}
    if PREV:
        for s in ALL:
            for kw, p in PREV.get("sites", {}).get(s, {}).get("positions", {}).items(): prev_pos[(s, kw)] = p
    total = 0
    for s in ALL:
        for r in KT.get(s, []):
            total += 1
            if r.get("pos"): ranked.append((r["pos"], r["kw"], s))
    ranked.sort()
    n1 = sum(1 for p, _, _ in ranked if p <= 10); n2 = sum(1 for p, _, _ in ranked if 10 < p <= 30)
    n3 = sum(1 for p, _, _ in ranked if 30 < p <= 100); n0 = total - len(ranked)
    dist = (f'<div class="distbar"><i style="flex:{max(n1,1)};background:var(--g)"></i>'
            f'<i style="flex:{max(n2,1)};background:var(--g400)"></i>'
            f'<i style="flex:{max(n3,1)};background:var(--t400)"></i>'
            f'<i style="flex:{max(n0,1)};background:var(--surface)"></i></div>'
            f'<div style="display:flex;gap:12px;font-size:11px;color:var(--n600)">'
            f'<span>● page 1 · {n1}</span><span>● 11–30 · {n2}</span><span>● 31–100 · {n3}</span><span>● out · {n0}</span></div>')
    rows = ""
    for p, kw, s in ranked[:7]:
        op = prev_pos.get((s, kw))
        mv = (f'<span class="up">▲ {op-p}</span>' if op and p < op else
              f'<span class="down">▼ {p-op}</span>' if op and p > op else '<span class="flat">—</span>')
        rows += f'<div class="moverow">{sdot(s)}<span>{H.escape(kw)}</span>{mv}<span class="pos num">#{p}</span></div>'
    return (f'<div class="card"><div class="rowflex" style="justify-content:space-between"><h2>Rankings movement</h2>'
            f'<span style="font-size:13px;color:var(--n600)">{len(ranked)} / {total} in top 100</span></div>{dist}'
            f'<div style="margin-top:10px">{rows}</div></div>')

def ov_backlink_card():
    rd_tot = sum((SEM.get(s) or {}).get("ref_domains") or 0 for s in ALL)
    lb = _LINKS_CACHE["body"]
    tot, chk = _LINKS_CACHE["total"], _LINKS_CACHE["checked"]
    pct = round(100 * chk / tot) if tot else 0
    sp_max = max(((dfs_of(s).get("spam_score") or 0), ABBR[s]) for s in ALL)
    return (f'<div class="card"><h2>Backlink engine</h2>'
            f'<div class="grid g3" style="gap:10px;margin:12px 0">'
            f'<div><div class="kick n">Ref. domains</div><div class="big sm num">{rd_tot}</div></div>'
            f'<div><div class="kick n">Checklist</div><div class="big sm num">{pct}%</div></div>'
            f'<div><div class="kick w">Spam max</div><div class="big sm num" style="color:var(--t700)">{sp_max[0]}</div></div></div>'
            f'<div class="bar"><i class="done" style="width:{pct}%"></i></div>'
            f'<div style="font-size:12px;color:var(--n600);margin-top:8px">{chk} of {tot} placements done</div>'
            f'<a class="linkbtn" href="links" style="display:inline-block;margin-top:8px">Open →</a></div>')

def ov_work_card():
    n_dev = sum(1 for s in ALL if tech_items(s))
    n_owner = 2 + (0 if D["sites"].get("iptvsegura.com", {}).get("in_gsc") else 1)
    tiles = "".join(f'<div class="inset"><div style="font-size:11px;color:var(--n700)">{r}</div>'
                    f'<div class="big sm num">{n}</div></div>'
                    for r, n in [("Developer", n_dev), ("Content", 1), ("Links", 1), ("Owner", n_owner)])
    total = n_dev + 2 + n_owner
    return (f'<div class="card"><h2>Work — by role</h2>'
            f'<div class="grid g4" style="gap:10px;margin:12px 0 10px">{tiles}</div>'
            f'<a class="linkbtn" href="today">All {total} tasks →</a></div>')

def ov_changes_card():
    if not PREV:
        return '<div class="card"><h2>What changed</h2><p class="sub" style="margin-top:8px">Baseline saved — diffs appear from the next audit.</p></div>'
    inner = changes_card()
    return inner

def build_home():
    n_alerts = sum(1 for lv, _ in alerts() if lv in ("crit", "warn"))
    n_dev = sum(1 for s in ALL if tech_items(s))
    n_tasks = n_dev + 2 + 2 + (0 if D["sites"].get("iptvsegura.com", {}).get("in_gsc") else 1)
    dates, vals = _port_series()
    wk = sum(vals[-7:]) if vals else 0
    title = ("All clear this morning." if n_alerts == 0 else
             "Good morning. One thing needs you." if n_alerts == 1 else
             f"Good morning. {n_alerts} things need you.")
    hdr = (f'<div class="hdr"><div><h1>{title}</h1>'
           f'<p class="sub">{NSITES} sites · 58 keywords probed · {wk:,} clicks this week</p></div>'
           f'<div class="rowflex">'
           + (f'<span class="tag warn" style="padding:6px 14px">{n_alerts} fix</span>' if n_alerts else '')
           + f'<span class="tag pos" style="padding:6px 14px">{n_tasks} tasks open</span></div></div>')
    return (hdr + ov_alert_banners() + ov_north_star()
            + f'<div class="grid g169">{ov_sites_table()}<div class="stack">{ov_rankings_card()}{ov_backlink_card()}</div></div>'
            + f'<div class="grid g2">{ov_work_card()}{ov_changes_card()}</div>')


def build_settings():
    integ = [("Google Search Console", "service account · 10 properties · clicks & impressions daily", "pos", "Connected"),
             ("DataForSEO", "backlinks, domain rank, spam, live SERP probes", "warn" if DFS_DOWN else "pos",
              "OUT OF CREDIT — top up" if DFS_DOWN else "Connected"),
             ("Semrush", "AS, ref. domains — pulled live via MCP connector when linked", "neu", "Via Claude"),
             ("Vercel", "deploys ride on git push to the dashboard branch", "pos", "Connected"),
             ("Sales app", "browser-local; lives at /sales, /replies, /support", "neu", "Local")]
    ints = "".join(f'<div class="rowflex" style="padding:9px 0;border-bottom:1px solid var(--rule)">'
                   f'<span class="dot" style="background:{"var(--g)" if k == "pos" else "var(--n400)"}"></span>'
                   f'<div style="flex:1"><div style="font-weight:600;font-size:13px">{n}</div>'
                   f'<div style="font-size:11px;color:var(--n600)">{d}</div></div>'
                   f'<span class="tag {"pos" if k == "pos" else "neu"}">{st}</span></div>'
                   for n, d, k, st in integ)
    goals_rows = "".join(f'<div class="rowflex" style="padding:8px 0"><span style="flex:1;font-size:13px">{H.escape(gl["label"])}</span>'
                         f'<span class="inset" style="padding:5px 14px;font-size:13px">{gl["target"]:,}</span>'
                         f'<span class="inset" style="padding:5px 14px;font-size:13px">{H.escape(gl.get("due", ""))}</span></div>'
                         for gl in GOALS.get("goals", []))
    sites_rows = ""
    for s in ALL:
        gsc = '<span class="up">verified</span>' if D["sites"].get(s, {}).get("in_gsc") else '<span class="down">missing</span>'
        lane_short = H.escape(LANE.get(s, "")[:70])
        sites_rows += (f'<tr><td>{sdot(s)} {ABBR[s]}</td><td>{s}</td><td>{CTRY[s][1]}</td>'
                       f'<td style="font-size:12px;color:var(--n700);max-width:300px">{lane_short}…</td>'
                       f'<td>{phase_tag(s)}</td><td>{gsc}</td>'
                       f'<td class="mono">{CANON.get(s, s)}</td></tr>')
    rules = [("Daily audit", "crawls \u00d7 10 \u2192 GSC + DataForSEO \u2192 58 SERP probes \u2192 Semrush \u2192 regenerate \u2192 deploy \u2192 verify twice"),
             ("Re-probe rule", "any watched ranking that changes is re-probed twice before it is recorded; GSC corroborates big moves"),
             ("Spam pause rule", "+4 points on any site = pause that site\u2019s tier-2 links and review the newest ones")]
    rules_html = "".join(f'<div class="inset" style="margin-top:10px"><div style="font-weight:600;font-size:13px">{t}</div>'
                         f'<div style="font-size:12px;color:var(--n600);margin-top:3px">{d}</div></div>' for t, d in rules)
    return (f'<div class="hdr"><div><h1>Settings & integrations</h1>'
            f'<p class="sub">How the dashboard is wired. Change goals or sites by telling Claude.</p></div></div>'
            f'<div class="grid g2"><div class="card"><h2>Integrations</h2><div style="margin-top:8px">{ints}</div></div>'
            f'<div class="card"><h2>North-star goals</h2><div style="margin-top:8px">{goals_rows}</div>'
            f'<div style="font-size:12px;color:var(--n600);margin-top:8px">To change a target: tell Claude \u201cset the clicks goal to \u2026\u201d</div></div></div>'
            f'<div class="card table"><div class="cardhead"><h2>Sites</h2></div><div class="overflow"><table>'
            f'<thead><tr><th>Slug</th><th>Domain</th><th>Market</th><th>Lane</th><th>Phase</th><th>GSC</th><th>Canonical host</th></tr></thead>'
            f'<tbody>{sites_rows}</tbody></table></div></div>'
            f'<div class="card" style="margin-top:20px"><h2>Audit schedule & rules</h2>{rules_html}</div>')


today_body = build_work()
open(os.path.join(OUT, "today.html"), "w").write(shell("Today — Daily SEO Plan", today_body, cur="today", extra_js=COPY_JS))

# trends
def trends_body():
    b = (f'<h1>Trends — are we winning?</h1>'
         f'<p class="meta">History builds from {H.escape(HIST[0]["date"]) if HIST else "today"} onward.'
         + (" Search Console traffic is paused." if GSC_OFF else "") + '</p>')
    dates, vals = _port_series()
    imap = {}
    for s in ALL:
        for x in daily_of(s): imap[x["date"]] = imap.get(x["date"], 0) + x["impressions"]
    ivals = [imap.get(d, 0) for d in dates]
    tot_c, tot_i = sum(vals), sum(ivals)
    wk = sum(vals[-7:]); pw = sum(vals[-14:-7]) if len(vals) >= 14 else 0
    b += ('<div class="board">'
          + tile("t3", "CLICKS · 90 DAYS", f"{tot_c:,}", "all sites", wk - pw)
          + f'<div class="card t9"><span class="kpiL">CLICKS PER DAY · 90 DAYS</span><div style="margin-top:8px">'
          + (area_chart(vals, dates, w=760, h=170, color="var(--t)", cid="tr1", label="Clicks") if len(vals) > 2 else "") + '</div></div>'
          + '</div><div class="board">'
          + tile("t3", "IMPRESSIONS · 90 DAYS", f"{tot_i:,}", "all sites")
          + f'<div class="card t9"><span class="kpiL">IMPRESSIONS PER DAY · 90 DAYS</span><div style="margin-top:8px">'
          + (area_chart(ivals, dates, w=760, h=170, color="var(--s2)", cid="tr2", label="Impressions") if len(ivals) > 2 else "") + '</div></div>'
          + '</div>')
    b += f'<div class="board"><div class="t6">{weekly_scorecard()}</div><div class="t6">{ai_search_card()}</div></div>'
    tiles = ""
    order = sorted(ALL, key=lambda s: -sum(x["clicks"] for x in daily_of(s)[-90:]) if daily_of(s) else 0)
    for s in order:
        i = ALL.index(s); col = f"var(--s{i+1})"; dfs = dfs_of(s); sm = SEM.get(s) or {}
        clk = [x["clicks"] for x in daily_of(s)[-90:]]
        c90 = sum(clk) if clk else 0
        w7 = sum(clk[-7:]) if clk else 0
        p7 = sum(clk[-14:-7]) if len(clk) >= 14 else 0
        d = w7 - p7
        dl = f'<span class="tileDelta {"up" if d>=0 else "down"}">{"▲" if d>=0 else "▼"} {abs(d)} this week</span>' if clk else ""
        tiles += (f'<a class="card tile t4" style="text-decoration:none" href="{SLUG[s]}">'
                  f'<span class="kpiL"><span class="dot" style="background:{col}"></span> {s.replace(".com","").replace(".fr","").upper()}</span>'
                  f'<span class="tileNum">{c90:,}<small> clicks·90d</small></span>{dl}'
                  f'<div style="margin-top:8px">{spark(clk, color=col) if clk else chr(39)}</div>'
                  f'<span class="tileLbl">{dfs.get("ranked_top100") if dfs.get("ranked_top100") is not None else "—"} kw top-100 · '
                  f'{sm.get("ref_domains") if sm.get("ref_domains") is not None else "—"} ref.dom · '
                  f'{_sc.CONFIG[s]["status"]}</span></a>')
    b += f'<h2 style="margin:8px 0 12px;font-size:17px">Per site — 90-day trajectory</h2><div class="board">{tiles}</div>'
    return b
open(os.path.join(OUT, "trends.html"), "w").write(shell("Trends — IPTV Portfolio", trends_body(), cur="trends"))

# links
def links_body():
    b = (f'<h1>Backlinks — step by step</h1><p class="meta">Scoreboard first, then the work: '
         f'<b>Step 1 → 2 → 3</b>. Tick as you go, sync when done.</p>')
    def pc(t, x):
        return (f'<div class="card pcard"><div class="phead"><h2>{icon("clipboard")} {t}</h2>'
                f'<button class="copybtn" data-copy>Copy prompt</button></div><pre class="ptext">{H.escape(x)}</pre></div>')
    b += (f'<div class="card" style="border-left:4px solid var(--t)"><div class="phead">'
          f'<h2>{icon("check")} Sync your ticks</h2><button class="copybtn" id="copyprog">Copy progress</button></div>'
          '<p class="sub" style="margin:0">Checkboxes save in THIS browser instantly. To make them permanent everywhere: '
          'tick → <b>Copy progress</b> → paste the code to Claude. Stored server-side, pre-checked on every device next deploy.</p></div>')
    b += authority_table()
    PLATFORMS = ["Facebook Page", "X (Twitter) profile", "YouTube channel", "Pinterest profile",
                 "Linktree / About.me hub", "Issuu (1 PDF guide)", "SlideShare (1 PDF)",
                 "WordPress.com blog + 1 post", "Blogger blog + 1 post", "Tumblr blog + 1 post",
                 "Medium article (1 per site)", "Google Alert set for brand"]
    SINGLE = ["Source of Sources signup (ONE expert account)", "Featured.com account (free plan)",
              "Qwoted account", "Talkwalker Alerts account"]
    LIMITED = {"facebookpage": "drip 1-2/day (FB limit)", "mediumarticle1persit": "max 2/day (Medium limit)"}
    heads = "".join(f'<th style="text-align:center">{ABBR[s]}</th>' for s in ALL)
    mrows = ""
    for p in PLATFORMS:
        pid = "".join(c for c in p.lower() if c.isalnum())[:20]
        cells = "".join(f'<td style="text-align:center"><input class="lpx" type="checkbox" id="lp-{pid}-{ABBR[s]}"'
                        f'{" checked" if f"lp-{pid}-{ABBR[s]}" in CHECKED else ""}></td>' for s in ALL)
        lim = f' <span class="krank far" style="font-size:9.5px">⏳ {LIMITED[pid]}</span>' if pid in LIMITED else ""
        mrows += f'<tr><td style="font-family:inherit">{H.escape(p)}{lim}</td>{cells}<td class="lpcount" style="font-weight:700">0/{NSITES}</td></tr>'
    for p in SINGLE:
        pid = "".join(c for c in p.lower() if c.isalnum())[:20]
        mrows += (f'<tr><td style="font-family:inherit">{H.escape(p)}</td>'
                  f'<td colspan="{NSITES}" style="text-align:center"><input class="lpx" type="checkbox" id="lp-{pid}-one"'
                  f'{" checked" if f"lp-{pid}-one" in CHECKED else ""}></td>'
                  f'<td class="lpcount" style="font-weight:700">0/1</td></tr>')
    b += ('<style>.lpx{appearance:none;-webkit-appearance:none;width:20px;height:20px;border:1.5px solid var(--n600);'
          'border-radius:6px;background:transparent;cursor:pointer;position:relative;vertical-align:middle;margin:0}'
          '.lpx:hover{border-color:var(--t)}.lpx:checked{background:var(--t);border-color:var(--t)}'
          '.lpx:checked::after{content:"";position:absolute;left:6px;top:2px;width:5px;height:10px;'
          'border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}.lpcount{color:var(--n700)!important}</style>'
          f'<div class="card"><h2>{icon("check")} Step 1 — Profile foundation: one platform × all {NSITES} sites</h2>'
          '<p class="sub">Pick the <b>topmost row that is not complete and not ⏳ rate-limited</b>, run the batch prompt below, '
          'tick the boxes, move to the next row.</p>'
          f'<div class="overflow"><table><thead><tr><th>platform</th>{heads}<th>done</th></tr></thead><tbody>{mrows}</tbody></table></div></div>')
    b += pc(f"Step 1 batch prompt — one platform × all {NSITES} sites", PLATFORM_BATCH)
    FRS = {"primeiptv-france.com", "iptvpix.com", "smarters-live.com", "smartersprofrance.fr",
           "iptvfranceofficiel.fr", "abonnementiptvofficiel.com"}
    MB = [("French Web 2.0 🇫🇷 — FR sites only", "fr",
           [("Overblog blog + 1 post", "https://www.over-blog.com/"), ("Canalblog blog + 1 post", "https://www.canalblog.com/"),
            ("Skyrock blog + 1 post", "https://www.skyrock.com/blog/"), ("Calameo — 1 PDF guide", "https://www.calameo.com/"),
            ("Dailymotion channel + 1 video", "https://www.dailymotion.com/"), ("Pearltrees collection", "https://www.pearltrees.com/")]),
          ("Web 2.0 & publishing — all sites", "all",
           [("Telegraph tutorial (no signup)", "https://telegra.ph/"), ("Substack newsletter mention", "https://substack.com/"),
            ("Google Sites hub link", "https://sites.google.com/"), ("Notion public guide page", "https://www.notion.so/"),
            ("Write.as blog", "https://write.as/"), ("Hashnode tutorial", "https://hashnode.com/"), ("Dev.to tech tutorial", "https://dev.to/")]),
          ("Video & media — all sites", "all",
           [("Vimeo video + description link", "https://vimeo.com/"), ("Rumble video", "https://rumble.com/"),
            ("Flickr profile/description", "https://www.flickr.com/"), ("Imgur infographic post", "https://imgur.com/"),
            ("SoundCloud profile", "https://soundcloud.com/")]),
          ("Curation & bookmarking — all sites", "all",
           [("Mix saves", "https://mix.com/"), ("Flipboard magazine flip", "https://flipboard.com/"),
            ("Scoop.it topic scoop", "https://www.scoop.it/"), ("Diigo public bookmark", "https://www.diigo.com/"),
            ("Raindrop public collection", "https://raindrop.io/")])]
    mb_rows = ""; cells_n = 0
    for gt, scope, items in MB:
        mb_rows += f'<tr><td colspan="{NSITES+2}" style="font-weight:700;color:var(--n700);padding-top:14px">{gt}</td></tr>'
        for name, url in items:
            pid = "".join(c for c in name.lower() if c.isalnum())[:20]
            cells = ""
            for s in ALL:
                if scope == "fr" and s not in FRS:
                    cells += '<td style="text-align:center;color:var(--n600)">·</td>'
                else:
                    cid = f"lp-mb2-{pid}-{ABBR[s]}"; cells_n += 1
                    cells += (f'<td style="text-align:center"><input class="lpx" type="checkbox" id="{cid}"'
                              f'{" checked" if cid in CHECKED else ""}></td>')
            nm = f'{H.escape(name)} <a class="slink" href="{url}" target="_blank" rel="noopener" style="font-size:11px">open ↗</a>'
            mb_rows += f'<tr><td style="font-family:inherit">{nm}</td>{cells}<td class="lpcount" style="font-weight:700">0/0</td></tr>'
    b += (f'<div class="card"><h2>{icon("gem")} Step 2 — Max-backlinks matrix: one platform × its sites</h2>'
          f'<p class="sub">Same method as Step 1. {cells_n} placements — all free, simple-signup, no business info, '
          f'1-2 per site per day, brand/URL anchors only. FR-only rows apply to the 6 French sites (· = n/a).</p>'
          f'<div class="overflow"><table><thead><tr><th>platform</th>{heads}<th>done</th></tr></thead><tbody>{mb_rows}</tbody></table></div></div>')
    TOOLS = [("checker", "Device checker"), ("codes", "Downloader codes"), ("xtream", "Xtream⇄M3U"), ("calc", "Bandwidth calc")]
    TD = [("Product Hunt launch", "https://www.producthunt.com/"), ("AlternativeTo listing", "https://alternativeto.net/"),
          ("SaaSHub listing", "https://www.saashub.com/"), ("Indie Hackers build post", "https://www.indiehackers.com/"),
          ("Peerlist project", "https://peerlist.io/"), ("SideProjectors listing", "https://www.sideprojectors.com/"),
          ("Launching Next submit", "https://www.launchingnext.com/"), ("StartupBase submit", "https://startupbase.io/")]
    th = "".join(f'<th style="text-align:center">{l}</th>' for _, l in TOOLS)
    tr = ""
    for name, url in TD:
        pid = "".join(c for c in name.lower() if c.isalnum())[:20]
        cells = "".join(f'<td style="text-align:center"><input class="lpx" type="checkbox" id="lp-tool-{pid}-{tk}"'
                        f'{" checked" if f"lp-tool-{pid}-{tk}" in CHECKED else ""}></td>' for tk, _ in TOOLS)
        nm = f'{H.escape(name)} <a class="slink" href="{url}" target="_blank" rel="noopener" style="font-size:11px">open ↗</a>'
        tr += f'<tr><td style="font-family:inherit">{nm}</td>{cells}<td class="lpcount" style="font-weight:700">0/4</td></tr>'
    b += (f'<div class="card"><h2>{icon("zap")} Step 2b — Tool launches: one directory × the 4 tools</h2>'
          '<p class="sub">The shipped tools are the highest-quality links available — directories judge the tool, not the niche. '
          'Product Hunt: ONE launch per tool, spaced weeks apart.</p>'
          f'<div class="overflow"><table><thead><tr><th>directory</th>{th}<th>done</th></tr></thead><tbody>{tr}</tbody></table></div></div>')
    b += pc("Step 2 prompt — Web 2.0 post, any site", WEB20_GENERIC)
    b += (f'<div class="card"><h2>{icon("refresh")} Step 3 — Ongoing weekly cycle</h2>'
          '<div class="overflow"><table><thead><tr><th>#</th><th>action</th></tr></thead><tbody>'
          '<tr><td>1</td><td>2 journalist pitches + check Google Alerts</td></tr>'
          '<tr><td>2</td><td>1 Web 2.0 post (rotate site &amp; platform)</td></tr>'
          '<tr><td>3</td><td>2-3 forum/Quora answers (rotate FR/ES/NL)</td></tr>'
          '<tr><td>4</td><td>Telegram all channels + 1 Reddit value comment</td></tr>'
          '<tr><td>5</td><td>5 outreach emails (mentions/listicles/broken links) → back to 1</td></tr>'
          '</tbody></table></div></div>')
    ql = ('<a href="https://www.sourceofsources.com/" target="_blank" rel="noopener">Source of Sources</a> · '
          '<a href="https://featured.com/" target="_blank" rel="noopener">Featured</a> · '
          '<a href="https://www.qwoted.com/" target="_blank" rel="noopener">Qwoted</a> · '
          '<a href="https://www.google.com/alerts" target="_blank" rel="noopener">Google Alerts</a> · '
          '<a href="https://ahrefs.com/backlink-checker" target="_blank" rel="noopener">Ahrefs free checker</a>')
    ml = " · ".join(f'<a href="https://www.google.com/search?q=%22{s.replace(".com","")}%22+-site%3A{s}" '
                    f'target="_blank" rel="noopener">{s.replace(".com","")}</a>' for s in ALL)
    b += (f'<div class="card"><h2>{icon("globe")} Working links</h2>'
          f'<p class="sub" style="margin-bottom:8px"><b>Journalist platforms &amp; tools:</b> {ql}</p>'
          f'<p class="sub" style="margin:0"><b>Unlinked-mention search:</b> {ml}</p></div>')
    b += pc("Step 3 prompt — journalist pitch", SOS_PITCH)
    b += pc("Step 3 prompt — outreach templates", OUTREACH_TPL)
    MILES = [("m1", "Step 1 profile matrix complete for all sites"),
             ("m2", "primeiptv-france reaches 12 referring domains"),
             ("m3", "Tool #1 launched on Product Hunt"),
             ("m4", "All 4 tools listed on AlternativeTo + SaaSHub"),
             ("m5", "First journalist quote published"),
             ("m6", "Semrush Authority Score reaches 10 on iptvesp or iptvned"),
             ("m7", "iptvesp spam score back under 50"),
             ("m8", "Every satellite has its first 5 referring domains"),
             ("m9", "10 keyword targets ranking in the top 100 portfolio-wide")]
    mr = "".join(f'<tr><td><input class="lpx" type="checkbox" id="lp-au-{k}"{" checked" if f"lp-au-{k}" in CHECKED else ""}></td>'
                 f'<td>{H.escape(t)}</td></tr>' for k, t in MILES)
    b += (f'<div class="card"><h2>{icon("target")} Milestones — tick when true</h2>'
          '<p class="sub">Verifiable outcomes, not busywork. Each one moves the scoreboard at the top.</p>'
          f'<div class="overflow"><table><tbody>{mr}</tbody></table></div></div>')
    return b
open(os.path.join(OUT, "settings.html"), "w").write(shell("Settings — IPTV Portfolio", build_settings(), cur="settings"))
_lb_raw = links_body()
_LINKS_CACHE = {"body": _lb_raw, "total": _lb_raw.count('type="checkbox"'), "checked": _lb_raw.count(" checked")}
open(os.path.join(OUT, "index.html"), "w").write(shell("IPTV Portfolio — SEO Dashboard", build_home(), cur=None))

_lb = links_body()
_total_boxes = _lb.count('type="checkbox"')
_checked_boxes = _lb.count(' checked')
_rd_tot = sum((SEM.get(s) or {}).get("ref_domains") or 0 for s in ALL)
_sp_max = max(((dfs_of(s).get("spam_score") or 0), s) for s in ALL)
_pct = round(100 * _checked_boxes / _total_boxes) if _total_boxes else 0
_links_tiles = ('<div class="board">'
    + tile("t4", "REFERRING DOMAINS", f"{_rd_tot}", "Semrush, all sites — the number this page grows")
    + tile("t4", "CHECKLIST PROGRESS", f"{_pct}%", f"{_checked_boxes} of {_total_boxes} boxes done")
    + tile("t4", "SPAM WATCH", f"{_sp_max[0]}", f"highest: {_sp_max[1].replace('.com','')} — +4pts = pause that site")
    + '</div>')
_lb = _lb.replace('</p>', '</p>' + _links_tiles, 1)
open(os.path.join(OUT, "links.html"), "w").write(shell("Backlinks — IPTV Portfolio", _lb, cur="links", extra_js=COPY_JS + LINKS_JS))


# plan
prow = ""
PHASE = {"iptvesp.com": ("GROW 📈", "Protect the Spanish money queries; conversion module in the Telegram cluster"),
         "primeiptv-france.com": ("FLAGSHIP 🏁", "All new FR content + every outreach link points here"),
         "iptvned.com": ("REBUILD 🔧", "Legal-B2B cluster + NL links"),
         "iptvpix.com": ("RECOVERING 📶", "Keep strengthening internal links; no restructuring"),
         "smarters-live.com": ("BUILD 🔧", "Rank the Smarters-Pro hub and the shipped tools"),
         "iptvshqiptar.com": ("BASELINE 🧱", "Core Albanian content + light link tier"),
         "smartersprofrance.fr": ("SATELLITE ↺", "Install/config long-tail only"),
         "iptvfranceofficiel.fr": ("SATELLITE ↺", "Premium/HDR lane; retitle /application-iptv off the head term"),
         "abonnementiptvofficiel.com": ("WATCH ◎", "Money pages frozen; support with internal links only"),
         "iptvsegura.com": ("ONBOARD ◔", "NEW: ES safety/trust lane — GSC property + first links + fix titles/www")}
for s in ALL:
    ph, job = PHASE[s]; dfs = dfs_of(s)
    prow += (f'<tr><td>{s}</td><td>{ph}</td><td>{job}</td>'
             f'<td>{dfs.get("ranked_top100") if dfs.get("ranked_top100") is not None else "—"} kw · '
             f'{dfs.get("ref_domains") if dfs.get("ref_domains") is not None else "—"} ref.dom</td></tr>')
plan_body = (f'<a class="backlink" href="./">← Portfolio home</a><h1>Plan — where we are going</h1>'
             f'<p class="meta">The standing strategy. Daily execution lives in <a class="slink" href="today">Today</a>; '
             f'the link engine in <a class="slink" href="links">Backlinks</a>.</p>'
             f'<div class="card"><h2>Where each site stands — {gen}</h2><div class="overflow"><table>'
             f'<thead><tr><th>site</th><th>phase</th><th>this cycle\'s job</th><th>status</th></tr></thead>'
             f'<tbody>{prow}</tbody></table></div></div>'
             '<div class="card"><h2>Standing strategy</h2><ul class="lcl">'
             '<li><b>FR flagship = primeiptv.</b> All French links and content investment go here until further notice.</li>'
             '<li><b>iptvesp = protect &amp; monetise.</b> The Telegram cluster carries the traffic; the money page must stay fast and linked.</li>'
             '<li><b>iptvpix = recovering.</b> No penalty; the cause was authority/crawl-demand. Domain Rank is now measurable and Semrush lists it again. No restructuring.</li>'
             '<li><b>Satellites stay in their lanes</b> — spf install/config, ifo premium/HDR, aio trial/deals. One keyword, one page, one site.</li>'
             '<li><b>Authority is the portfolio ceiling.</b> Referring domains per site are still in the single digits on the flagship — the Backlinks steps are the highest-leverage work available.</li>'
             '<li><b>AI search is a live channel.</b> ChatGPT already cites the portfolio; write every article so it can be cited (numbered steps, direct answers, tables).</li>'
             '</ul></div>'
             f'<div class="card" style="border-left:4px solid var(--s2)"><h2>{icon("layers")} Content OS — the 5-skill pipeline</h2>'
             '<p class="sub">Every article now ships through the installed skill system instead of one-shot prompts. '
             'Each site page carries its ready-to-copy workflow with its reserved keyword.</p>'
             '<div class="overflow"><table><thead><tr><th>step</th><th>skill</th><th>what it produces</th></tr></thead><tbody>'
             '<tr><td>0</td><td><code>site-brief-builder</code></td><td>done — 9 briefs drafted at <code>seo-tools/briefs/&lt;site&gt;/site-brief.md</code> (⚠️-verify fields await the owner)</td></tr>'
             '<tr><td>1</td><td><code>keyword-fanout-map</code></td><td>intent-clustered keyword map with live volumes (01-keyword-map.csv)</td></tr>'
             '<tr><td>2</td><td><code>seo-content-writer</code></td><td>the article — citation-ready structure, voice from the brief</td></tr>'
             '<tr><td>3</td><td><code>onpage-optimizer</code></td><td>title/meta/headings/schema pass on the draft</td></tr>'
             '<tr><td>4</td><td><code>internal-link-architect</code></td><td>exact links in/out with anchors (money page prioritised)</td></tr>'
             '<tr><td>5</td><td><code>ai-visibility-checker</code></td><td>AI-citation gap list — feeds the next cycle</td></tr>'
             '</tbody></table></div>'
             '<p class="sub" style="margin-top:8px">Guard rails stay in force: the reserved-keyword queue and the lane contract in each brief '
             'mean the pipeline cannot cannibalize a sibling site. The dashboard audit remains the verifier of record.</p></div>'
             f'<div class="card"><h2>{icon("gem")} Sales — the missing metric</h2>'
             '<p class="sub" style="margin:0">The dashboard tracks visibility; the business runs on subscriptions. '
             'Give Claude a weekly number per site (even approximate — "esp 6 sales, prime 2") and a revenue column '
             'joins the Weekly scorecard, closing the loop from clicks to money.</p></div>')
_pages_tot = sum(F.get(s, {}).get("pages") or 0 for s in ALL)
_arts_tot = sum(len(CT.get(s, {}).get("articles", [])) for s in ALL)
_plan_tiles = ('<div class="board">'
    + tile("t3", "ACTIVE SITES", f"{NSITES}", "4 markets + Poland planned")
    + tile("t3", "PAGES LIVE", f"{_pages_tot}", "crawled this audit")
    + tile("t3", "ARTICLES PUBLISHED", f"{_arts_tot}", "across the portfolio")
    + tile("t3", "PAGE-1 RANKINGS", f"{goal_current('top10')}", "targets in the top 10")
    + '</div>')
plan_body = plan_body.replace('</p>', '</p>' + _plan_tiles, 1)
open(os.path.join(OUT, "plan.html"), "w").write(shell("Plan — IPTV Portfolio", plan_body, cur="plan"))

# per-site pages
def _ovtile(label, value, badge="", sub=""):
    b = f'<span class="ovbadge">{badge}</span>' if badge else ""
    s = f'<span class="ovsub">{sub}</span>' if sub else ""
    return f'<div class="ovtile"><span class="ovlabel">{label}</span><span class="ovval">{value}{b}</span>{s}</div>'

def domain_overview(s):
    sm = SEM.get(s) or {}; dfs = dfs_of(s)
    fv = lambda v: f"{v:,}" if isinstance(v, (int, float)) else (v if v else "—")
    tiles = (_ovtile("Authority Score", sm.get("authority_score", "—"), badge=sm.get("as_label", ""))
             + _ovtile("Organic Traffic", fv(sm.get("organic_traffic")))
             + _ovtile("Organic Keywords", fv(sm.get("organic_keywords")), sub=sm.get("ok_delta", ""))
             + _ovtile("Ref. Domains", fv(sm.get("ref_domains")))
             + _ovtile("Backlinks", fv(sm.get("backlinks"))))
    if sm.get("ai_visibility") or sm.get("ai_cited_pages"):
        tiles += _ovtile("AI Search", fv(sm.get("ai_visibility", 0)),
                         sub=f'{sm.get("ai_cited_pages",0)} cited · {sm.get("ai_note","")}'.rstrip(" ·"))
    sem_note = f'owner-verified {H.escape(sm.get("date",""))}' if sm else "no Semrush data yet"
    sp = dfs.get("spam_score")
    live = (_ovtile("Domain Rank", dfs.get("domain_rank") if dfs.get("domain_rank") is not None else "—", sub="of 1000")
            + _ovtile("Ref. Domains", fv(dfs.get("ref_domains")))
            + _ovtile("Backlinks", fv(dfs.get("backlinks")))
            + _ovtile("Spam", f'<span class="krank {_spam_cls(sp)}">{sp if sp is not None else "—"}</span>')
            + _ovtile("Top-100 KW", fv(dfs.get("ranked_top100")))
            + _ovtile("Targets ranking", f'{nrank(s)}/{len(KT.get(s,[]))}'))
    return (f'<div class="ovwrap"><div class="ovpanel"><div class="ovchip sem">SEMRUSH</div>'
            f'<div class="ovgrid">{tiles}</div><div class="ovfoot">{sem_note}</div></div>'
            f'<div class="ovpanel"><div class="ovchip live">LIVE · DataForSEO + crawl</div>'
            f'<div class="ovgrid">{live}</div><div class="ovfoot">refreshed every audit · {H.escape(gen)}</div></div></div>')

def site_opportunity(s):
    rec = CT.get(s, {}).get("recommend", []); kt = KT.get(s, [])
    ranked = [r for r in kt if r.get("pos")]
    gaps = sorted(((r["vol"] or 0, r["kw"]) for r in rec if not r["covered"] and reserved_for(s, r["kw"])), reverse=True)
    cands = {}
    for r in rec:
        if r["covered"] and not r.get("sibling"): cands[r["kw"]] = (r["vol"] or 0, r.get("page"))
    for r in kt:
        if not r.get("pos") and r["kw"] not in cands: cands[r["kw"]] = (r.get("vol") or 0, r.get("page"))
    for r in ranked: cands.pop(r["kw"], None)
    if gaps and gaps[0][0] >= 300:
        vol, kw = gaps[0]; num = f"{vol:,}"
        txt = (f'“{H.escape(kw)}” — genuinely uncovered here and unclaimed in this market. '
               f'The article prompt below targets it.')
    elif cands:
        kw, (vol, page) = max(cands.items(), key=lambda kv: kv[1][0])
        num = f"{vol:,}" if vol else "—"
        where = f' ({H.escape(page.split(" ")[0])})' if page else ""
        txt = (f'“{H.escape(kw)}” — the target page{where} is LIVE ✓ but not yet in the top 100. '
               f'Content is done; <b>authority is the unlock</b>: internal links pointing in + referring domains.')
    else:
        return ""
    foot = ""
    if ranked:
        foot = ('<p class="sub" style="margin:8px 0 0">Already ranking: '
                + " · ".join(f'“{H.escape(r["kw"])}” <b>#{r["pos"]}</b>' for r in ranked) + ' ✓ — protect these.</p>')
    return (f'<div class="card oppcard"><h2>{icon("gem")} Biggest opportunity — this site</h2>'
            f'<div class="oppNum">{num}<span style="font-size:14px;color:var(--n600);font-weight:600"> /mo</span></div>'
            f'<p class="sub" style="margin:0">{txt}</p>{foot}</div>')

def kt_card(s):
    rows = KT.get(s, [])
    if not rows: return ""
    svol = sum(r.get("vol") or 0 for r in rows); lead = rows[0]; body = ""
    for r in rows:
        p = r.get("pos")
        rk = ('<span class="krank miss">not in top 100</span>' if p is None else
              f'<span class="krank {"good" if p<=10 else "ok" if p<=30 else "far"}">#{p}</span>')
        body += f'<tr><td>{H.escape(r["kw"])}</td><td>{(r.get("vol") or 0):,}</td><td>{rk}</td></tr>'
    return (f'<div class="card"><h2>{icon("target")} Keyword targets</h2>'
            f'<p class="sub">Primary: <b>{H.escape(lead["kw"])}</b> ({(lead.get("vol") or 0):,}/mo) · '
            f'{svol:,}/mo addressable across {len(rows)} terms · {POS_SRC}</p>'
            f'<div class="overflow"><table><thead><tr><th>target keyword</th><th>volume/mo</th><th>current rank</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div></div>')

def content_section(s):
    c = CT.get(s, {}); arts = c.get("articles", []); rec = c.get("recommend", [])
    thin = c.get("n_thin", 0)
    top = "".join(f'<tr><td>{H.escape(a["path"])}</td><td>{a["words"]:,}</td></tr>' for a in arts[:8])
    arts_html = (f'<div class="card"><h2>{icon("file")} Articles — {len(arts)} published'
                 + (f' · <b>{thin}</b> thin (&lt;600 words)' if thin else "") + '</h2>'
                 f'<p class="sub">Longest posts from the live crawl.</p>'
                 f'<div class="overflow"><table><thead><tr><th>article</th><th>words</th></tr></thead>'
                 f'<tbody>{top}</tbody></table></div></div>') if arts else ""
    kw_rows = ""
    for r in rec[:10]:
        if r.get("page"): badge = f'<span class="krank ok">strengthen {H.escape(r["page"].split(" ")[0])}</span>'
        elif r.get("sibling"): badge = f'<span class="krank miss">{H.escape(r["sibling"].split(".")[0])} owns it</span>'
        elif r["covered"]: badge = '<span class="krank miss">has article</span>'
        elif not reserved_for(s, r["kw"]):
            badge = f'<span class="krank miss">queued on {H.escape(RESERVED[(MK(s), r["kw"])].split(".")[0])}</span>'
        else: badge = '<span class="krank good">GAP — write it</span>'
        kw_rows += f'<tr><td>{H.escape(r["kw"])}</td><td>{r["vol"]:,}</td><td>{badge}</td></tr>'
    rec_html = (f'<div class="card"><h2>{icon("bulb")} Recommended keywords — next article</h2>'
                f'<p class="sub">Article-angle terms for this market. "GAP" = nobody in the portfolio covers it.</p>'
                f'<div class="overflow"><table><thead><tr><th>keyword</th><th>vol/mo</th><th>status</th></tr></thead>'
                f'<tbody>{kw_rows}</tbody></table></div></div>') if rec else ""
    nap = next_article_prompt(s)
    nap_html = (f'<div class="card pcard"><div class="phead"><h2>{icon("pen")} No skills installed? Classic one-shot prompt</h2>'
                f'<button class="copybtn" data-copy>Copy prompt</button></div>'
                f'<pre class="ptext">{H.escape(nap)}</pre></div>') if nap else ""
    return arts_html + rec_html

def skill_pipeline_card(s):
    c = CT.get(s, {}); rec = c.get("recommend", [])
    gap = next((r for r in rec if not r["covered"] and reserved_for(s, r["kw"])), None)
    if not gap: return ""
    lang, _ = LANG[s]
    brief = f"seo-tools/briefs/{DOM2SLUG[s]}/site-brief.md"
    vol = f"{gap['vol']:,}/mo" if gap["vol"] else "low volume, on-intent"
    seq = (f'Write the next article for {s} with the 5-skill pipeline. Site brief: {brief} (in the jamal repo).\n\n'
           f'1. /keyword-fanout-map  "{gap["kw"]}"  — country {CTRY[s][1]}, language {lang}, per the site brief.\n'
           f'2. /seo-content-writer  — blog post from 01-keyword-map.csv + the brief. FIRST check no existing\n'
           f'   article on {s} (or any same-market portfolio site) already targets "{gap["kw"]}" — if one does, STOP.\n'
           f'3. /onpage-optimizer  — run on the draft before publishing (blog branch).\n'
           f'4. /internal-link-architect  — target = the new URL on {s}; money page {MONEY[s]} gets priority anchors.\n'
           f'5. Publish + sitemap.xml. The next dashboard audit verifies the page and its rank automatically.')
    return (f'<div class="card pcard" style="border-left:4px solid var(--s2)"><div class="phead">'
            f'<h2>{icon("layers")} Next article — 5-skill pipeline</h2>'
            f'<button class="copybtn" data-copy>Copy workflow</button></div>'
            f'<p class="sub">Reserved for this site: <b>{H.escape(gap["kw"])}</b> ({vol}). '
            f'The skills read <code>{brief}</code> — voice, lane rules and money page come from there, not from memory.</p>'
            f'<pre class="ptext">{H.escape(seq)}</pre></div>')


def site_board(s):
    d = daily_of(s)
    wk = sum(x["clicks"] for x in d[-7:]) if d else 0
    pw = sum(x["clicks"] for x in d[-14:-7]) if len(d) >= 14 else 0
    dfs = dfs_of(s); sm = SEM.get(s) or {}
    best = None
    for r in KT.get(s, []):
        if r.get("pos") and (best is None or r["pos"] < best[0]): best = (r["pos"], r["kw"])
    i = ALL.index(s); col = f"var(--s{i+1})"
    clk = [x["clicks"] for x in d[-30:]] if d else []
    t1 = (f'<div class="card tile t3"><span class="kpiL">CLICKS · PAST 7 DAYS</span>'
          f'<span class="tileNum">{wk:,}</span>'
          + (f'<span class="tileDelta {"up" if wk-pw>=0 else "down"}">{"▲" if wk-pw>=0 else "▼"} {abs(wk-pw)} vs last week</span>' if d else '<span class="tileLbl">no GSC data yet</span>')
          + (f'<div style="margin-top:8px">{spark(clk, color=col)}</div>' if clk else "") + '</div>')
    t2 = (f'<div class="card tile t3"><span class="kpiL">{"BEST RANKING · 3 SEP PROBE" if DFS_DOWN else "BEST LIVE RANKING"}</span>'
          + (f'<span class="tileNum">#{best[0]}</span><span class="tileLbl">{H.escape(best[1])}</span>' if best
             else '<span class="tileNum">—</span><span class="tileLbl">no targets in the top 100 yet</span>') + '</div>')
    kw100 = dfs.get("ranked_top100")
    t3_ = (f'<div class="card tile t3"><span class="kpiL">KEYWORDS · TOP 100</span>'
           f'<span class="tileNum">{kw100 if kw100 is not None else "—"}</span>'
           f'<span class="tileLbl">{sm.get("organic_keywords") if sm.get("organic_keywords") is not None else "—"} in Semrush · {nrank(s)}/{len(KT.get(s, []))} targets</span></div>')
    sp_ = dfs.get("spam_score")
    t4_ = (f'<div class="card tile t3"><span class="kpiL">AUTHORITY</span>'
           f'<span class="tileNum">{sm.get("ref_domains") if sm.get("ref_domains") is not None else "—"}<small> ref.dom</small></span>'
           f'<span class="tileLbl">AS {sm.get("authority_score", "—")} · {sm.get("backlinks") if sm.get("backlinks") is not None else "—"} links · spam {sp_ if sp_ is not None else "—"}</span></div>')
    return f'<div class="board">{t1}{t2}{t3_}{t4_}</div>'

for s in ALL:
    cfg = _sc.CONFIG[s]
    i_s = ALL.index(s) + 1
    body = (f'<a class="backlink" href="./">← All websites</a>'
            f'<div class="hdr sitehdr"><div>'
            f'<h1><span class="dot s{i_s}" style="width:12px;height:12px;margin-right:6px"></span>{s} {ext(s)}</h1>'
            f'<p class="sub">{cfg["country"]} — {cfg["desc"]} · updated {H.escape(STAMP_TXT)}</p></div>'
            f'<span class="badge b-{cfg["tone"]} bigbadge">{cfg["badge"]} {cfg["status"]}</span></div>')
    inner = site_board(s)
    inner += _sc.card(s, D, F, KT, CT, SEM, RECS)
    inner += site_opportunity(s)
    if tech_items(s):
        inner += (f'<a class="card workstrip" href="today"><div><h2 style="margin:0">{icon("warn")} This site has open fixes</h2>'
                  f'<p class="sub" style="margin:4px 0 0">The prompt lives on the Work page — Developer section.</p></div>'
                  f'<span class="srarrow">{icon("arrow")}</span></a>')
    inner += kt_card(s)
    inner += content_section(s)
    body += f'<div class="stack">{inner}</div>'
    open(os.path.join(OUT, f"{SLUG[s]}.html"), "w").write(shell(f"{s} — SEO", body, cur=s, extra_js=COPY_JS))

print("multi-page dashboard written to out/:", sorted(os.listdir(OUT)))

# The diff baseline (prev_snapshot.json) must survive re-runs within one audit:
# generate writes cur_snapshot.json; the DEPLOY step promotes it to prev_snapshot.json
# (cp cur_snapshot.json prev_snapshot.json) only after the new version is verified live.
json.dump(CUR_SNAP, open(os.path.join(BASE, "cur_snapshot.json"), "w"), indent=1)
print("snapshot saved to cur_snapshot.json — promote to prev_snapshot.json after deploy")
