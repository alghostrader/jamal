# Implementation Prompt — Fix Everything Open (Active IPTV Portfolio)

**How to use this:** open a Claude Code session inside the repository (or repositories) containing the websites' source code and paste everything below the line. It is self-contained. Scope is the six **active** properties only: **iptvesp.com · iptvned.com · iptvpix.com · primeiptv-france.com · smarters-live.com · iptvshqiptar.com**. (iptvfranceofficiel.fr, abonnementiptvofficiel.com and smartersprofrance.fr are retired — do not touch them.) After finishing, tick the boxes on the fix tracker (github.com/alghostrader/jamal/issues/1) for independent verification by the daily sync.

---

You are a senior full-stack engineer executing a precise SEO fix list on six websites (Next.js App Router on Vercel, shared template family). Every item below is a **verified, currently-open defect** from a July 2026 audit program, with live acceptance criteria. Work in the order given. For each fix: implement, verify locally, deploy, then verify against the **live production URL** with the exact check stated — an item is done only when its live check passes. One commit per fix (`fix(site): <item> [audit-2026-07]`). Do not refactor beyond what a fix requires; do not change copy except where specified; do not touch robots.txt, canonical logic, hreflang, existing consolidation redirects, or checkout noindex behavior — those are verified correct.

## PART A — Performance (highest value)

**A1. iptvesp.com `/suscripciones` — LCP 4.1–4.3 s, Perf 63–67 (P0).**
The money page of the best-performing site is its slowest page; the LCP element is text delayed by hydration.
- Convert the pricing cards and everything above the fold to server components (drop `"use client"` where there's no interactivity); `next/dynamic` for interactive widgets (plan selector, accordion); analytics stays deferred to first interaction.
- **Accept when:** live Lighthouse mobile: LCP < 2.5 s and Perf ≥ 90, three consecutive runs.

**A2. iptvned.com homepage — TBT regression 280 ms → 780–2,070 ms (P1).**
Measured at 280 ms on 11 July; a content deployment between 11–21 July regressed it (main-thread ~6.4 s).
- `git log` the homepage/shared layout between those dates; find the added client component or script; revert it or dynamic-import it.
- **Accept when:** live Lighthouse mobile TBT < 300 ms, twice consecutively.

**A3. iptvpix.com homepage — Perf 59–78, LCP 3.5–3.7 s, TBT 860 ms+ (P1).**
Never received the hydration treatment. Apply the exact recipe that fixed iptvned's homepage (sibling template, now LCP 1.3 s): server components for hero/pricing/FAQ/testimonials, `next/dynamic` below the fold, single analytics stack, trim the ~500 KB RSC payload.
- **Accept when:** live Lighthouse mobile LCP < 2.5 s AND TBT < 300 ms.

**A4. Smaller performance items (P2, bundle with the above):**
- iptvned `/installatie` — LCP ~2.9 s (same render-delay signature as A2/A3).
- iptvesp `/instalacion` — CLS 0.096 (borderline): add explicit dimensions to whatever shifts.
- **Accept when:** each page live: CLS < 0.1, LCP < 2.5 s.

## PART B — Redirects & links

**B1. www redirects: two 307s → 308 (P1).**
`www.primeiptv-france.com` → apex and `www.iptvned.com` → apex currently return **307** (temporary). In Vercel → Settings → Domains, set each www redirect to permanent.
- **Accept when:** `curl -sI https://www.<domain>/` returns `308` (or `301`) with the correct `location`.

**B2. Internal links routing through redirects (P2).**
- iptvpix: 9 targets (top: `/blog/amende-iptv-france` ×2, `/blog/iptv-samsung-smart-tv-tizen` ×2, `/blog/iptv-legal-france`, `/blog/comment-installer-iptv-smarters`, `/blog/comment-installer-iptv-sur-firestick`, `/blog/france-iptv-m3u`, `/blog/meilleur-abonnement-iptv-france`) — each 308s to a consolidated URL; update the in-content/related-post hrefs to the final destinations.
- iptvesp: `/blog/iptv-espana-sin-cortes` (×2) and any remaining.
- **Accept when:** a site crawl finds zero internal links whose target returns 3xx.

**B3. primeiptv: 2 broken blog cross-links (P2).**
`/blog/comparatif-iptv-france-2026` (intended target: `/comparatif/iptv-france-2026`) and `/blog/smart-tv-ou-fire-stick` (a retired sister-site slug pasted by mistake — link primeiptv's own equivalent guide or remove). One linking page each.
- **Accept when:** site crawl shows zero linked 404s.

## PART C — Titles

**C1. Publishing guard (P1, do first so the regression stops).**
Build-time/CI check that fails when any rendered `<title>` exceeds 60 characters (validate frontmatter/CMS title + template suffix at build). Apply to all six sites' pipelines.

**C2. Trim the open over-length titles (P1):**
iptvned 12 new posts · primeiptv 8 new guides · iptvpix 3 · iptvesp 2 (`iptv-multipantalla-espana` 62, `iptv-telegram-gratis-2026` 67). Keyword first, cut decoration, brand suffix only via the template.
- **Accept when:** sitewide crawl: 0 titles > 60 chars on all four sites.

## PART D — Structure, schema & site-specific

**D1. iptvned legal-B2B cluster concentration (P1).**
The three new posts (`iptv-horeca-legaal-nederland`, `iptv-strafbaar-nederland`, `iptv-illegaal-gevolgen-nederland`) must interlink with each other AND with `/iptv-legaal-nederland` (the consolidated landing), plus one contextual link from `/blog/iptv-opgerold-nederland` (the site's only authority page) into the cluster.
- **Accept when:** each of the four pages has inbound links from ≥ 2 of the others.

**D2. iptvned `/pers-media` is thin (210 words):** expand with the promised press-kit content, or remove from nav + sitemap.

**D3. iptvshqiptar.com — small fixes + baseline (new to the program; recon 28 July).**
The site is healthy (correct www 308 chain, self-referencing canonicals, `lang="sq"`, real `/kontakt`, checkout properly noindexed, per-URL sitemap lastmod, 55-char homepage title). Open items:
- Ship `/favicon.ico` (currently 404; the `<link rel="icon">` route works, legacy fetchers don't).
- Run the standard family checks as a baseline and fix anything found: all titles ≤ 60 chars, descriptions ≤ 160, no internal links to 3xx/404, every sitemap URL has ≥ 3 inlinks, JSON-LD assets all resolve 200, Lighthouse mobile ≥ 90 on home + 1 post.
- **Accept when:** favicon 200 + the baseline checklist passes.

**D4. smarters-live.com — decision + minimal hygiene (P2).**
Near-zero search presence (1 click/90d; 2 pages). Options, owner to choose: (a) **recommended:** 301 its pages to the closest primeiptv-france.com guides (the FR flagship — its TiviMate/app-guide section covers the same topics) and keep the domain parked; (b) build it out as its own property — in which case run the full family baseline (as D3) on it. Implement whichever the owner picks; if no answer, do nothing and flag it in the final summary.

## PART E — Owner tasks (surface to the owner, do not attempt in code)

**E1. iptvpix suppression status:** live evidence (28 July): brand query "iptvpix" ranks the site at position 17 via `/blog` (homepage absent), zero GSC impressions since 18 July — the domain remains algorithmically suppressed despite clean tech. Owner must check GSC UI → Manual Actions + Security Issues. If clean, expected recovery is weeks and often needs a core update; keep A3 (it's worth doing regardless) but route new FR investment to primeiptv.
**E2. Add iptvshqiptar.com to Google Search Console** (Domain property, DNS TXT), submit its sitemap, and add the monitoring service account to it — it's currently the only active site with no measurement.
**E3. Rotate the GSC service-account key and DataForSEO password** when the current monitoring cycle allows — both have been shared in chat.

## PART F — Working rules

- After deploying each fix, run its live acceptance check and paste the result in the commit/PR description.
- If an acceptance check fails twice post-deploy, stop and report rather than stacking changes.
- Do not modify: robots.txt, canonicals, hreflang (primeiptv's geo set is correct), July consolidation redirects, checkout noindex.
- Do not touch the three retired sites (iptvfranceofficiel.fr, abonnementiptvofficiel.com, smartersprofrance.fr) in any way.
- Finish with a summary table: item → commit → live check result, so the owner can tick the fix tracker for independent re-verification.

Priorities if time-boxed: A1 → B1 → C1 → A2 → A3 → C2 → D1 → D3 → everything else.
