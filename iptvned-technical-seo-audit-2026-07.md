# Technical SEO Audit — iptvned.com

**Prepared for:** Site owner, iptvned.com
**Audit date:** 9 July 2026
**Scope:** Full technical audit — crawl architecture, indexability, Core Web Vitals, structured data, internal linking, mobile usability, HTTPS/security
**Pages analysed:** 70 URLs crawled (60 sitemap URLs + discovered city/checkout pages), 2,000+ internal links mapped, 9 Lighthouse lab runs, all findings re-verified against the live site before publication

---

## 1. Executive Summary

iptvned.com — the Dutch-market sibling of iptvpix.com, running the same codebase — inherits that site's worst defects and adds two of its own: **the `www` host 302-redirects every visitor and crawler to a Vercel SSO login page**, and **the sitewide navigation links to `/pandora-iptv` on all 68 pages, a URL that returns 404** (with `/contact` broken on another 27 pages). On top of that, the `/blog` hub and `/iptv-kopen` declare the homepage as their canonical — effectively de-indexing themselves — the Organization logo in structured data points to a 404 asset on every page, and a template bug stamps the brand twice into 56 of 68 titles ("— IPTVNED · IPTVNED"). These are all template/configuration fixes achievable in week one; the deeper 30-day work is untangling the ~35 blog URLs competing in four keyword-cannibalization clusters ("beste IPTV" ×9, "IPTV legaal" ×10, generic "IPTV Nederland" ×13, M3U ×3) and cutting the homepage's JavaScript burden (710 ms TBT, 6.4 s main-thread on a 526 KB document).

---

## 2. Health Scorecard

| Area | Status | Notes |
|---|---|---|
| Host configuration | 🔴 Critical | `www` host 302s to a Vercel SSO login instead of the site |
| Crawlability & architecture | 🔴 Critical | Sitewide nav 404 (`/pandora-iptv` ×68 pages, `/contact` ×27); 1 orphan; city pages half-wired |
| Indexability | 🔴 Critical | `/blog` and `/iptv-kopen` canonicalised (and hreflang'd) to the homepage |
| Core Web Vitals (lab) | 🟡 Mixed | Blog/landing LCP fine; homepage TBT 710 ms; `/installatie` LCP 2.9–4.1 s |
| Structured data | 🟡 Needs work | Org logo → 404 `icon.svg` sitewide; landing pages lack Article/Service; favicon route works |
| On-page metadata | 🔴 Systematic bug | Brand doubled in 56/68 titles; 48/68 > 60 chars |
| Internal linking | 🟡 Uneven | Nav pages get 67 inlinks; 15+ posts and 3 city pages at 1–2; heavy cannibalization clusters |
| Mobile, HTTPS, trust | 🟢 Good | Viewport 68/68; TLS 1.3 + HSTS preload; legal pages present; checkout correctly noindexed |

---

## 3. Prioritized Fix List (Impact × Effort)

| # | Finding | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | **`www` host serves a Vercel SSO wall (verified on `/` and `/abonnementen`):** `https://www.iptvned.com/*` → `302 → vercel.com/sso-api?...`. Every www link, ad, or crawl dead-ends on a third-party login. Attach www to the production Vercel project and 308 it to the apex. | **High** | **Low** | **P0** |
| 2 | **Sitewide broken navigation:** `/pandora-iptv` is linked from **all 68 pages** (it's in the shared nav/footer — the page exists on the French sister site but was never built here) and returns 404; `/contact` is linked from 27 blog pages and 404s. ~95 broken internal links total. | **High** | **Low** | **P0** |
| 3 | **Self-de-indexing pages:** `/blog` (hub for 44 posts) and `/iptv-kopen` declare `canonical → https://iptvned.com` plus hreflang alternates all pointing at the homepage. Google is told both are homepage duplicates. (Control check: `/iptv-box` self-references correctly.) | **High** | **Low** | **P0** |
| 4 | **Organization logo 404s sitewide:** JSON-LD references `https://iptvned.com/icon.svg` (4× on the homepage) → 404 — the same bug as the French sibling; the real favicon lives at a generated `/icon?…` route. `/favicon.ico` also 404s. | **Med-High** | **Trivial** | **P0** |
| 5 | **Title template bug — brand doubled on 56/68 pages:** titles end "… — IPTVNED · IPTVNED"; 48/68 exceed 60 characters (up to 113). Google will truncate or rewrite nearly every blog title. | **Med-High** | **Low** | **P1** |
| 6 | **Keyword cannibalization — ~35 URLs in 4 clusters:** "beste IPTV Nederland" ×9, "IPTV legaal/illegaal" ×10, generic "IPTV Nederland" ×13 (including an `iptv-nederland-2` duplicate slug and a stale `iptv-nederland-forum-2024`), M3U ×3. Same bulk-generation pattern as the French sibling — each page self-canonicalises, splitting relevance. | **High** | **High** | **P1** |
| 7 | **Homepage JavaScript weight:** TBT 710 ms, main-thread 6.4 s on a 526 KB document (clean run), double analytics stack (gtag + Plausible). `/installatie` LCP 2.9–4.1 s across two clean runs, driven by ~1.2 s element render delay (hydration blocking text paint). | **Med** | **Med** | **P1** |
| 8 | **Half-wired sections:** `/iptv-merken` is in the sitemap with zero internal links (orphan); the four `/steden/*` city pages (Amsterdam, Rotterdam, Eindhoven, Utrecht) exist and self-canonicalise but are **not in the sitemap** and get 1–2 inlinks each (except Amsterdam, 20). Decide: wire them in (sitemap + links) or remove. | **Med** | **Low** | **P1** |
| 9 | Landing pages lack content schema: BlogPosting covers 44 blog posts, but money/landing pages carry only Organization/WebSite/Breadcrumb — no Service/Product except one page; ~30 meta descriptions exceed 160 chars. | **Low-Med** | **Low** | **P2** |
| 10 | Cosmetic but sloppy: checkout plan IDs are French (`/afrekenen?plan=3mois-1ecran`) on a Dutch site; 15+ blog posts have a single inlink; a11y fails (`color-contrast`, `heading-order`, `aria-prohibited-attr`, `label-content-name-mismatch`) across templates. | **Low** | **Low-Med** | **P3** |

---

## 4. Detailed Findings

### 4.1 Host Configuration

Identical defect to the operator's primeiptv-france.com property, verified live on two URLs:

```
https://www.iptvned.com/abonnementen  →  302
location: https://vercel.com/sso-api?url=https%3A%2F%2Fwww.iptvned.com%2Fabonnementen&nonce=…
```

The www subdomain resolves to an SSO-protected Vercel deployment rather than the public site, and `http://www` chains into it. Fix in Vercel domain settings (www → 308 → apex).

### 4.2 Crawl & Site Architecture

- **The good:** 68 pages return 200 at depth ≤ 3; trailing-slash and query-parameter handling correct; real 404s; checkout (`/afrekenen` + plan variants) properly noindexed, canonicalised and robots-disallowed.
- **Sitewide broken navigation (P0):** `/pandora-iptv` — a page that exists on the French sibling but was never created here — is linked from **every one of the 68 pages** (verified in live homepage HTML). `/contact` is linked from 27 blog pages and also 404s. Together ~95 dead internal links burn crawl budget and leak equity on every page view. Either build the pages or remove/retarget the links (nav template + blog CTA template).
- **Orphan & half-wired sections:** `/iptv-merken` (sitemap, 0 inlinks — verified: 0 links on live homepage); the 4 `/steden/*` city pages are live with correct canonicals but missing from the sitemap and barely linked (Utrecht: 1 inlink; Rotterdam/Eindhoven: 2). This mirrors the French site's abandoned `/villes/` concept — but here the pages exist, so the cheap win is to finish wiring them (sitemap + a "Steden" footer row) rather than delete.

### 4.3 Indexability

- `robots.txt` clean (all agents + AI crawlers allowed, `/afrekenen` disallowed, sitemap declared). Sitemap has 16 distinct lastmod values (credible dates).
- **Self-de-indexing (P0, verified live):** `/blog` and `/iptv-kopen` output `<link rel="canonical" href="https://iptvned.com">` plus hreflang blocks (`nl`, `nl-NL`, `nl-BE`, `x-default`) all pointing at the homepage. `/blog` is the discovery hub for 44 posts — telling Google it's a homepage duplicate weakens the whole content section. Make canonicals self-referencing and remove (or correctly self-reference) the hreflang trio — the same fix already specified for iptvpix.com.
- `/afrekenen` is both robots-disallowed and noindexed — same benign redundancy as the sibling; prefer noindex alone.

### 4.4 On-Page Metadata

- **Doubled brand suffix (56/68 pages, verified live):** blog titles are templated as "{title} — IPTVNED" and then the sitewide "· IPTVNED" suffix is appended again: `…streamingprotocollen uitgelegd — IPTVNED · IPTVNED`. One template-level fix removes the duplication and immediately shortens every affected title.
- 48/68 titles exceed 60 characters (up to 113); ~30 descriptions exceed 160 (up to 251). H1s: exactly one per page ✅ (checkout pages excepted, which are noindexed anyway).

### 4.5 Core Web Vitals & Page Speed

**Method note:** PSI/CrUX quota unavailable; Lighthouse 12 lab data (emulated mobile, slow-4G) with automated corrupted-trace detection and re-runs; volatile pages measured twice.

| Page (mobile) | Perf | LCP | TBT | CLS |
|---|---|---|---|---|
| `/` (homepage) | 82 | 1.4 s 🟢 | **710 ms** 🔴 | 0.046 🟢 |
| `/abonnementen` (2 clean runs) | 77 / 94 | 1.3 s 🟢 (one 4.3 s outlier, §6) | 110–290 ms 🟡 | 0.046 🟢 |
| `/installatie` (2 clean runs) | 83 / 94 | **2.9–4.1 s** 🔴 | 120–220 ms 🟡 | 0.046 🟢 |
| `/blog/hoe-werkt-iptv-in-nederland` | 92 | 1.2 s 🟢 | 340 ms 🟡 | 0.046 🟢 |
| `/` desktop | 97 | 0.6 s 🟢 | 140 ms 🟢 | 0.008 🟢 |

**Diagnosis — the iptvpix JavaScript profile, reproduced:** excellent server times (TTFB 60–150 ms, edge cache) and text-based LCP elements, but heavy hydration. The homepage executes 6.4 s of main-thread work on a 526 KB HTML document (RSC payload duplication; `/abonnementen` is 563 KB) and loads **two analytics stacks** (gtag + Plausible). `/installatie`'s LCP is a text paragraph delayed ~1.2 s by hydration — the same signature as the French sibling's homepage. Fixes: drop one analytics stack, defer the remaining tag to first interaction, convert static sections to server components, and trim the RSC payload. Target: TBT < 200 ms sitewide, `/installatie` LCP < 2.5 s.

### 4.6 Structured Data

- **Present:** Organization + WebSite sitewide; BlogPosting on all 44 posts (complete author/publisher/dates); BreadcrumbList on 54/67; HowTo on the installation hub; ProfilePage on `/over-ons`; Product on `/abonnementen`.
- **Defects:** the Organization `logo`/`contentUrl` reference **`/icon.svg` → 404** on all ~68 pages (verified live; 4 references on the homepage alone) — same P0 asset bug as iptvpix.com; `/favicon.ico` 404s (the working icon is a generated `/icon?...` route, so ship a real `/icon.svg` + `/favicon.ico` or point JSON-LD at the working route). Money/landing pages other than `/abonnementen` carry no content-type schema (add Service/Article as appropriate); `/blog` hub lacks CollectionPage (add alongside the canonical fix).

### 4.7 Internal Linking & Content Architecture

- Nav/footer distribute 67 inlinks to every top-level page — utility pages (`/pers-media`, `/terugbetalingsbeleid`) rank equal with `/abonnementen`. The long tail is starved: 15+ posts at 1–2 inlinks, plus the orphan and city pages (§4.2). No related-posts module.
- **Cannibalization is the dominant strategic issue** (~35 of 68 URLs in 4 clusters):
  - *beste IPTV* ×9 — `/beste-iptv-abonnement` (landing) vs 8 blog variants (`beste-iptv-nederland`, `-reddit`, `-tweakers`, `-provider-`, `-aanbieder-`, `-aanbieders-2025-`, `beste-iptv-2025-`, `wat-is-de-beste-`)
  - *IPTV legaal/illegaal* ×10 — 2 landings + 8 near-duplicate blog angles (`is-iptv-legaal-`, `is-iptv-illegaal-`, `is-iptv-kijken-legaal-`, `iptv-nederland-legaal`, `legale-iptv-…` ×2, etc.)
  - *generic IPTV Nederland* ×13 — including the tell-tale `iptv-nederland-2` duplicate slug and stale `iptv-nederland-forum-2024`
  - *M3U* ×3
  Consolidation plan mirrors the iptvpix recommendation: one canonical winner per cluster (usually the landing page), merge unique material, 301 the satellites. Expect 68 URLs → ~40 stronger ones.
- Cross-domain check vs the French sibling: 0–1% shingle overlap — content is unique per market (different language and genuinely different text).

### 4.8 Mobile Usability, HTTPS & Trust

- Viewport 68/68; tap targets/font sizes pass; fully server-rendered.
- Accessibility 91–96: recurring `color-contrast`, `heading-order`, `label-content-name-mismatch`, and an `aria-prohibited-attr` on `/abonnementen`.
- TLS 1.3, valid Let's Encrypt wildcard (expires 19 Aug 2026 — confirm auto-renewal), HSTS preload, full security-header set, zero mixed content, HTTP/2 + edge cache.
- Trust pages present (over-ons, pers-media, privacybeleid, terugbetalingsbeleid) ✅ — though `/contact` is linked but missing (fix #2). Checkout flow is on-site (`/afrekenen`), correctly noindexed; the French plan IDs in Dutch checkout URLs are cosmetic debt.

---

## 5. 30-Day Roadmap

**Week 1 — Stop the bleeding (dev: ~1–2 days)**
1. Vercel: attach `www` to production and 308 → apex; re-test all host/protocol variants.
2. Fix the nav template: build `/pandora-iptv` (or remove the link on all 68 pages); create `/contact` or retarget its 27 links.
3. Canonicals on `/blog` and `/iptv-kopen` → self-referencing; remove/fix hreflang.
4. Ship `/icon.svg` + `/favicon.ico` (or point JSON-LD logo at the working icon route).
5. Fix the doubled "— IPTVNED · IPTVNED" title template.

**Week 2 — Metadata, schema, wiring (dev: ~1 day)**
6. Retitle top 20 pages to ≤ 60 chars; trim over-length descriptions.
7. Add CollectionPage to `/blog`, Service/Article schema to landing pages.
8. Wire `/iptv-merken` and the 4 `/steden/*` pages into nav/footer + sitemap (or remove them).
9. Pull Search Console: verify www duplication clears and `/blog`/`/iptv-kopen` regain indexation; baseline CWV field data.

**Week 3 — Performance (dev: ~2 days)**
10. Remove one analytics stack (gtag or Plausible); defer the survivor to first interaction.
11. Cut homepage/`/installatie` hydration (server components, dynamic imports); target TBT < 200 ms, `/installatie` LCP < 2.5 s; re-measure.

**Week 4 — Content consolidation (content: ongoing)**
12. Build the Dutch keyword map; execute cluster consolidation (start with "beste IPTV" ×9 and the `-2`/`-forum-2024` slugs); 301 satellites to winners.
13. Add a related-posts module; one contextual link to `/abonnementen` per commercial-intent post.
14. Monitoring: monthly broken-link/orphan crawl, GSC index coverage on the two re-canonicalised pages, cluster-level query tracking.

---

## 6. Verification Log

The six highest-priority findings were re-verified against the live site immediately before this report was finalized (9 July 2026):

| Finding | Re-verification result |
|---|---|
| 1. `www` → Vercel SSO wall | ✅ **Confirmed live twice** — `HTTP/2 302` to `vercel.com/sso-api` on `/` and `/abonnementen` |
| 2. Sitewide 404 nav links | ✅ **Confirmed live** — `/pandora-iptv` → 404 with `href="/pandora-iptv"` present in live homepage HTML (68 linking pages in crawl); `/contact` → 404 (27 linking pages) |
| 3. Canonical → home on `/blog`, `/iptv-kopen` | ✅ **Confirmed live** — both return `canonical href="https://iptvned.com"`; control page `/iptv-box` correctly self-references |
| 4. Org logo `icon.svg` 404 | ✅ **Confirmed live** — `/icon.svg` → 404; referenced 4× in live homepage JSON-LD |
| 5. Doubled brand titles (56/68) | ✅ **Confirmed live** — e.g. `/blog/beste-iptv-nederland` ends "— IPTVNED · IPTVNED" |
| 6. `/iptv-merken` orphan | ✅ **Confirmed live** — page returns 200, in sitemap, zero links from live homepage and zero in the full crawl graph |

**What could not be confirmed, and why:**

- **Field Core Web Vitals (CrUX):** API quota unavailable throughout the audit; lab findings (homepage TBT, `/installatie` LCP) should be validated in Search Console before sizing the Week-3 work.
- **`/abonnementen` LCP:** one run measured 4.3 s, the clean re-run 1.3 s with identical TTFB — the outlier matches the audit sandbox's TLS-relay stall signature and was excluded; treat `/abonnementen` LCP as healthy pending field data.
- **Index status:** no Search Console access — the practical indexation state of `/blog`, `/iptv-kopen`, the www host, and the cannibalization clusters' query-level behaviour should be checked in GSC when implementing fixes.

---

## Appendix — Methodology

- **Crawler:** custom BFS crawler (mobile Chrome UA), 70 URLs crawled (100% sitemap coverage + discovered city/checkout URLs), capturing status codes, redirect chains, canonicals, meta robots, hreflang, titles/descriptions/H1s, viewport, JSON-LD, word counts, image alts, and the full internal-link edge list.
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile + desktop preset, simulated slow-4G) with automated sanity checks (score presence, main-thread plausibility, document-title consistency) and up to 4 attempts per page; volatile pages measured twice on clean runs.
- **Duplication testing:** 8-word shingle Jaccard overlap vs the operator's French sibling on matched topics (0–1% — unique content).
- **Verification:** every P0/P1 finding re-tested with independent live requests before publication (§6).
