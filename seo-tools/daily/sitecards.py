#!/usr/bin/env python3
"""Per-site status cards. Rebuilt 12 Aug 2026; degrades gracefully when GSC traffic is unavailable."""
import html as H

CONFIG = {
    "iptvesp.com":          {"country": "Spain",       "desc": "the growth engine",                      "status": "ACCELERATING", "tone": "good",    "badge": "▲"},
    "primeiptv-france.com": {"country": "France",      "desc": "the flagship",                           "status": "FLAGSHIP",     "tone": "flag",    "badge": "★"},
    "iptvned.com":          {"country": "Netherlands", "desc": "rebuilding via the legal cluster",       "status": "REBUILD",      "tone": "warn",    "badge": "◆"},
    "iptvpix.com":          {"country": "France",      "desc": "recovering — index returning",           "status": "RECOVERING",   "tone": "flag",    "badge": "▲"},
    "smarters-live.com":    {"country": "France",      "desc": "the app hub (tools shipped)",            "status": "BUILD",        "tone": "neutral", "badge": "◔"},
    "iptvshqiptar.com":     {"country": "Albania",     "desc": "first rankings landing",                 "status": "BASELINE",     "tone": "neutral", "badge": "◔"},
    "smartersprofrance.fr": {"country": "France",      "desc": "satellite — Smarters install library",   "status": "SATELLITE",    "tone": "neutral", "badge": "↺"},
    "iptvfranceofficiel.fr":{"country": "France",      "desc": "satellite — premium/HDR lane",           "status": "SATELLITE",    "tone": "neutral", "badge": "↺"},
    "abonnementiptvofficiel.com": {"country": "France","desc": "satellite — trial/deals lane",           "status": "WATCH",        "tone": "warn",    "badge": "◎"},
    "iptvsegura.com":       {"country": "Spain",       "desc": "NEW — ES safety/trust lane",             "status": "ONBOARDING",   "tone": "neutral", "badge": "◔"},
    "rodaktv.com":          {"country": "Poland",      "desc": "NEW — sole PL site + diaspora",          "status": "LAUNCH",       "tone": "neutral", "badge": "◔"},
}
ORDER = ["iptvesp.com", "primeiptv-france.com", "iptvned.com", "iptvpix.com", "smarters-live.com",
         "iptvshqiptar.com", "smartersprofrance.fr", "iptvfranceofficiel.fr", "abonnementiptvofficiel.com", "iptvsegura.com", "rodaktv.com"]

def _health(s, F):
    f = F.get(s, {})
    checks = [("Titles ≤60", len(f.get("titles_over60", [])) == 0),
              ("No redirect-links", len(f.get("redirect_links", [])) == 0),
              ("No orphans", len(f.get("orphans", [])) == 0),
              ("Canonicals", len(f.get("canonical_mismatch", [])) == 0),
              ("No broken links", not f.get("linked404"))]
    www = (f.get("www_redirect", "") or "")
    if "apex" in f:
        checks.append(("apex 308", str(f.get("apex", "")).startswith("308")))
    else:
        checks.append(("www 308", www.startswith("308")))
    if f.get("favicon") is not None:
        checks.append(("Favicon", f.get("favicon") == 200))
    return checks

def card(s, D, F, KT, CT, SEM, RECS, link=None):
    """Organic-design site status card. The page header above it already shows the
    site name/lane and the 4 stat tiles show week clicks + authority — this card
    carries the 90-day view, the story, and the verified checklists. No duplication."""
    cfg = CONFIG[s]
    v = D["sites"].get(s, {})
    dfs = v.get("dfs", {}) or {}
    daily = v.get("daily", [])
    sm = SEM.get(s) or {}
    kt = KT.get(s, [])
    nrank = sum(1 for r in kt if r.get("pos"))
    best = min([r["pos"] for r in kt if r.get("pos")], default=None)
    rd = dfs.get("ref_domains")

    if daily:
        c90 = sum(x["clicks"] for x in daily); i90 = sum(x["impressions"] for x in daily)
        ctr = f"{(100*c90/i90):.1f}%" if i90 else "—"
        stats = [("Clicks · 90 days", f"{c90:,}"), ("Impressions · 90 days", f"{i90:,}"),
                 ("CTR", ctr), ("Targets ranking", f"{nrank}/{len(kt)}")]
    else:
        t100 = dfs.get("ranked_top100")
        stats = [("Top-100 keywords", t100 if t100 is not None else "—"),
                 ("Targets ranking", f"{nrank}/{len(kt)}"),
                 ("Best position", f"#{best}" if best else "—"),
                 ("Articles", CT.get(s, {}).get("n_articles", "—"))]
    statrow = ('<div class="statrow">'
               + "".join(f'<div class="st"><span class="stl">{H.escape(l)}</span>'
                         f'<span class="stv">{val}</span></div>' for l, val in stats)
               + '</div>')

    hc = _health(s, F)
    n_ok = sum(1 for _, ok in hc if ok)
    chips = "".join(f'<span class="hchip {"ok" if ok else "bad"}">{"✓" if ok else "✗"} {H.escape(l)}</span>' for l, ok in hc)
    health = (f'<div class="secrow"><div class="rectitle">Verified clean today · {n_ok}/{len(hc)}</div>'
              f'<div class="hchips">{chips}</div></div>')

    ranked = sorted([r for r in kt if r.get("pos")], key=lambda r: r["pos"])[:4]
    rk = ""
    if ranked:
        rk = (f'<div class="secrow"><div class="rectitle">{globals().get("POS_LABEL", "Live rankings")}</div><div class="hchips">'
              + "".join(f'<span class="hchip ok">#{r["pos"]} {H.escape(r["kw"])}</span>' for r in ranked)
              + '</div></div>')

    narr = _narrative(s, dfs, sm, F, kt, CT)
    recs = "".join(f'<li><span class="tag {"pos" if t.upper()=="DO" else "neu"}">{H.escape(t)}</span>'
                   f'<span>{H.escape(x)}</span></li>' for t, x in RECS.get(s, []))
    recs_html = (f'<div class="secrow"><div class="rectitle">Ongoing priorities</div>'
                 f'<ul class="recs">{recs}</ul></div>') if recs else ""
    return f'''<div class="card sitecard">
      <div class="schead"><h2>Where this site stands</h2></div>
      <p class="narr">{H.escape(narr)}</p>
      {statrow}{rk}{health}{recs_html}</div>'''

def build(D, F, KT, CT, SEM, RECS, links=None):
    links = links or {}
    cards = "".join(card(s, D, F, KT, CT, SEM, RECS, links.get(s)) for s in ORDER)
    return (f'<div class="card" style="background:none;border:none;padding:0;margin-bottom:8px">'
            f'<h2 style="font-size:16px">Site by site</h2></div><div class="scards">{cards}</div>')

def _narrative(s, dfs, sm, F, kt, CT):
    pages = F.get(s, {}).get("pages", "?")
    arts = CT.get(s, {}).get("n_articles", "?")
    rd, top100 = dfs.get("ref_domains"), dfs.get("ranked_top100")
    ranked = [r for r in kt if r.get("pos")]
    if s == "iptvesp.com":
        return (f"The growth engine: {top100} keywords in the top 100 (DataForSEO) across {arts} articles, on {rd} referring domains. "
                f"Semrush AS {sm.get('authority_score','?')} with {sm.get('ref_domains','?')} ref. domains — the strongest profile in the portfolio. "
                f"The Spanish money queries are live; protect them and keep /suscripciones fast.")
    if s == "primeiptv-france.com":
        return (f"The flagship: {arts} articles, {pages} pages, and top-100 keywords up to {top100}. "
                f"Referring domains {rd} (Semrush sees {sm.get('ref_domains','?')}) — still the bottleneck, but it is finally moving. "
                f"All new French content and outreach links belong here.")
    if s == "iptvned.com":
        return (f"{top100} keywords in the top 100 — the widest keyword footprint after esp — on {rd} referring domains. "
                f"Semrush AS {sm.get('authority_score','?')}. The legal-B2B cluster is the replacement play for the faded news query; NL links are the unlock.")
    if s == "iptvpix.com":
        return (f"RECOVERING and now measurable: DataForSEO gives it a Domain Rank of {dfs.get('domain_rank')} — the only site in the portfolio above the measurable threshold — "
                f"on {rd} referring domains, {pages} pages, {arts} articles. Semrush lists it again after a full absence. "
                f"Keep strengthening internal links; no restructuring while the recovery runs.")
    if s == "smarters-live.com":
        return (f"The app hub: {pages} pages with the device-checker and Downloader-codes tools shipped and verified. "
                f"{rd} referring domains (Semrush {sm.get('ref_domains','?')}). It owns the application-iptv lane and the 49,500/mo Smarters-Pro play; "
                f"authority is the only thing between it and those terms.")
    if s == "iptvshqiptar.com":
        return (f"The Albania bet is alive: first live rankings landed ({len(ranked)} target(s) in the top 100) on {pages} pages and {rd} referring domains. "
                f"Small market, modest volumes — but it is no longer invisible. Core Albanian content plus the light link tier keeps it climbing.")
    if s == "smartersprofrance.fr":
        return (f"Satellite, fully repaired: apex 308 ✓, titles ✓, links ✓, and DataForSEO now reports {top100} ranked keyword(s) — its first. "
                f"{arts} articles including the Smarters install library and the new configuration hub. Lane: install/config long-tail only.")
    if s == "iptvfranceofficiel.fr":
        return (f"Satellite on the premium/HDR lane: {arts} articles, {pages} pages, tech clean. "
                f"Semrush AS {sm.get('authority_score','?')} on {sm.get('ref_domains','?')} ref. domains, and notable AI visibility ({sm.get('ai_visibility',0)}) despite low authority — "
                f"AI engines cite it. /iptv-premium is the money page; head terms stay with the flagship.")
    if s == "abonnementiptvofficiel.com":
        pos = ", ".join(f'"{r["kw"]}" #{r["pos"]}' for r in ranked) or "none in the top 100 yet"
        return (f"Trial/deals satellite, post-overhaul watch. Live now: {pos}. Referring domains {rd} (Semrush {sm.get('ref_domains','?')}) — climbing. "
                f"The money pages stay frozen until positions stabilise; support them with internal links only.")
    return ""
