# Implementation Prompt — Fix Everything Open (IPTV Portfolio)

**How to use this:** open a Claude Code session inside the repository (or repositories) that contain the websites' source code, and paste everything below the line as the prompt. It is self-contained — the executing Claude does not need this conversation's history. After it finishes, tick the corresponding boxes on the fix tracker (github.com/alghostrader/jamal/issues/1) and the daily sync will verify each fix against the live sites.

---

You are a senior full-stack engineer executing a precise SEO fix list on a portfolio of websites. The list comes from a July 2026 technical audit program; every item below is a **verified, currently-open defect** with acceptance criteria. Work through them in the order given. For each fix: implement it, verify it locally, deploy, then verify against the **live production URL** with the exact check given. Do not consider an item done until its live check passes. Commit per-fix with clear messages. Do not refactor beyond what each fix requires, do not change content/copy except where specified, and do not touch robots.txt, canonicals, or redirects other than those explicitly listed — they are all correct as-is.

The sites (all Next.js App Router on Vercel unless noted): **iptvesp.com, iptvned.com, iptvpix.com, primeiptv-france.com, iptvfranceofficiel.fr, abonnementiptvofficiel.com, smartersprofrance.fr** (static build), smarters-live.com.

## PART A — Performance (highest value)

**A1. iptvesp.com `/suscripciones` — LCP 4.1–4.3 s, Perf 63–67 (P0).**
The money page of the portfolio's best-performing site is its slowest page. The LCP element is text delayed by hydration.
- Convert the pricing-card section and everything above the fold to **server components** (remove `"use client"` where there is no interactivity).
- Load any interactive widget (plan selector, FAQ accordion) via `next/dynamic` so its JS arrives in a later chunk.
- Keep third-party scripts (analytics) deferred to first interaction.
- **Accept when:** Lighthouse mobile (throttled) on the live URL: LCP < 2.5 s, Perf ≥ 90, three consecutive runs.

**A2. iptvned.com homepage — TBT regression 280 ms → 780–2,070 ms (P1).**
This page measured TBT 280 ms on 11 July; a content deployment between 11–21 July regressed it (main-thread ~6.4 s).
- `git log` the homepage and shared layout between those dates; identify the added client component or script (suspects: a new widget shipped with the content wave, an added script tag, a component that lost its server-only status).
- Revert or dynamic-import the culprit.
- **Accept when:** live Lighthouse mobile TBT < 300 ms, twice consecutively.

**A3. iptvpix.com homepage — Perf 59–78, LCP 3.5–3.7 s, TBT 860 ms+ (P1).**
This template was never given the hydration treatment. Apply exactly the same recipe that fixed iptvned's homepage in the 11 July round (its sibling template now scores LCP 1.3 s): server components for hero/pricing/FAQ/testimonials, `next/dynamic` below the fold, single analytics stack, trim the RSC payload (the document is ~500 KB).
- **Accept when:** live Lighthouse mobile LCP < 2.5 s AND TBT < 300 ms.

**A4. Same pass, smaller pages (P2, bundle with A1–A3):**
- iptvned `/installatie` — LCP ~2.9 s (same render-delay signature).
- iptvfranceofficiel `/application-iptv` — **CLS 0.145**: the font-fallback fix (`size-adjust`/`ascent-override` on the @font-face fallback) was applied to the homepage (now CLS 0) but not this template; apply the identical CSS, or find the unsized element in its hero/tab component.
- iptvesp `/instalacion` — CLS 0.096, borderline; add explicit dimensions to whatever shifts.
- **Accept when:** live Lighthouse: each page CLS < 0.1 and LCP < 2.5 s.

## PART B — Redirects & links

**B1. Host redirects: three 307s must become 308 (P1).**
- `smartersprofrance.fr` apex → www: currently **307**. Static host config — set the domain redirect to permanent (308 or 301).
- `www.primeiptv-france.com` → apex and `www.iptvned.com` → apex: currently **307**. In Vercel → Project → Settings → Domains, the www entry's redirect must be set to permanent (308).
- **Accept when:** `curl -sI` on each of the three hosts returns `308` (or `301`) with the correct `location`.

**B2. Internal links still routing through redirects (P2).**
- iptvpix: 9 link targets (top offenders: `/blog/amende-iptv-france` ×2, `/blog/iptv-samsung-smart-tv-tizen` ×2, `/blog/iptv-legal-france`, `/blog/comment-installer-iptv-smarters`, `/blog/comment-installer-iptv-sur-firestick`, `/blog/france-iptv-m3u`, `/blog/meilleur-abonnement-iptv-france`). These 308 to consolidated URLs — update the in-content/related-post hrefs to the final destinations (follow each redirect once to get the target).
- iptvesp: same for `/blog/iptv-espana-sin-cortes` (×2), any remaining references.
- **Accept when:** a crawl of each site finds zero internal links whose target returns 3xx.

**B3. primeiptv: 2 broken blog cross-links (P2).**
`/blog/comparatif-iptv-france-2026` (intended: `/comparatif/iptv-france-2026`) and `/blog/smart-tv-ou-fire-stick` (a sister-site slug pasted by mistake — link the equivalent primeiptv guide or remove). One page links each.
- **Accept when:** site crawl shows zero linked 404s.

## PART C — Titles (one template rule + a wave of trims)

**C1. Publishing guard (P1, do first so the problem stops recurring).**
Add a build-time check (or CI step) that fails when any page's rendered `<title>` exceeds 60 characters. For MDX/CMS content, validate frontmatter `title` + suffix length at build.

**C2. Trim the open over-length titles (P1):** iptvned 12 new posts; primeiptv 8 new guides; iptvesp 2 (`iptv-multipantalla-espana` 62, `iptv-telegram-gratis-2026` 67); iptvpix 3. Keep the keyword at the front, cut decoration, keep the brand suffix only where the template adds it.
- **Accept when:** sitewide crawl shows 0 titles > 60 chars on all four sites.

## PART D — Structure & schema (small)

**D1. abonnementiptvofficiel homepage FAQPage (P2, optional):** the FAQ section exists on-page; emit matching `FAQPage` JSON-LD (questions/answers must mirror the visible content exactly).
**D2. smarters-live.com fold-in (P2):** 301 its two pages (`/` and the blog post) to the equivalent smartersprofrance.fr URLs; keep the domain registered. *Do this only after E1 is done.*
**D3. iptvned `/pers-media` is thin (210 words):** expand with the press-kit content the page promises, or remove it from nav+sitemap.
**D4. iptvned legal-B2B cluster concentration (P1):** the three new posts (`iptv-horeca-legaal-nederland`, `iptv-strafbaar-nederland`, `iptv-illegaal-gevolgen-nederland`) must interlink with each other AND with `/iptv-legaal-nederland` (the consolidated landing), plus one contextual link from `/blog/iptv-opgerold-nederland` (the site's only authority page) into the cluster.
- **Accept when:** each of the four pages has inbound links from at least two of the others.

## PART E — Owner tasks (cannot be done in code — surface these to the owner, do not attempt)

**E1. Verify smartersprofrance.fr in Google Search Console** (Domain property, DNS TXT) and submit `sitemap.xml`. Still unverified as of 28 July.
**E2. iptvpix Manual Actions / Security Issues panels** in GSC UI — still unreported. The domain remains algorithmically suppressed (live evidence, 28 July: brand query "iptvpix" ranks the site at position 17 via /blog, homepage absent from top results; zero GSC impressions since 18 July). If the panels are clean and a fix was recently made, the expected recovery path is weeks and often requires a core update; keep publishing but route new FR investment to primeiptv per the flagship decision.
**E3. Rotate the GSC service-account key and the DataForSEO password** after the current monitoring period — both have been shared in chat.

## PART F — Working rules

- One commit per fix, message format: `fix(site): <item> [audit-2026-07]`.
- After deploying each fix, run its live acceptance check yourself and paste the result in the commit/PR description.
- If an acceptance check fails twice after deploy, stop and report rather than piling on changes.
- Do not modify: robots.txt files, canonical logic, hreflang blocks (primeiptv's geo hreflang is correct), the consolidation redirects shipped in July, or checkout noindex behavior.
- When everything is done, produce a summary table: item → commit → live check result, so the owner can tick the boxes on the fix tracker (github.com/alghostrader/jamal/issues/1) for independent verification.

Priorities if time-boxed: A1 → B1 → C1 → A2 → A3 → C2 → D4 → everything else.
