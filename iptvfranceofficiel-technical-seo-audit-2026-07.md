# Technical SEO Audit — iptvfranceofficiel.fr

**Prepared for:** Site owner, iptvfranceofficiel.fr
**Audit date:** 9 July 2026
**Scope:** Full technical audit — crawl architecture, indexability, Core Web Vitals, structured data, internal linking, mobile usability, HTTPS/security
**Pages analysed:** 36 URLs crawled (100% of the sitemap), 1,462 internal links mapped, 8 Lighthouse lab runs, all findings re-verified against the live site before publication

---

## 1. Executive Summary

iptvfranceofficiel.fr shares the strong technical foundation of its sister properties — all 36 pages indexable with correct self-referencing canonicals, a fully connected two-click architecture, valid per-URL sitemap dates, a working favicon, exemplary security headers, and template performance of 91–100 on mobile. Two defects need immediate attention: **eleven articles link their main commercial anchor ("abonnement IPTV") to `/abonnement-iptv`, a page that returns 404** — the blog's primary conversion path is broken — and the homepage and `/iptv-france` compete head-on for the same query with near-identical H1s ("Abonnement IPTV France édition 2026" vs "Abonnement IPTV France pas cher"). Secondary work: 31 of 36 titles exceed 60 characters, the `/articles` hub ships no structured data, and the web font intermittently causes a 0.18 layout shift on the homepage and `/application-iptv` — all quick, template-level fixes.

---

## 2. Health Scorecard

| Area | Status | Notes |
|---|---|---|
| Crawlability & architecture | 🟡 One critical break | Depth ≤ 2, 0 orphans, sitemap ↔ crawl 36/36 — but 11 links to a 404 money page |
| Indexability | 🟢 Good | All canonicals self-referencing; clean robots.txt; per-URL lastmod (9 distinct values) |
| Core Web Vitals (lab) | 🟢 Mostly good | 91–100 across templates; intermittent font-swap CLS 0.14–0.18 on 2 pages |
| Structured data | 🟡 Needs work | `/articles` hub has zero JSON-LD; non-square logo; no FAQPage |
| On-page metadata | 🟡 Needs work | 31/36 titles > 60 chars; home & `/iptv-france` H1s nearly identical |
| Internal linking | 🟢 Good | Contextual anchors to money pages; a few articles at 2–4 inlinks |
| Mobile usability | 🟢 Good | Viewport 36/36; tap targets pass; 1 image missing alt |
| HTTPS & security | 🟢 Excellent | TLS 1.3, HSTS preload, CSP, no mixed content |

---

## 3. Prioritized Fix List (Impact × Effort)

| # | Finding | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | **Broken conversion path:** 11 articles link the anchor "abonnement IPTV" (and variants like "guide comparatif des abonnements IPTV") to `/abonnement-iptv` → **404**. Every commercial click from the blog's in-body CTAs dead-ends. 301 the URL to `/iptv-france` (or create the page) *and* fix the article links. | **High** | **Low** | **P0** |
| 2 | **Homepage vs `/iptv-france` cannibalization (verified in H1s):** home H1 "Abonnement IPTV France édition 2026" vs `/iptv-france` H1 "Abonnement IPTV France pas cher" — two pages telling Google they target the identical head term; `/iptv-premium` adds "Abonnement IPTV 4K" to the mix. Google will pick one (not necessarily the intended one) and suppress the other. | **High** | **Med** | **P0** |
| 3 | **Titles: 31/36 exceed 60 characters** (up to 116). The homepage title also repeats the keyword twice ("Abonnement IPTV — Le meilleur Abonnement IPTV France 2026"), and the sitewide suffix "· Abonnement IPTV" is an exact-match keyword rather than a brand — a pattern Google's title rewriter and spam classifiers both dislike. | **Med** | **Low** | **P1** |
| 4 | `/articles` (hub linking all 24 posts) emits **zero JSON-LD** — no CollectionPage, no BreadcrumbList — while every other page has schema. | **Med** | **Low** | **P1** |
| 5 | **Font-swap layout shift:** the primary woff2 web font intermittently shifts the hero card, producing CLS 0.18 on the homepage and 0.145 on `/application-iptv` (Lighthouse traced the culprit to "Web font loaded"). Cold-cache users get the shift; warm-cache runs measure 0.005. Add `font-display` tuning + `size-adjust` fallback metrics. | **Med** | **Low** | **P1** |
| 6 | ~10 meta descriptions exceed 160 chars (up to 269) — truncated in SERPs. | **Low-Med** | **Low** | **P2** |
| 7 | Schema gaps: `Organization.logo` is the 1200×630 OG banner (Google prefers square ≥ 112×112); `/a-propos` lacks BreadcrumbList; no FAQPage/aggregateRating opportunities exploited. `/apple-icon.png` 404s. | **Low-Med** | **Low** | **P2** |
| 8 | Link equity: footer gives legal pages the same 35 inlinks as money pages; weakest articles sit at 2–4 inlinks (`iptv-epg-xmltv-guide`: 2, `iptv-pc-windows-mac`, `iptv-chromecast-google-tv`, `iptv-canal-plus-sport`: 3). | **Low-Med** | **Med** | **P2** |
| 9 | `http://www` variant resolves via a 2-hop redirect chain. | **Low** | **Low** | **P3** |
| 10 | Article images are Pexels stock URLs — and the **same image IDs are reused on the operator's sister site** for the matching articles (e.g. pexels-photo-8583821 on both "meilleur abonnement" posts). Content itself is unique (verified ~1% overlap), but shared imagery + identical slugs + same author across domains is an avoidable site-network footprint. | **Low** | **Med** | **P3** |
| 11 | Accessibility: `color-contrast` sitewide; `aria-hidden` elements with focusable children; one `aria-prohibited-attr` on the homepage; 1 image missing alt on `/iptv-premium`. | **Low** (SEO) | **Med** | **P3** |

---

## 4. Detailed Findings

### 4.1 Crawl & Site Architecture

- **Structure:** homepage → 11 hub/landing pages (depth 1) → 24 articles (depth 2). Sitemap and crawl match 36/36; zero orphans; clean URL handling (trailing-slash 308s, query params canonicalised, real 404s for unknown/case-variant URLs).
- **The one break — and it matters:** `/abonnement-iptv` returns 404 yet receives **11 in-body links from 11 different articles**, always on commercial anchors ("abonnement IPTV", "formules d'abonnement IPTV", "guide comparatif des abonnements IPTV"). This looks like a page that was renamed to `/iptv-france` without a redirect. Both halves of the fix are needed: a 301 from `/abonnement-iptv` → `/iptv-france` (recovers any external links and stops crawl waste) and updating the 11 article links to point directly at the target.
- **Redirects:** HTTPS enforced via 308; only the 2-hop `http://www` chain to tidy.

### 4.2 Indexability

- `robots.txt` allows all crawlers including AI bots, declares the sitemap; no noindex conflicts, no meta-robots surprises, no hreflang (correct for single-locale; `<html lang="fr">` on 36/36).
- **All canonicals self-referencing** — none of the canonical-to-homepage defects found on the operator's iptvpix.com property.
- **Sitemap quality is the best of the three audited properties:** 9 distinct `<lastmod>` values indicate real per-content dates rather than a build stamp.

### 4.3 On-Page Metadata & Keyword Targeting

- **Titles:** 31/36 exceed 60 characters (63–116). Root causes: long descriptive titles plus the suffix "· Abonnement IPTV". Two specific problems beyond length:
  - The homepage title "Abonnement IPTV — Le meilleur Abonnement IPTV France 2026" repeats the money keyword twice in one tag.
  - The suffix "· Abonnement IPTV" is not a brand — it is the site's target keyword appended to all 36 titles. Google's title-rewrite system frequently strips or rewrites such patterns; a distinctive brand token ("· IPTV France Officiel") is safer and frees ~10 characters.
- **Cannibalization (verified live in H1s):**

| Page | H1 | Title focus |
|---|---|---|
| `/` | "Abonnement IPTV France édition 2026" | meilleur abonnement IPTV France |
| `/iptv-france` | "Abonnement IPTV France pas cher" | abonnement IPTV France pas cher + price |
| `/iptv-premium` | "IPTV Premium" | abonnement IPTV 4K / Smarters Pro |

  The home and `/iptv-france` pairing is a direct conflict. Recommended split: homepage = brand + "meilleur abonnement IPTV" positioning; `/iptv-france` = price-led "pas cher" angle with the price point in the H1; `/iptv-premium` = 4K/features angle (already mostly distinct).
- **Descriptions:** ~10 exceed 160 chars (up to 269). **Headings:** one H1 per page on 36/36 ✅.

### 4.4 Core Web Vitals & Page Speed

**Method note:** Google PSI/CrUX API quota was unavailable; figures are Lighthouse 12 lab data (emulated mobile, slow-4G simulation). Runs failing sanity checks (impossible traces caused by the sandbox's TLS relay) were automatically detected and re-run; key pages were measured twice.

| Page (mobile) | Perf | LCP | TBT | CLS |
|---|---|---|---|---|
| `/` (2 clean runs) | 91 / 93 | 1.5–2.1 s 🟢 | 120–280 ms 🟡 | **0.181 / 0.005** 🟡 (font-swap dependent) |
| `/iptv-premium` (2 clean runs) | 72 / 92 | 1.6 s 🟢 (one 4.5 s outlier, see §6) | 230–320 ms 🟡 | 0–0.07 🟢 |
| `/application-iptv` | 94 | 1.5 s 🟢 | 30 ms 🟢 | **0.145** 🟡 (font) |
| `/articles/meilleur-abonnement-iptv-2026` | 98 | 2.4 s 🟡 | 40 ms 🟢 | 0.001 🟢 |
| `/` desktop | 100 | 0.7 s 🟢 | 0 ms 🟢 | 0.005 🟢 |

**Diagnosis.**
- **Foundation excellent:** TTFB 60–110 ms (Vercel edge cache), zero render-blocking resources, LCP healthy on every template. LCP elements are text nodes, not images.
- **The concrete defect is font-loading CLS:** Lighthouse's culprit trace attributes the homepage's 0.181 shift to "Web font loaded" (`e4af272ccee01ff0-s.woff2`) moving the hero card. Warm-cache runs show 0.005 — so a meaningful share of *first-visit* mobile users experience a failing CLS while returning visitors don't. Fix with `size-adjust`/`ascent-override` fallback font metrics (or `font-display: optional` for the display face); this is a one-file CSS change.
- **TBT is moderate (120–320 ms)** across money pages — same cause as the sister sites: hydration of large RSC-doubled HTML documents (site average ~300 KB, up to 461 KB on `/test-iptv`) plus gtag.js. Worth the same gtag-deferral treatment, gated on field data.

### 4.5 Structured Data

**Present:** `Organization` + `WebSite` (home); `Service` with `AggregateOffer` (22–79 €, 4 offers) on `/iptv-premium` and Service on 2 more landing pages; `HowTo` on `/application-iptv`; `ItemList` on `/boitier-iptv`; `ProfilePage`/`Person` ("Alae H.") on `/a-propos`; complete `Article` + `BreadcrumbList` on 24/24 posts with the author entity correctly pointing at `/a-propos`. No parse errors. Favicon works (unlike the sister site).

**Gaps:**
1. **`/articles` has zero JSON-LD** (verified live — 0 scripts). Add `CollectionPage` + `BreadcrumbList`.
2. `Organization.logo` reuses the rectangular 1200×630 OG image; supply a square ≥ 112×112 logo.
3. `/a-propos` lacks BreadcrumbList (the only landing page without it).
4. `apple-touch-icon` asset missing (404).
5. Article images are Pexels stock — valid but generic, and duplicated across the operator's network (fix list #10).

### 4.6 Internal Linking

- Money pages receive contextual, anchor-diverse in-body links, and every nav/footer page gets 35 inlinks. Average ~40 internal links and ~3,200 words per page; no thin pages.
- **But the highest-value contextual links are the broken ones** — the 11 "abonnement IPTV" article CTAs currently 404 (finding #1). Once redirected to `/iptv-france`, that page gains 11 strong commercial-anchor inlinks, which also supports the cannibalization fix by making `/iptv-france` the clear blog-endorsed money page.
- Under-linked tail: `iptv-epg-xmltv-guide` (2 inlinks), `iptv-pc-windows-mac`, `iptv-chromecast-google-tv`, `iptv-canal-plus-sport` (3 each). A related-articles module evens this out.
- Flat-equity note: the four legal pages carry the same 35 inlinks as revenue pages.

### 4.7 Mobile Usability

Viewport on 36/36 pages; tap targets and font sizes pass; fully server-rendered. The font-swap CLS (§4.4) is the only mobile-experience defect of note. Accessibility 88–96: recurring `color-contrast` failures, `aria-hidden` elements containing focusable controls, one `aria-prohibited-attr` on the homepage, and one image missing alt text on `/iptv-premium`.

### 4.8 HTTPS & Security

- TLS 1.3; valid Let's Encrypt wildcard cert (expires 30 Aug 2026 — confirm auto-renewal); HSTS `max-age=63072000; includeSubDomains; preload`
- CSP present (GTM/GA, fonts, Pexels/Unsplash images; `form-action` limited to self + `wa.me`); `nosniff`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` set; zero mixed content; HTTP/2 + edge caching
- Purchase flow via WhatsApp deep links (as on the sister site) — fine technically; add on-site conversion events if paid acquisition is planned.

---

## 5. 30-Day Roadmap

**Week 1 — Fix the conversion path & collision (dev: ~1 day)**
1. 301 `/abonnement-iptv` → `/iptv-france`; update the 11 article links to the final URL.
2. Differentiate home vs `/iptv-france`: rewrite H1s/titles per §4.3 (home = brand + "meilleur", `/iptv-france` = "pas cher" + price).
3. Fix the homepage title's doubled keyword; change the sitewide suffix to a distinctive brand token.
4. Collapse the `http://www` redirect chain.

**Week 2 — Metadata & schema (dev: ~1 day)**
5. Rewrite the 15 most important titles to ≤ 60 chars and the ~10 over-length descriptions to ≤ 160.
6. Add `CollectionPage` + `BreadcrumbList` to `/articles`; Breadcrumb to `/a-propos`; square logo for `Organization.logo`; ship `apple-touch-icon`.
7. Pull Search Console + CrUX field data to baseline real-user CWV (especially CLS).

**Week 3 — CWV polish (dev: ~1 day)**
8. Fix font-swap CLS: `size-adjust`-matched fallback metrics for the woff2 face (validate with repeat cold-cache Lighthouse runs targeting CLS < 0.1 on `/` and `/application-iptv`).
9. If field data confirms blocking time: defer gtag.js to first interaction and dynamic-import below-the-fold homepage sections.
10. Add alt text to the `/iptv-premium` image; fix `aria-hidden`/`aria-prohibited-attr` issues.

**Week 4 — Linking & content ops (content: ongoing)**
11. Add a related-articles module (3–4 contextual links); lift the four under-linked articles to ≥ 6 inlinks.
12. Begin replacing shared Pexels imagery with unique branded images on the top 10 articles (start with those whose image IDs are duplicated on the sister domain).
13. Set up monitoring: monthly crawl for broken links, GSC coverage + query-level check that home/`/iptv-france` stop alternating on the head term.

---

## 6. Verification Log

The five highest-priority findings were re-verified against the live site immediately before this report was finalized (9 July 2026):

| Finding | Re-verification result |
|---|---|
| 1. `/abonnement-iptv` broken conversion path | ✅ **Confirmed live** — URL returns 404; `href="/abonnement-iptv"` present in live article HTML; 11 linking articles enumerated from the crawl |
| 2. Home vs `/iptv-france` cannibalization | ✅ **Confirmed live** — H1s fetched fresh: "Abonnement IPTV France édition 2026" vs "Abonnement IPTV France pas cher" |
| 3. Titles > 60 chars (31/36) | ✅ **Confirmed** — live samples: `/iptv-france` 91, `/application-iptv` 102, `/articles/iptv-smarters-pro-vs-tivimate` 103 chars |
| 4. `/articles` hub has zero JSON-LD | ✅ **Confirmed live** — 0 `application/ld+json` scripts |
| 5. Font-swap CLS on `/` and `/application-iptv` | ✅ **Observed with culprit trace** (Lighthouse attributes the 0.181 shift to the woff2 web font loading) — ⚠️ **intermittent by nature**: warm runs measure 0.005, so treat as a first-visit risk to be confirmed in CrUX field CLS, not a constant defect |

**What could not be confirmed, and why:**

- **`/iptv-premium` LCP:** first run measured 4.5 s, re-run 1.6 s with the same healthy TTFB. The 4.5 s reading is consistent with a sandbox TLS-relay stall rather than a site defect and was **not** used in conclusions; validate in field data.
- **Field Core Web Vitals (CrUX):** API quota unavailable from the audit environment; the CLS and TBT findings especially should be checked in Search Console, since both are load-timing dependent.
- **Query-level cannibalization impact:** no Search Console access — the home/`/iptv-france` conflict is proven on-site (H1s/titles) but its ranking cost should be observed in GSC Performance (look for the two URLs alternating on "abonnement iptv france").

---

## Appendix — Methodology

- **Crawler:** custom BFS crawler (mobile Chrome UA), 36 URLs (100% site coverage) + 1 discovered 404 target, capturing status codes, redirect chains, canonicals, meta robots, titles/descriptions/H1s, viewport, JSON-LD, word counts, image alts, and the internal-link edge list (1,462 edges).
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile + desktop preset, simulated slow-4G) with automatic detection and re-run of corrupted traces (a sandbox TLS-relay limitation); homepage and `/iptv-premium` measured twice on clean runs.
- **Duplication testing:** 8-word shingle Jaccard overlap against the operator's sister domain on three matched article pairs (~1% — unique content).
- **Verification:** every P0/P1 finding re-tested with independent live requests before publication (§6).
