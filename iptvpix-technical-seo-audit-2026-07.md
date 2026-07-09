# Technical SEO Audit — iptvpix.com

**Prepared for:** Site owner, iptvpix.com
**Audit date:** 9 July 2026
**Scope:** Full technical audit — crawl architecture, indexability, Core Web Vitals, structured data, internal linking, mobile usability, HTTPS/security
**Pages analysed:** 77 URLs crawled (BFS from homepage), 67 sitemap URLs, 5 Lighthouse lab runs, all findings re-verified against the live site before publication

---

## 1. Executive Summary

iptvpix.com is technically well-built — a fast, secure Next.js site with clean URL handling, a valid sitemap, correct 404 behaviour and complete article schema — but a small number of high-impact defects are actively suppressing its ability to rank. The most serious: four indexable pages (including the entire blog hub at `/blog`) declare the **homepage** as their canonical URL, telling Google to drop them from the index; the sitewide Organization logo and Product image in structured data point to a **404 asset**; and roughly **66 internal links across ~24 blog pages point to pages that don't exist** (`/contact`, `/offres`, `/villes/paris`, `/villes/lyon`). Fixing the canonical/hreflang misconfiguration, the broken structured-data asset and the dead internal links — all low-effort changes — should be completed in week one, followed by homepage mobile performance work (LCP 3.2–3.4 s, ~5 s of main-thread JavaScript) and a structured consolidation of the ~30 blog posts competing with each other for the same keywords.

---

## 2. Health Scorecard

| Area | Status | Notes |
|---|---|---|
| Crawlability & architecture | 🟢 Good | Max depth 2 clicks; flat, fully connected; 1 orphan page |
| Indexability | 🔴 Critical issues | 4 pages canonicalised to homepage; broken hreflang; 66+ links to 404s |
| Core Web Vitals (lab) | 🟡 Mixed | Templates score 93–100; homepage mobile 64–84 (LCP 3.2–3.4 s) |
| Structured data | 🟡 Needs work | Sitewide logo 404s; split Product entities; FAQ/Breadcrumb gaps |
| Internal linking | 🟡 Needs work | Equity flat via footer; 15 posts have a single inlink; money pages not prioritised |
| Mobile usability | 🟢 Good | Viewport on 100% of pages; tap targets & font sizes pass |
| HTTPS & security | 🟢 Excellent | TLS 1.3, HSTS preload, strong CSP, no mixed content |

---

## 3. Prioritized Fix List (Impact × Effort)

Score = expected organic impact vs. implementation effort. Fix top-down.

| # | Finding | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | Canonical + hreflang on `/blog`, `/iptv-acheter`, `/box-iptv`, `/pandora-iptv` all point to the homepage — these pages are self-de-indexing. | **High** | **Low** | **P0** |
| 2 | ~66 internal links on ~24 blog pages target 404 pages (`/contact` ×24, `/offres` ×16, `/villes/paris` ×22, `/villes/lyon`, `/iptv-firestick-france`, `/iptv-legal-france-gratuit`). | **High** | **Low** | **P0** |
| 3 | `https://iptvpix.com/icon.svg` returns **404** but is the Organization `logo` (all ~72 pages) and the Product `image` on `/abonnements`. `/favicon.ico` also 404s. | **Med-High** | **Trivial** | **P0** |
| 4 | Keyword cannibalization: 13 pages target "IPTV légal France", 10 target generic "IPTV France", 7 target "meilleur IPTV" — each with self-referencing canonicals, splitting relevance signals. | **High** | **High** | **P1** |
| 5 | Homepage mobile performance: LCP 3.2–3.4 s, TBT 360–1,780 ms, ~5 s main-thread work, 503 KB HTML document, 162 KB Google Tag Manager. All other templates score 93–100. | **Med-High** | **Med** | **P1** |
| 6 | `/a-propos` is an orphan — in the sitemap but receives **zero** internal links. It is also the author-entity URL in every BlogPosting schema. | **Med** | **Trivial** | **P1** |
| 7 | `/abonnements` splits Product markup into two separate entities (one with `offers`, one with `aggregateRating`/`review`), preventing a merged rich result with both price and stars. | **Med** | **Low** | **P1** |
| 8 | Internal link equity is flat: footer/nav gives every utility page (privacy policy, press) 70 inlinks — identical to money pages — while 15 blog posts have exactly 1 inlink. No related-posts module. | **Med** | **Med** | **P2** |
| 9 | Missing schema by page type: no `FAQPage` (FAQ content exists on home & `/abonnements`), no `BreadcrumbList` on 11 of 18 landing pages or the homepage, no `Blog`/`CollectionPage` on `/blog`. | **Med** | **Low** | **P2** |
| 10 | Title/description hygiene: ~50 titles exceed 65 characters (up to 137), ~35 meta descriptions exceed 170 characters (up to 306) — truncated in SERPs. | **Low-Med** | **Med** | **P2** |
| 11 | `http://www.iptvpix.com` resolves via a 2-hop chain (`308 → https://www → 308 → apex`). | **Low** | **Low** | **P3** |
| 12 | Sitemap `<lastmod>` is build-stamped — all 67 URLs share the identical timestamp, so Google learns to ignore it. | **Low** | **Low** | **P3** |
| 13 | Accessibility: `color-contrast` and `heading-order` fail sitewide (Lighthouse a11y 91–96). | **Low** (SEO) | **Med** | **P3** |

---

## 4. Detailed Findings

### 4.1 Crawl & Site Architecture

**What works well.** The site is exceptionally flat: from the homepage, every one of the 71 indexable pages is reachable within **2 clicks** (depth 0: 1, depth 1: 18, depth 2: 51 — only `/checkout` sits at depth 3, and it is correctly noindexed). Trailing-slash URLs 308-redirect to the canonical non-slash form, query parameters (e.g. `?utm_source=`) return the clean self-referencing canonical, and unknown URLs return a **real 404 status** (no soft-404s).

**Issues.**

- **Orphan page:** `/a-propos` (About) is listed in the sitemap and returns 200, but no crawled page links to it. This is doubly costly because every blog post's `BlogPosting` schema names it as the author URL (`Rédaction IPTVPIX → https://iptvpix.com/a-propos`) — an E-E-A-T asset Google can only reach through the sitemap.
- **Broken internal links (66+ instances, verified live):** blog templates link to pages that were evidently planned but never shipped:
  - `/contact` — linked from **24** pages
  - `/villes/paris` — linked from **22** pages (plus `/villes/lyon` from 1)
  - `/offres` — linked from **16** pages
  - `/iptv-firestick-france` (2 links from the Apple TV guide) and `/iptv-legal-france-gratuit` (1 link) — these look like former URLs whose content now lives under `/blog/…`; they should be 301-redirected, not just unlinked.
- **Redirect chain:** `http://www.iptvpix.com` → `https://www.iptvpix.com` → `https://iptvpix.com` (2 hops). Each protocol/host variant should reach the canonical origin in a single hop.

### 4.2 Indexability — robots.txt, Sitemap, Canonicals, noindex

**What works well.** `robots.txt` is clean: it allows everything except `/checkout`, declares both sitemaps, and explicitly welcomes AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.) — a sensible modern choice. The sitemap contains 67 URLs, all returning 200, all absolute HTTPS. Checkout pages combine `noindex, nofollow` with canonicals to `/checkout` and are excluded from the sitemap — correct handling of transactional pages.

**Critical issue — self-de-indexing pages (verified live, twice):**

| Page | Canonical points to | hreflang points to |
|---|---|---|
| `/blog` (the hub linking all 51 posts) | `https://iptvpix.com` | all variants → homepage |
| `/iptv-acheter` | `https://iptvpix.com` | all variants → homepage |
| `/box-iptv` | `https://iptvpix.com` | all variants → homepage |
| `/pandora-iptv` | `https://iptvpix.com` | all variants → homepage |

These four pages tell Google "I am a duplicate of the homepage." Google will typically drop them from the index and disregard their content entirely — for `/blog` this also weakens the crawl/discovery path to all 51 posts. All four are in the sitemap with priority values, which directly contradicts the canonical signal. **Fix:** make each canonical self-referencing.

**hreflang is structurally broken.** Only 5 of 71 pages emit hreflang (`fr`, `fr-FR`, `fr-BE`, `x-default`), and on all 5 every alternate URL is the homepage. hreflang must be reciprocal and self-referencing per page. Since the site has a single French version, the cleanest fix is to **remove hreflang entirely** (the `<html lang="fr">` attribute, present on all pages, is sufficient), or implement it correctly on every page pointing to itself.

**Minor.** One robots-meta nuance: `/checkout` is both `Disallow`ed in robots.txt and `noindex`ed — because Googlebot cannot fetch a disallowed page, it never sees the noindex. If checkout URLs ever attract external links they could appear as "indexed, though blocked by robots.txt". Pick one mechanism (noindex alone is safer; remove the Disallow) — low urgency.

### 4.3 Core Web Vitals & Page Speed

**Method note:** Google's PageSpeed Insights / CrUX API quota was unavailable from this environment, so results below are **Lighthouse 12 lab data** (emulated Moto G Power, 4× CPU throttle, slow-4G), each key page run 1–3 times. Lab TBT on the homepage varied between runs (360 ms – 1,780 ms); LCP was stable. **Field data (CrUX / Search Console Core Web Vitals report) should be pulled to confirm real-user numbers** — flagged in §6.

| Page (mobile) | Perf | LCP | TBT | CLS | SEO | A11y |
|---|---|---|---|---|---|---|
| `/` (homepage) | **64–84** | **3.2–3.4 s** 🔴 | 360–1,780 ms 🔴 | 0.046 🟢 | 100 | 95 |
| `/abonnements` | 93–95 | 1.4 s 🟢 | 230–300 ms 🟡 | 0–0.046 🟢 | 100 | 91 |
| `/installation` | 99–100 | 1.1 s 🟢 | 10–80 ms 🟢 | 0 🟢 | 100 | 94 |
| `/blog/iptv-france-2026-guide-complet` | 95 | 1.1 s 🟢 | 240 ms 🟡 | 0.046 🟢 | 100 | 96 |
| `/` desktop | 96 | 0.6 s 🟢 | 150 ms 🟢 | 0.008 🟢 | — | — |

**Diagnosis — the homepage is the outlier, and the cause is JavaScript, not images:**

- The LCP element is a **text paragraph** (`div.surface-strong … p`), with ~1.06 s of *element render delay* on top of ~0.58 s TTFB — the text is in the server HTML but paints late because the main thread is busy hydrating.
- Main-thread work totals **4.6–5.2 s**; ~3.8 s is attributed to the homepage document itself (inline scripts + React hydration of a **503 KB HTML document** — the largest on the site is `/abonnements` at 574 KB). The Next.js RSC payload effectively ships page content twice.
- **Google Tag Manager (gtag.js, 162 KB)** is the single largest resource on the page and contributes ~240 ms of execution; Plausible is also loaded, so analytics is doubled up.
- Server response is excellent (TTFB 60–150 ms, Vercel edge cache HIT), render-blocking resources: none, fonts: preloaded correctly, CLS: near zero everywhere. The foundation is strong — this is purely a JS-weight problem concentrated on the homepage.

**Recommendations (in order of return):** load gtag.js after first interaction or drop it in favour of the already-present Plausible; audit the homepage for client components that can become server components (hydration cost scales with the 503 KB payload); split below-the-fold sections (testimonial/FAQ widgets) with `next/dynamic`; re-measure. Target: LCP < 2.5 s, TBT < 200 ms on mobile lab.

### 4.4 Structured Data

**Present and correct:** all 51 blog posts carry complete `BlogPosting` (headline, dates, author with URL, publisher, image — verified the hero image returns 200 — `wordCount`, `inLanguage`) plus `BreadcrumbList`. `Organization` and `WebSite` (with SearchAction) are emitted sitewide. No JSON-LD parse errors anywhere.

**Issues:**

1. **Broken logo/image asset (sitewide, verified live):** `Organization.logo` and `Organization.logo.contentUrl` reference `https://iptvpix.com/icon.svg` → **HTTP 404**. The same 404 URL is the only `Product.image` on `/abonnements`. The actual favicon is served from a different, working route (`/icon?703a…`, 200). Google cannot render a broken logo in brand panels or a broken product image in shopping-style rich results. `/favicon.ico` also 404s (harmless for the `<link rel="icon">` tag, but worth shipping for legacy fetchers).
2. **Split Product entities on `/abonnements`:** one `Product` carries the four `Offer`s (19–89 €), a *second, separate* `Product` carries `aggregateRating` (4.7, 6 reviews) and the review bodies. As independent nodes they won't be merged — the offer-bearing product has no rating and the rated product has no offers. Merge into a single `Product` (one `@id`), keeping `offers` + `aggregateRating` + `review` together. Note: the six reviews are first-party; Google may ignore self-serving review markup on Organization-level entities — keep it on the Product and ensure reviews genuinely exist on-page.
3. **Missing schema by page type:**

| Page type | Has | Missing / recommended |
|---|---|---|
| Homepage | Organization, WebSite | `BreadcrumbList` n/a; consider `FAQPage` (an FAQ section exists on-page)¹ |
| Landing pages (18) | Breadcrumb on only 7/18; Article on 5; Product on 2; HowTo on 1 | `BreadcrumbList` on the remaining 11; `Article` or `WebPage` consistently; `FAQPage` where FAQs exist¹ |
| `/blog` index | Organization, WebSite only | `Blog` or `CollectionPage` + `BreadcrumbList` |
| Blog posts (51) | BlogPosting + Breadcrumb ✅ | — (complete) |
| `/abonnements` | Product ×2, Breadcrumb | Merge Products (above); `Offer.url` currently points to robots-blocked `/checkout` URLs — acceptable, but consider pointing to `/abonnements` anchors |

¹ Google now shows FAQ rich results only for well-known authoritative sites, but valid `FAQPage` markup still helps entity understanding and AI-assistant/LLM answer surfacing — which this site explicitly courts via its robots.txt policy.

### 4.5 Internal Linking

The link graph (2,610 internal links across 71 pages) is dominated by the sitewide header/footer: **every** page in the main nav+footer receives ~70 inlinks. The result:

- **Link-equity hoarders:** `/politique-de-confidentialite`, `/politique-de-remboursement` and `/presse-media` each receive 70 inlinks — exactly as many as the revenue pages `/abonnements` and `/installation`. Utility pages don't need sitewide equity; money pages should stand out. Consider trimming footer links on blog templates or adding contextual in-body links to `/abonnements` (currently blog posts link to it only via the shared nav).
- **Under-linked key content:** 15 blog posts have exactly **1** inlink (the `/blog` index) — including several of the newest, highest-quality pieces (`iptv-france-2026-guide-complet`, `meilleur-iptv-france-test-2026`, `ligue1-iptv-2026`, `coupe-du-monde-2026-streaming`, `iptv-smarters-pro-vs-tivimate`). There is no related-posts module; adding 3–4 contextual related links per post would lift every post to ≥4 inlinks and shorten discovery paths.
- **`/a-propos`: 0 inlinks** (see §4.1) — add it to the footer and to author bylines on posts.
- A meaningful share of existing in-body links are **wasted on 404 targets** (66+ links, §4.1) — every one is leaked equity until fixed.

### 4.6 Content Duplication & Cannibalization (affects indexability)

The blog contains large clusters of posts written for the same query with near-identical slugs, each self-canonicalised (verified) — so Google must pick a winner among the site's own pages on every query:

- **"IPTV légal France" cluster — 13 URLs** (`/iptv-legal-france`, `/blog/iptv-legal-france`, `/blog/iptv-legal-france-2`, `/blog/iptv-legal-en-france`, `/blog/iptv-legal-en-france-2`, `/blog/iptv-legalite-france`, `/blog/iptv-legal-ou-illegal-en-france`, `/blog/iptv-legal-france-prix`, `/blog/iptv-legal-france-gratuit`, `/blog/iptv-interdit-en-france`, plus amende variants)
- **Generic "IPTV France" cluster — 10 URLs** (`/blog/iptv-france`, `/blog/iptv-france-2`, `/blog/iptv-en-france`, `/blog/tv-iptv-france`, `/blog/premium-iptv-france`, `/blog/france-iptv-pro`, avis/reddit/pas-cher variants)
- **"Meilleur IPTV" cluster — 7 URLs**, **M3U — 3 URLs**, **Firestick — 4 URLs**, **Samsung/Smart TV — 3 URLs**, **IPTV apps — 5 URLs**

The `-2` suffixed slugs (`iptv-france-2`, `iptv-legal-france-2`, `iptv-legal-en-france-2`) are the clearest signal these were generated in bulk without a keyword map. **Recommendation:** for each cluster, pick one canonical winner (usually the landing page, e.g. `/iptv-legal-france`), merge unique value from the satellites into it, then 301 the satellites (or `rel=canonical` them to the winner where content must remain). Expect this to consolidate 30+ competing URLs into ~8 strong ones.

### 4.7 Mobile Usability

All 71 indexable pages ship `width=device-width, initial-scale=1` viewports; Lighthouse tap-target and font-size audits pass on every tested template; layout is responsive with near-zero CLS; content is fully server-rendered (identical for JS-off crawlers). Two persistent, sitewide accessibility failures — insufficient **color contrast** and **non-sequential heading order** (plus a label/accessible-name mismatch on interactive controls) — are UX/compliance issues rather than ranking factors, but heading order also affects how crawlers outline the page. No mobile-blocking issues found.

### 4.8 HTTPS & Security

Excellent across the board — no action needed beyond the redirect-chain fix:

- TLS 1.3, valid Let's Encrypt wildcard cert (`*.iptvpix.com` + apex, expires 16 Aug 2026 — ensure auto-renewal is active)
- HTTP→HTTPS enforced via 308; HSTS `max-age=63072000; includeSubDomains; preload`
- Strong `Content-Security-Policy` including `upgrade-insecure-requests`, `frame-ancestors 'self'`; `X-Content-Type-Options: nosniff`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` all set
- Zero mixed content found in any crawled page
- Served over HTTP/2 with edge caching (Vercel)

---

## 5. 30-Day Roadmap

**Week 1 — Stop the bleeding (dev: ~1–2 days total)**
1. Fix canonicals on `/blog`, `/iptv-acheter`, `/box-iptv`, `/pandora-iptv` → self-referencing. Remove (or correctly implement) hreflang.
2. Ship `/icon.svg` (and `/favicon.ico`), or point all JSON-LD `logo`/`image` fields at the working icon route / a proper 512×512 PNG logo.
3. Fix the 66 broken links: create `/contact` (a contact page is expected by users and by Google for trust) or retarget those links; remove/retarget `/offres` and `/villes/*` links; 301 `/iptv-firestick-france` → `/blog/iptv-firestick-france` and `/iptv-legal-france-gratuit` → `/blog/iptv-legal-france-gratuit`.
4. Add footer + author-byline links to `/a-propos`.
5. Collapse the `http://www` redirect chain to a single hop.

**Week 2 — Structured data & sitemap (dev: ~1 day)**
6. Merge the two `Product` entities on `/abonnements` into one (offers + rating + reviews).
7. Add `BreadcrumbList` to the 11 landing pages missing it; add `Blog`/`CollectionPage` to `/blog`; add `FAQPage` to home and `/abonnements`.
8. Emit real per-URL `<lastmod>` values in the sitemap (from content updated-at, not build time).
9. Pull Search Console + CrUX field data to validate lab CWV findings and establish the baseline.

**Week 3 — Homepage performance (dev: ~2–3 days)**
10. Defer or remove gtag.js (Plausible already installed); load any remaining tags on first interaction.
11. Reduce homepage hydration cost: convert static sections to server components, `next/dynamic` below-the-fold widgets, trim the 503 KB document toward ≤250 KB.
12. Re-run Lighthouse; target mobile LCP < 2.5 s, TBT < 200 ms.

**Week 4 — Content consolidation & internal links (content + dev: ongoing)**
13. Build the keyword map; for each cannibalization cluster pick one winner, merge and 301 the satellites (start with the 13-page "IPTV légal" cluster and the three `-2` slugs).
14. Add a related-posts module (3–4 contextual links) to the blog template; add one in-body link to `/abonnements` from each commercial-intent post.
15. Rewrite the ~20 worst over-length titles (≤60 chars) and descriptions (≤160 chars), starting with money pages.
16. Set up monitoring: GSC index-coverage checks on the four re-canonicalised pages, CWV field-data tracking, and a monthly broken-link crawl.

---

## 6. Verification Log

Per the audit protocol, the five highest-priority findings were re-verified against the live site immediately before this report was finalized (9 July 2026):

| Finding | Re-verification result |
|---|---|
| 1. Canonicals → homepage on `/blog`, `/iptv-acheter`, `/box-iptv`, `/pandora-iptv` | ✅ **Confirmed live** — all four return `<link rel="canonical" href="https://iptvpix.com">`; control page `/meilleur-abonnement-iptv` correctly self-references |
| 2. `icon.svg` 404 while referenced in JSON-LD | ✅ **Confirmed live** — `/icon.svg` → 404; live homepage JSON-LD references it 4× (logo, contentUrl); `/abonnements` Product image references it |
| 3. 66+ internal links to 404 targets | ✅ **Confirmed live** — all six target URLs return 404; sampled live blog page contains `href="/contact"`, `href="/offres"`, `href="/villes/paris"` |
| 4. `/a-propos` orphan | ✅ **Confirmed live** — page returns 200 and is in the sitemap; no `href="/a-propos"` found in homepage, `/abonnements`, or sampled blog post HTML |
| 5. Homepage mobile CWV (LCP 3.2–3.4 s, heavy JS) | ✅ **Confirmed in lab, twice** (LCP 3.4 s / 3.2 s; main-thread 5.2 s / 4.6 s) — ⚠️ **lab data only; could not be confirmed against real-user field data** (see below) |

**What could not be confirmed, and why:**

- **Field Core Web Vitals (CrUX):** Google's PageSpeed Insights/CrUX API quota was unavailable from the audit environment. Lab results were consistent across repeat runs, but real-user LCP/INP/CLS should be validated in Search Console → Core Web Vitals before and after the Week-3 work.
- **Homepage TBT exact value:** varied 360 ms–1,780 ms between lab runs (main-thread work was consistently ~5 s). Treat TBT direction, not the single number, as the finding.
- **Index status / traffic impact:** without Search Console access, the *actual* indexation state of the four mis-canonicalised pages and the cannibalization clusters' query-level performance could not be observed — only the on-site signals. GSC's URL Inspection and Performance reports should be checked when implementing fixes #1 and the Week-4 consolidation.
- Early test-run anomalies (a "missing `<title>`" and "invalid robots.txt" reading on `/abonnements` and `/installation`) were traced to the audit harness, re-tested, and **excluded** — both pages verifiably ship correct titles, descriptions and lang attributes (SEO score 100 on re-run).

---

## Appendix — Methodology

- **Crawler:** custom BFS crawler (mobile Chrome UA), 77 URLs fetched, capturing status codes, redirect chains, canonicals, meta robots, X-Robots-Tag, titles/descriptions/H1s, hreflang, viewport, JSON-LD, word counts, image alts, and the full internal-link edge list (2,610 edges).
- **Sitemap/robots analysis:** `robots.txt`, `sitemap.xml` (67 URLs), `blog/rss.xml` cross-referenced against the crawl to detect orphans and non-sitemap URLs.
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile, simulated slow-4G throttling), 4 templates × mobile + homepage desktop, unstable pages re-run up to 3×. One environment caveat: audits ran through a local TLS relay required by the audit sandbox; the relay forces HTTP/1.1, so Lighthouse's "Use HTTP/2" advisory was discarded as an artifact (the live site serves HTTP/2 — verified directly with curl).
- **Verification:** every P0/P1 finding re-tested with independent live requests before publication (§6).
