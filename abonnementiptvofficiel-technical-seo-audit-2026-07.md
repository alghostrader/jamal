# Technical SEO Audit — abonnementiptvofficiel.com

**Prepared for:** Site owner, abonnementiptvofficiel.com
**Audit date:** 9 July 2026
**Scope:** Full technical audit — crawl architecture, indexability, Core Web Vitals, structured data, internal linking, mobile usability, HTTPS/security
**Pages analysed:** 36 URLs crawled (100% of the sitemap), 1,383 internal links mapped, 7 Lighthouse lab runs, all findings re-verified against the live site before publication

---

## 1. Executive Summary

abonnementiptvofficiel.com is in strong technical health — every one of its 36 pages is indexable with correct self-referencing canonicals, the site is fully connected within two clicks with zero broken links and zero orphans, security is exemplary, and page templates score 97–100 on mobile performance with the homepage ranging 72–99 across lab runs. The defects that remain are concentrated and fixable in days, not weeks: the declared favicon returns a **404** on every page, **all 36 page titles exceed 60 characters** (five legal/about pages even carry the brand name *twice*), the `/blog` hub ships **no structured data at all**, and the homepage carries the site's heaviest JavaScript load (162 KB gtag.js plus hydration of a 344 KB HTML document) whose blocking-time impact varied too widely in the lab to pin down and should be confirmed with real-user data. One structural risk deserves attention as content grows: the homepage, `/iptv-france` and `/iptv-premium` all compete for the same "abonnement IPTV France" head terms and should be more sharply differentiated before more commercial pages are added.

---

## 2. Health Scorecard

| Area | Status | Notes |
|---|---|---|
| Crawlability & architecture | 🟢 Excellent | Depth ≤ 2; 0 broken links; 0 orphans; sitemap ↔ crawl match 36/36 |
| Indexability | 🟢 Good | All canonicals self-referencing; no noindex conflicts; clean robots.txt |
| Core Web Vitals (lab) | 🟢 Mostly good | Templates 97–100; homepage 72–99 (TBT variance, see §4.4); `/guide-installation` LCP 2.5 s borderline |
| Structured data | 🟡 Needs work | Favicon 404; `/blog` has zero JSON-LD; no FAQPage; non-square logo |
| On-page metadata | 🟡 Needs work | 36/36 titles > 60 chars; 5 doubled brand suffixes; 14/36 descriptions > 160 chars |
| Internal linking | 🟢 Good | Contextual, varied anchors to money pages; minor flat-equity pattern |
| Mobile usability | 🟢 Good | Viewport 36/36; tap targets & font sizes pass |
| HTTPS & security | 🟢 Excellent | TLS 1.3, HSTS preload, CSP, no mixed content |

---

## 3. Prioritized Fix List (Impact × Effort)

| # | Finding | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | `<link rel="icon" href="/favicon.ico">` is declared on every page but **`/favicon.ico` returns 404**. Google renders favicons next to every mobile result; a missing one costs SERP CTR sitewide. | **Med-High** | **Trivial** | **P0** |
| 2 | **Every title (36/36) exceeds 60 characters** (63–120 chars) — all get truncated in SERPs. Five pages (`/a-propos`, all four legal pages) append the brand **twice**: "… · Abonnement IPTV Officiel · Abonnement IPTV Officiel" — a template bug. The 26-char brand suffix is the root cause. | **Med-High** | **Low** | **P0** |
| 3 | `/blog` (the hub for all 24 posts) emits **zero JSON-LD** — no Blog/CollectionPage, no BreadcrumbList — while every other page has schema. | **Med** | **Low** | **P1** |
| 4 | Homepage mobile JavaScript: heaviest JS load on the site (gtag.js 162 KB / up to 531 ms execution; 344 KB HTML hydrated twice via RSC payload). Lab TBT varied 70–690 ms across clean runs — impact unconfirmed, validate with field data before/after deferring gtag. LCP itself is healthy (1.8–2.1 s). | **Med** (unconfirmed) | **Med** | **P1** |
| 5 | Head-term cannibalization risk: homepage ("Meilleur Abonnement IPTV France 2026"), `/iptv-france` ("Abonnement IPTV France 2026") and `/iptv-premium` ("Le meilleur abonnement IPTV") target overlapping queries; the blog adds `meilleur-abonnement-iptv-2026`. Currently mild — differentiate before it compounds. | **Med** | **Med** | **P1** |
| 6 | 14/36 meta descriptions exceed 160 characters (up to 240) — truncated in SERPs. | **Low-Med** | **Low** | **P2** |
| 7 | Missing schema opportunities: no `FAQPage` (FAQ section exists on the homepage), no `aggregateRating` anywhere (only add if genuine on-page reviews exist), `Organization.logo` is the 1200×630 OG image — Google prefers a **square** logo ≥ 112×112. `/a-propos` lacks BreadcrumbList. | **Low-Med** | **Low** | **P2** |
| 8 | Link equity is flat: header/footer give every page — including the four legal pages — the same 35 inlinks as the money pages; weakest blog posts (`iptv-vlc-media-player`, `abonnement-iptv-12-mois-pas-cher`, `abonnement-iptv-multi-ecrans`) have only 2–3 inlinks. | **Low-Med** | **Med** | **P2** |
| 9 | Sitemap `<lastmod>` is build-stamped — all 36 URLs share one identical timestamp, so Google learns to distrust it. | **Low** | **Low** | **P3** |
| 10 | `http://www` variant resolves via a 2-hop redirect chain (`http://www → https://www → apex`). | **Low** | **Low** | **P3** |
| 11 | Article images in blog schema are Pexels stock URLs (`images.pexels.com`) — technically valid (200), but generic stock imagery is reused across the web and adds no image-search value; self-hosted unique images would serve E-E-A-T and image SEO better. | **Low** | **Med** | **P3** |
| 12 | Accessibility: `color-contrast` fails sitewide; `aria-hidden-focus` on interactive elements of `/iptv-premium` and blog posts (Lighthouse a11y 93–96). | **Low** (SEO) | **Med** | **P3** |

---

## 4. Detailed Findings

### 4.1 Crawl & Site Architecture — the strongest area

- **Perfect crawl integrity:** all 36 URLs return 200; the sitemap and the crawl match exactly (nothing in the sitemap is unreachable, nothing reachable is missing from the sitemap); there are **zero orphan pages and zero broken internal links** — rare and commendable.
- **Flat architecture:** homepage → depth 1 (11 pages) → depth 2 (24 blog posts). Nothing deeper.
- **Clean URL handling (all verified):** trailing slashes 308 to canonical form; query parameters (e.g. `?utm_source=`) keep a clean self-referencing canonical; unknown and case-variant URLs return real 404s.
- **Redirects:** HTTPS enforced by 308; the only flaw is the 2-hop `http://www` chain (fix list #10).

### 4.2 Indexability

- `robots.txt` allows everything, declares the sitemap, and explicitly welcomes AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.) — consistent with the site's modern discovery strategy. No crawl traps, no parameter pollution, no noindex conflicts anywhere.
- **All 36 canonicals are correct and self-referencing** — notable because the sister property audited alongside this site had four pages canonicalised to its homepage; this site does not have that defect.
- No hreflang is emitted, which is **correct** for a single-locale French site; `<html lang="fr">` is present on 36/36 pages.
- The only sitemap weakness is the build-stamped `<lastmod>` (identical `2026-07-08T07:56:43Z` on all URLs).

### 4.3 On-Page Metadata — the systematic weakness

- **Titles:** 100% of pages (36/36) exceed 60 characters, ranging 63–120. The pattern `{Page title} · Abonnement IPTV Officiel` guarantees overflow because the brand suffix alone is 26 characters. On five pages a second template layer appends the brand again (verified live): `À propos — Alae H. · Abonnement IPTV Officiel · Abonnement IPTV Officiel`. Google will rewrite or truncate all of these. **Fix:** shorten the suffix (e.g. `· IPTV Officiel`) or drop it on non-brand pages, and de-duplicate the template concatenation.
- **Meta descriptions:** 14/36 over 160 chars (up to 240) — truncation, not a penalty, but wasted copywriting.
- **Headings:** exactly one H1 per page on all 36 pages ✅. OG tags present on 36/36 ✅.

### 4.4 Core Web Vitals & Page Speed

**Method note:** Google PSI/CrUX API quota was unavailable from the audit environment, so figures are **Lighthouse 12 lab data** (emulated mobile, slow-4G simulated throttling). Three homepage runs that produced physically impossible traces (57–77 s attributed to a single script, missing `<title>` on pages that verifiably have one) were identified as audit-harness artifacts, discarded, and replaced with clean re-runs. Field data should be confirmed in Search Console (§6).

| Page (mobile) | Perf | LCP | TBT | CLS |
|---|---|---|---|---|
| `/` (homepage), 3 clean runs | **72 / 83 / 99** | 1.8–2.1 s 🟢 | **70–690 ms** 🟡 (variable) | 0.02 🟢 |
| `/iptv-premium` | 99 | 1.8 s 🟢 | 110 ms 🟢 | 0.03 🟢 |
| `/guide-installation` | 97 | **2.5 s** 🟡 | 120 ms 🟢 | 0 🟢 |
| `/blog/meilleur-abonnement-iptv-2026` | 100 | 1.4 s 🟢 | 80 ms 🟢 | 0.001 🟢 |
| `/` desktop | 100 | 0.6 s 🟢 | 0 ms 🟢 | 0.03 🟢 |

**Diagnosis.** Server-side performance is excellent everywhere (TTFB 60–110 ms, Vercel edge cache, zero render-blocking resources, fonts preloaded, near-zero CLS), and LCP/CLS are stable and healthy on every template. The one open question is homepage **main-thread JavaScript**: across three clean lab runs, TBT ranged 70 ms → 690 ms and main-thread work 1.1 s → 3.2 s. The structural load is real — React hydration of a 344 KB HTML document (site average 269 KB — the Next.js RSC payload ships content twice) plus **gtag.js (162 KB, up to ~531 ms execution)** — but whether it hurts real users at the INP level could not be settled in the lab; check Search Console field data first. `/guide-installation`'s 2.5 s LCP sits exactly on Google's "good" threshold and is worth one look at its hero media. Low-risk improvements regardless: load gtag after first interaction, convert static homepage sections to server components, `next/dynamic` the below-the-fold widgets.

### 4.5 Structured Data

**Present and well-designed** — the schema strategy is clearly deliberate:

| Page | Schema present |
|---|---|
| Homepage | `Organization` + `WebSite` (with SearchAction), `@graph`-linked |
| `/iptv-premium`, `/iptv-france`, `/test-iptv` | `Service` with `AggregateOffer`/`Offer` (prices, EUR, validity) + `BreadcrumbList` |
| `/guide-installation` | `TechArticle` + Breadcrumb |
| `/boitier-iptv` | `ItemList` (comparison) + Breadcrumb |
| `/a-propos` | `ProfilePage` + `Person` (author entity "Alae H.") |
| 24 blog posts | `Article` (complete: author→`/a-propos#person`, dates, publisher, keywords) + Breadcrumb, 24/24 |
| Legal pages | BreadcrumbList |

No JSON-LD parse errors anywhere. The author-entity chain (Article → Person → ProfilePage) is a genuine E-E-A-T strength.

**Gaps and defects:**
1. **Favicon 404 (P0):** the head declares `/favicon.ico`, which does not exist. Also missing: `apple-touch-icon`. (The OG image `/og-default.jpg` works.)
2. **`/blog` has no structured data at all** — verified live (0 `ld+json` scripts). Add `CollectionPage`/`Blog` + `BreadcrumbList`.
3. **Logo shape:** `Organization.logo` reuses the 1200×630 OG banner; Google's guidance for logo display is a square image ≥ 112×112. Ship a dedicated square logo.
4. **No `FAQPage`** despite a "questions fréquentes" section on the homepage — valid markup helps entity understanding and AI-assistant answer surfacing even though classic FAQ rich results are now restricted.
5. **Stock imagery in Article schema:** all post images are Pexels URLs — valid but generic (fix list #11).

### 4.6 Internal Linking

Distinctly better than typical for a site this size:

- Money pages receive **contextual, anchor-diverse links**, not just navigation: `/iptv-premium` is linked with 130+ anchors ("IPTV Premium", "abonnement IPTV Premium", "offre IPTV Premium"…), `/test-iptv` and `/iptv-france` similarly. Average 38 internal links per page, ~2,900 words average content length, no thin pages.
- **Remaining imbalances:** the sitewide footer gives the four legal pages the same 35 inlinks as revenue pages (equity is flat at the top), and the three weakest posts have only 2–3 inlinks (`iptv-vlc-media-player`, `abonnement-iptv-12-mois-pas-cher`, `abonnement-iptv-multi-ecrans`). A related-posts module and a few contextual links would even this out.
- **Cross-domain note:** this site shares an operator with iptvpix.com and covers overlapping topics. A shingle-overlap test on matched article pairs measured **~0% duplication** — the content is genuinely unique per domain, so there is no cross-site duplicate-content risk today. Keep it that way as both blogs grow.

### 4.7 Mobile Usability

Viewport meta on 36/36 pages; Lighthouse tap-target and font-size audits pass on all tested templates; fully server-rendered content (identical without JS); CLS ≤ 0.03 everywhere. Accessibility scores 93–96 with two recurring failures — **color contrast** (sitewide) and **`aria-hidden` elements containing focusable controls** (on `/iptv-premium` and post templates) — compliance/UX issues rather than ranking factors.

### 4.8 HTTPS & Security

- TLS 1.3; valid Let's Encrypt wildcard certificate (expires 6 Sep 2026 — confirm auto-renewal)
- HTTP→HTTPS via 308; HSTS `max-age=63072000; includeSubDomains; preload`
- CSP present and scoped (GTM, GA, fonts, Pexels/Unsplash images, `form-action` limited to self + `wa.me`); `nosniff`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` all set
- Zero mixed content; HTTP/2 with edge caching
- The purchase flow runs through WhatsApp (`wa.me` deep links, verified working). This is fine technically; be aware it leaves no on-site conversion page for analytics or ads tracking — if paid acquisition is planned, add a lightweight on-site confirmation step or event tracking.

---

## 5. 30-Day Roadmap

**Week 1 — Template-level quick wins (dev: ~1 day)**
1. Ship `/favicon.ico` (+ `apple-touch-icon`) — the file is missing, not the tag.
2. Fix the double-brand-suffix bug on `/a-propos` and the four legal pages.
3. Shorten the global title suffix and rewrite the ~10 most important titles to ≤ 60 chars (home, `/iptv-premium`, `/iptv-france`, `/test-iptv`, `/guide-installation`, `/boitier-iptv`, top posts).
4. Collapse the `http://www` redirect chain to one hop.

**Week 2 — Structured data (dev: ~1 day)**
5. Add `CollectionPage` + `BreadcrumbList` JSON-LD to `/blog`; add Breadcrumb to `/a-propos`.
6. Add a square ≥ 112×112 logo and reference it from `Organization.logo`.
7. Add `FAQPage` markup to the homepage FAQ section.
8. Emit real per-URL `<lastmod>` values in the sitemap.
9. Pull Search Console + CrUX field data to baseline real-user CWV.

**Week 3 — Homepage JavaScript (dev: ~2 days, gated on Week-2 field data)**
10. Check Search Console INP/TBT field data first (item 9): if real users confirm blocking time, proceed; if not, do only item 11's cheap wins.
11. Defer gtag.js to first interaction; server components for static homepage sections; `next/dynamic` below the fold; target lab TBT consistently < 200 ms.
12. Check `/guide-installation`'s LCP element (2.5 s, on the threshold) — likely one preload or image-sizing fix.

**Week 4 — Positioning & content ops (content: ongoing)**
13. Differentiate the three overlapping commercial pages: give `/iptv-france` a geo/legal angle, `/iptv-premium` a features/4K angle, and keep "meilleur abonnement IPTV France" for the homepage only; align H1s/titles accordingly.
14. Trim descriptions > 160 chars; add related-posts module; add 2–3 contextual inlinks to the three under-linked posts.
15. Begin replacing Pexels hero images with unique branded images on the top 10 posts.
16. Set up monitoring: monthly crawl for broken links/titles, GSC coverage and CWV tracking.

---

## 6. Verification Log

The five highest-priority findings were re-verified against the live site immediately before this report was finalized (9 July 2026):

| Finding | Re-verification result |
|---|---|
| 1. Favicon declared but missing | ✅ **Confirmed live** — `<link rel="icon" href="/favicon.ico">` present in HTML head; `GET /favicon.ico` → 404 |
| 2. Doubled brand suffix in titles | ✅ **Confirmed live on all 5 pages** — `/a-propos`, `/mentions-legales`, `/conditions-generales`, `/politique-de-remboursement`, `/politique-de-confidentialite` |
| 3. All titles > 60 characters | ✅ **Confirmed** — 36/36 in crawl data; live samples: home 63, `/iptv-premium` 89, `/blog/iptv-smarters-pro` 103 chars |
| 4. `/blog` has zero JSON-LD | ✅ **Confirmed live** — 0 `application/ld+json` scripts on the page |
| 5. Homepage JS weight (344 KB HTML, gtag) | ✅ **Payload confirmed live** (344,102-byte document, gtag.js present) — ⚠️ **the user-impact half of this finding is UNCONFIRMED**: three clean Lighthouse runs disagreed (TBT 70 / 690 ms, perf 72–99), so it is reported as a risk to validate with field data, not a proven defect |

**What could not be confirmed, and why:**

- **Field Core Web Vitals (CrUX):** PSI/CrUX API quota was unavailable from the audit environment. Lab runs were repeated until stable; real-user LCP/INP should be validated in Search Console.
- **Homepage TBT:** clean runs measured 70 ms, 690 ms and (once, alongside other suspect signals) 1,680 ms. The lab could not settle whether homepage blocking time is a real user problem; the fix-list item is scoped accordingly and Search Console INP data should decide the Week-3 investment.
- **Index status & query data:** no Search Console access — the cannibalization assessment (fix #5) is based on on-site targeting signals (titles/H1s/content), not observed query-level competition; validate in GSC Performance before restructuring.
- **Discarded artifacts:** three Lighthouse runs reporting missing `<title>`/`<html lang>` and impossible main-thread times (57–77 s) were traced to the sandboxed audit harness (TLS relay stalls under concurrent runs), re-tested cleanly, and excluded from all conclusions — the affected pages verifiably ship correct titles, descriptions and `lang` attributes (SEO 100 on clean re-runs).

---

## Appendix — Methodology

- **Crawler:** custom BFS crawler (mobile Chrome UA), 36 URLs (100% site coverage), capturing status codes, redirect chains, canonicals, meta robots, titles/descriptions/H1s, viewport, JSON-LD, word counts, image alts, and the full internal-link edge list (1,383 edges).
- **Indexability:** robots.txt, sitemap.xml cross-referenced with crawl; URL-variant probes (trailing slash, case, query params, non-existent paths).
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile + desktop preset, simulated slow-4G), 4 templates + desktop, unstable runs re-executed solo until stable. Audits ran through a local TLS relay required by the sandbox; the relay forces HTTP/1.1, so protocol-level advisories were discarded (live site verified HTTP/2 via curl).
- **Duplication testing:** 8-word shingle Jaccard overlap on matched article pairs across the operator's two domains.
- **Verification:** every P0/P1 finding re-tested with independent live requests before publication (§6).
