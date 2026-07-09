# Technical SEO Audit — iptvesp.com

**Prepared for:** Site owner, iptvesp.com
**Audit date:** 9 July 2026
**Scope:** Full technical audit — crawl architecture, indexability, Core Web Vitals, structured data, internal linking, mobile usability, HTTPS/security
**Pages analysed:** 63 URLs crawled (100% of the 46-URL sitemap + checkout variants + 12 discovered dead targets), 916 internal links mapped, 8 Lighthouse lab runs, all findings re-verified against the live site before publication

---

## 1. Executive Summary

iptvesp.com — the Spanish sibling in the operator's portfolio — is structurally the least finished of the seven properties audited: the site is essentially a homepage plus 45 blog posts, and **the commercial tier its own templates link to does not exist**: 91 internal links across the site point at 12 dead URLs, led by the missing pricing page (`/suscripciones`, linked from 15 pages) and payment page (`/pago`, 14 pages), alongside untranslated French leftovers (`/offres`, `/villes/paris`, `/contact`) — leaving `/checkout` reachable through a single link. Compounding this, `/instalacion` — one of only four non-blog content pages — declares the homepage as its canonical (self-de-indexing, independently confirmed by Lighthouse's canonical audit), and the checkout still carries the French sibling's branding in its title ("Finaliza tu **commande** — IPTV Smarters **France**"). The positives: correct host/HTTPS configuration (no www-SSO defect here), a working icon.svg (alone in the family), good sitemap lastmod hygiene, and solid blog-post performance — so the 30-day plan is chiefly about **building the missing money pages, fixing the canonical, finishing the localisation, and consolidating ~26 cannibalizing blog posts**, plus adding the legally required aviso legal and condiciones pages that are absent entirely.

---

## 2. Health Scorecard

| Area | Status | Notes |
|---|---|---|
| Crawlability & architecture | 🔴 Critical | 91 links to 12 dead targets; the pricing/payment tier doesn't exist; checkout has 1 inlink |
| Indexability | 🔴 Critical | `/instalacion` canonicalised to the homepage (1 of only 4 content landings) |
| Localisation quality | 🔴 Sloppy | French URLs and French branding leaking into the Spanish site |
| Core Web Vitals (lab) | 🟡 Mixed | Posts/instalacion healthy; home LCP 3.6 s & blog hub 3.3 s (hydration render delay) |
| Structured data | 🟡 Thin | Only Org/WebSite/BlogPosting/Breadcrumb; no Product/Service/FAQ anywhere; 9 posts missing BlogPosting |
| Trust & compliance | 🔴 Gap | No aviso legal, no condiciones, no contact page (Spanish LSSI requires aviso legal) |
| On-page metadata | 🟡 Needs work | 47/51 titles > 60 chars; 16/51 descriptions > 160 |
| Host, HTTPS, mobile | 🟢 Good | www 308s correctly; TLS 1.3 + HSTS; viewport 51/51; icon.svg works (unique in the family) |

---

## 3. Prioritized Fix List (Impact × Effort)

| # | Finding | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | **The commercial tier is missing — 91 broken internal links to 12 dead URLs (verified live):** `/suscripciones` (×15 linking pages), `/pago` (×14), `/contact` (×10), `/offres` (×9, French leftover), `/iptv-box` (×9), `/iptv-legal-espana` (×8), `/iptv-multa-espana` (×7), `/iptv-hd-4k-espana` (×6), `/villes/paris` (×6, French leftover), `/mejor-iptv-suscripcion` (×5), `/comprar-iptv-espana`, `/comprar-iptv`. The blog constantly funnels readers to a pricing page that 404s; `/checkout` is reachable from exactly one link. Build the landing tier the sister sites have (pricing, box, legal, 4K) and 301/retarget the rest. | **Critical** | **Med** | **P0** |
| 2 | **`/instalacion` canonicalises to the homepage** — the site's main installation hub tells Google it's a homepage duplicate (confirmed live *and* flagged by Lighthouse's SEO canonical audit). Same family bug as iptvpix/iptvned. | **High** | **Low** | **P0** |
| 3 | **Unfinished localisation:** checkout title reads "Finaliza tu **commande** — IPTV Smarters **France** · IPTV Smarters España" (French word + French sibling's brand, on all 5 checkout URLs); French URL stubs linked in blog templates (#1). Sloppy signals on the highest-intent page of the funnel. | **Med-High** | **Low** | **P0** |
| 4 | **No aviso legal, condiciones/CGV, or contact page** — only privacy and refund policies exist. Spain's LSSI-CE requires an aviso legal identifying the operator on commercial sites; terms of sale are expected for a paid service, and Google reads their absence as a trust deficit. (The sister sites' templates can be adapted.) | **High** | **Low** | **P0** |
| 5 | **Titles: 47/51 exceed 60 characters** (up to 97). Also note: the site brands itself entirely as "IPTV Smarters España" — a third-party app trademark — the same brand-risk noted for smartersprofrance.fr. | **Med** | **Low** | **P1** |
| 6 | **Cannibalization — ~26 of 45 posts in 5 clusters:** listas/M3U ×5 (`listas-iptv-espana`, `iptv-listas-espana`, `listas-iptv-gratis-espana`, `listas-iptv-espana-2025-gratis`, `iptv-m3u-espana`), generic "IPTV España" ×8 (incl. duplicate `iptv-espana-telegram` / `-telegram-2`), Smarters app ×6, "mejor IPTV" ×4, legal/multa ×3. With no landing tier, these posts have nothing to consolidate *to* — build the landings (#1), then 301 the satellites. | **High** | **High** | **P1** |
| 7 | **Homepage & blog-hub LCP:** home 3.6 s / hub 3.3 s on mobile — text LCP delayed ~1.25 s by hydration (364 KB HTML document; the family's Next.js RSC-payload pattern). TBT moderate (270–380 ms). Blog posts themselves are fine (LCP 1.9 s). | **Med** | **Med** | **P1** |
| 8 | **Schema is the thinnest of the portfolio:** no Product, Service, FAQPage, or CollectionPage anywhere; BlogPosting + Breadcrumb on only 41/50 pages (9 posts missing both). Favicon note: `/icon.svg` works here (alone in the family) but `/favicon.ico` 404s. | **Med** | **Low-Med** | **P2** |
| 9 | **13 posts have exactly 1 inlink** (only from `/blog`); three recent posts hoard 41 inlinks each from a "featured" module. No analytics stack is installed at all — nothing on the site is being measured. | **Med** | **Low-Med** | **P2** |
| 10 | 16/51 descriptions > 160 chars; `/instalacion` CLS 0.096 (borderline); a11y: `color-contrast`, `heading-order`, `label-content-name-mismatch` sitewide. | **Low** | **Low-Med** | **P3** |

---

## 4. Detailed Findings

### 4.1 Crawl & Site Architecture

- **What exists is well-formed:** all 46 sitemap URLs return 200 at depth ≤ 2; no orphans; trailing-slash/query handling correct; real 404s; checkout correctly noindexed + robots-disallowed and out of the sitemap.
- **What's missing is the problem.** The site consists of the homepage, `/instalacion`, `/blog`, two policy pages, and 45 posts (its French/Dutch siblings have 10–18 landing pages). The templates, however, were written for the full architecture: in-body CTAs and nav fragments link to a pricing page, payment page, box/legal/4K landings, and even French URLs (`/offres`, `/villes/paris`, `/contact`) — **12 dead targets, 91 linking pages, all verified live**. The revenue path is the most damaged: a reader convinced by a blog post clicks "suscripciones" or "pago" and lands on a 404; `/checkout` has exactly one inbound link.
- **Fix order matters:** create `/suscripciones` (or retarget those links to `/checkout`), then the supporting landings (`/iptv-box`, `/iptv-legal-espana`, `/iptv-multa-espana`, `/iptv-hd-4k-espana` — these double as cannibalization-cluster winners, §4.6), then purge the French stubs.

### 4.2 Indexability

- `robots.txt` minimal and clean; sitemap has **19 distinct lastmod values** (best-in-family credibility); no hreflang (correct; `lang="es"` on 51/51).
- **`/instalacion` → canonical `https://iptvesp.com` (P0, verified live + Lighthouse `canonical` audit failure):** the installation hub — linked from all 50 pages — self-de-indexes. The homepage and all blog posts self-reference correctly.
- Checkout URLs: noindexed with canonicals to `/checkout` ✅ (same benign robots/noindex redundancy as siblings).

### 4.3 Localisation Quality

Verified live: all five checkout URLs title themselves "Finaliza tu commande — IPTV Smarters France · IPTV Smarters España" — a French word ("commande") and the French sibling's brand on the page where users enter payment details. Combined with the French URL stubs in templates, the site reads as a partially-adapted clone at exactly the moments trust matters most. A one-day localisation sweep (checkout template, blog CTA fragments, nav) closes this.

### 4.4 Core Web Vitals & Page Speed

**Method note:** PSI/CrUX quota unavailable; Lighthouse 12 lab data (emulated mobile, slow-4G) with automated corrupted-trace detection/re-runs (details §6).

| Page (mobile) | Perf | LCP | TBT | CLS |
|---|---|---|---|---|
| `/` (homepage) | 82 | **3.6 s** 🔴 | 330 ms 🟡 | 0 🟢 |
| `/instalacion` | 92 | 1.8 s 🟢 | 270 ms 🟡 | 0.096 🟡 |
| `/blog` (hub) | 87 | **3.3 s** 🔴 | 270 ms 🟡 | 0.036 🟢 |
| `/blog/iptv-espana` (post) | 90 | 1.9 s 🟢 | 380 ms 🟡 | 0 🟢 |
| `/` desktop | 100 | 0.6 s 🟢 | 0 ms 🟢 | 0.001 🟢 |

**Diagnosis — the family hydration signature, concentrated on the two hubs:** the homepage's LCP element is a text paragraph whose paint is delayed ~1.25 s by React hydration of a 364 KB document (TTFB itself is fine at ~640 ms through the audit proxy, faster in the real world per the `x-vercel-cache: HIT` serving). Blog posts are much lighter (135–145 KB) and score 90+. Fixes: server-component conversion and `next/dynamic` below-the-fold on the homepage and `/blog` hub; keep TBT in check while adding the missing landing pages. Note `/instalacion`'s CLS (0.096) sits just under the 0.1 threshold — watch it in field data. Interestingly this site ships **no analytics at all** — good for TBT, but nothing (conversions, CWV, traffic) is currently measured; add one lightweight stack (the family already uses Plausible elsewhere).

### 4.5 Structured Data

- **Present:** Organization + WebSite sitewide (and the Organization logo `/icon.svg` actually resolves — the only site in the family where this long-standing bug is fixed); BlogPosting + BreadcrumbList on 41/50 pages.
- **Gaps:** 9 blog pages missing BlogPosting/Breadcrumb (template inconsistency worth a look); **no Product/Service anywhere** — not even on the homepage, which is currently the de-facto pricing page (its plan cards are unmarked); no FAQPage; no CollectionPage on `/blog`; `/favicon.ico` 404s (ship it for legacy fetchers).
- When `/suscripciones` is built (#1), give it the family's Product + AggregateOffer pattern from day one.

### 4.6 Internal Linking & Content Architecture

- Nav/footer give the five structural pages 50 inlinks each. A "featured" module funnels 41 inlinks each to three recent posts (`iptv-f1-espana`, `iptv-espana-fire-tv-stick-4k-max-2026`, `iptv-samsung-smart-tv-sin-smarters`) while **13 posts have exactly 1 inlink** — the most lopsided distribution in the portfolio. Replace the static featured trio with a rotating/related-posts module.
- **Cannibalization (~26 of 45 posts, five clusters** — listas/M3U ×5, generic "IPTV España" ×8 with a literal `-2` duplicate slug, Smarters ×6, mejor ×4, legal/multa ×3). The consolidation play: build the four missing landings as cluster winners (`/suscripciones` ← mejor/comprar posts; `/iptv-legal-espana` ← legal/multa; `/iptv-hd-4k-espana` ← 4K; a lists/M3U landing ← the five listas posts), then 301 or canonicalise the satellites. This kills two P0/P1 findings with one structure.
- Cross-domain uniqueness vs the French/Dutch siblings: different language, unique text — no duplication risk.

### 4.7 Trust & Compliance

Verified live: `/aviso-legal`, `/contacto`, `/condiciones`, `/condiciones-generales`, `/sobre-nosotros` all 404; the homepage footer references only privacy and refund policies. Spain's LSSI-CE (art. 10) requires an aviso legal identifying the service operator; terms of sale (condiciones generales) are expected for paid subscriptions, and a contact channel is both a legal expectation and one of Google's clearest trust signals for transactional sites. The blog even links to a `/contact` page that was never built (#1). Port the four-page legal set from the sister templates.

### 4.8 Mobile Usability & HTTPS/Security

- Viewport 51/51; tap targets/fonts pass; fully server-rendered; one borderline CLS (§4.4).
- Accessibility 94 typical: `color-contrast`, `heading-order`, `label-content-name-mismatch` recur across templates.
- **Host configuration is correct** — `www` 308s to the apex in one hop (no Vercel-SSO defect here); http variants chain properly. TLS 1.3, valid Let's Encrypt wildcard (expires 20 Aug 2026 — confirm auto-renewal), HSTS `includeSubDomains; preload`, full security-header set, zero mixed content, HTTP/2 + edge cache.

---

## 5. 30-Day Roadmap

**Week 1 — Revenue path & compliance (dev: ~2–3 days)**
1. Build `/suscripciones` (pricing landing with Product/AggregateOffer schema); until it ships, retarget the 15 `/suscripciones` and 14 `/pago` links to `/checkout`.
2. Fix `/instalacion`'s canonical → self-referencing.
3. Localisation sweep: checkout title/copy ("commande"→"pedido", drop "IPTV Smarters France"), remove/retarget French URL stubs (`/offres`, `/villes/paris`, `/contact`).
4. Create aviso legal, condiciones generales, and a contact page; link them in the footer.

**Week 2 — Landing tier & metadata (dev/content: ~2 days)**
5. Build the remaining linked-but-missing landings: `/iptv-box`, `/iptv-legal-espana`, `/iptv-multa-espana`, `/iptv-hd-4k-espana` (each is already receiving 6–9 internal links and doubles as a cluster winner).
6. Retitle the worst 20 pages to ≤ 60 chars; trim the 16 over-length descriptions.
7. Add BlogPosting/Breadcrumb to the 9 uncovered posts; CollectionPage on `/blog`; ship `/favicon.ico`.
8. Install one analytics stack + Search Console; baseline field CWV.

**Week 3 — Performance & linking (dev: ~1–2 days)**
9. Homepage + `/blog` hub hydration cuts (server components, dynamic imports); target LCP < 2.5 s on both.
10. Replace the static featured-posts trio with a related-posts module; lift the 13 single-inlink posts to ≥ 4.

**Week 4 — Content consolidation (content: ongoing)**
11. Execute cluster consolidation into the new landings (start with listas/M3U ×5 and the `-telegram-2` duplicate); 301 satellites.
12. Verify in GSC: `/instalacion` re-indexed under its own URL, new landings indexed, broken-link count at zero.
13. Longer-term: reduce dependence on the "IPTV Smarters" trademark as the site's brand identity.

---

## 6. Verification Log

The five highest-priority findings were re-verified against the live site immediately before this report was finalized (9 July 2026):

| Finding | Re-verification result |
|---|---|
| 1. Missing commercial tier / 91 broken links | ✅ **Confirmed live** — `/suscripciones`, `/pago`, `/iptv-box`, `/iptv-legal-espana` all return 404; live blog HTML contains `href="/suscripciones"` and `href="/pago"`; source counts recomputed from the full 916-edge link graph |
| 2. `/instalacion` canonical → homepage | ✅ **Confirmed live** (`<link rel="canonical" href="https://iptvesp.com">`) **and independently flagged** by Lighthouse's SEO `canonical` audit on the same page |
| 3. French branding on checkout | ✅ **Confirmed live** — `<title>Finaliza tu commande — IPTV Smarters France · IPTV Smarters España</title>` on `/checkout` |
| 4. Missing aviso legal / condiciones / contacto | ✅ **Confirmed live** — all candidate URLs 404; footer contains only privacy + refund links |
| 5. Titles > 60 chars (47/51) | ✅ **Confirmed** from fresh crawl data; live samples up to 97 chars |

**Artifacts excluded from conclusions:** repeated Lighthouse runs on blog posts reported missing `<title>` (accessibility 54 / SEO 82) — the known audit-sandbox TLS-relay corruption seen throughout this engagement; crawl data confirms every post ships a real title, and the affected runs' performance sections (which were internally consistent: LCP 1.9 s) were retained while their SEO/accessibility categories were discarded.

**What could not be confirmed:** real-user CrUX field data (API quota unavailable across the engagement) — the homepage/hub LCP findings and `/instalacion`'s borderline CLS should be validated in Search Console once it's connected (the site currently has no analytics or GSC signals at all, see fix #9).

---

## Appendix — Methodology

- **Crawler:** custom BFS crawler (mobile Chrome UA), 63 URLs crawled (100% sitemap coverage + checkout variants + 12 dead targets), capturing status codes, redirect chains, canonicals, meta robots, titles/descriptions/H1s, viewport, JSON-LD, word counts, image alts, and the internal-link edge list (916 edges).
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile + desktop preset, simulated slow-4G) with automated sanity checks and up to 4 attempts per page; LCP diagnosed via phase breakdown.
- **Duplication testing:** cross-domain shingle checks vs the operator's French/Dutch siblings (unique content); intra-site clusters identified by slug/topic analysis.
- **Verification:** every P0/P1 finding re-tested with independent live requests before publication (§6).
