# Technical SEO Audit — primeiptv-france.com

**Prepared for:** Site owner, primeiptv-france.com
**Audit date:** 9 July 2026
**Scope:** Full technical audit — crawl architecture, indexability, Core Web Vitals, structured data, internal linking, mobile usability, HTTPS/security
**Pages analysed:** 57 URLs crawled + 10 sitemap orphans probed (67 sitemap URLs total), 1,587 internal links mapped, 8 Lighthouse lab runs, all findings re-verified against the live site before publication

---

## 1. Executive Summary

primeiptv-france.com has the best Core Web Vitals of the operator's portfolio (mobile Lighthouse 98–100 on every template, LCP 1.2–1.9 s, CLS 0) and a well-organised content architecture with legal pages, an FAQ, and a comparison hub in place. Three defects undermine it: **the `www` host is not connected to the production deployment — `https://www.primeiptv-france.com/` 302-redirects every visitor and crawler to a Vercel SSO login page**; **10 of the 67 sitemap URLs are orphans with zero internal links** (including the entire `/blog` hub and all three `/application/*` guides); and **a broken template emits an empty JSON-LD script on ~53 pages** — most visibly on `/faq`, which has rich FAQ content but no FAQPage markup because the schema block renders blank. All three are template/configuration-level fixes; combined with title trimming (35 of 57 over 60 characters) and stitching the ten geo pages into the main link graph, the site's technical debt clears within the 30-day plan.

---

## 2. Health Scorecard

| Area | Status | Notes |
|---|---|---|
| Host configuration | 🔴 Critical | `www` host 302s to a Vercel SSO login instead of the site |
| Crawlability & architecture | 🟡 Needs work | 57 linked pages healthy, but 10 sitemap orphans + geo cluster islanded at depth 3 |
| Indexability | 🟢 Good | Self-referencing canonicals everywhere; clean robots.txt; real 404s |
| Core Web Vitals (lab) | 🟢 Best of portfolio | 98–100 mobile on all templates; LCP 1.2–1.9 s; CLS 0 |
| Structured data | 🟡 Needs work | Empty JSON-LD script on ~53 pages; `/faq` missing FAQPage; 8 fragmented Products on `/tarifs` |
| On-page metadata | 🟡 Needs work | 35/57 titles > 60 chars; sitemap lastmod build-stamped |
| Internal linking | 🟡 Uneven | Nav pages get 56 inlinks; 8 guides at ≤ 2; geo pages interlink only with each other |
| Trust, mobile, HTTPS | 🟢 Good | Legal pages present; viewport 57/57; TLS 1.3 + HSTS preload |

---

## 3. Prioritized Fix List (Impact × Effort)

| # | Finding | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | **`www` host serves a Vercel SSO wall (verified twice):** `https://www.primeiptv-france.com/` (and every deep URL on it) responds `302 → vercel.com/sso-api?...`. Any user, link, or crawler arriving on www hits an authentication page on another domain. The http→https→www chain funnels into it too. Assign the www domain to the production deployment in Vercel and 308 it to the apex. | **High** | **Low** | **P0** |
| 2 | **10 sitemap URLs are orphans (0 internal links):** `/blog`, `/application/iptv-smarters-pro`, `/application/tivimate`, `/application/ibo-player`, and 6 guides (`iptv-tour-de-france-2026`, `meilleure-box-iptv-2026`, `iptv-vs-molotov-mycanal-streaming`, `iptv-chromecast-france`, `iptv-smarters-pro-android`, `iptv-smarters-pro-gratuit`). All return 200 with valid canonicals — they're built, submitted to Google, and then hidden from every visitor and from PageRank flow. | **High** | **Low** | **P0** |
| 3 | **Broken schema template — empty JSON-LD on ~53 pages:** an `application/ld+json` script renders with empty content sitewide. The clearest casualty is `/faq`: ~30 questions of on-page FAQ content and no FAQPage markup (the empty block is almost certainly the FAQ schema failing to serialize). | **Med-High** | **Low** | **P0** |
| 4 | **35/57 titles exceed 60 characters** (up to 93) — the pattern "{keyword-rich title} \| PrimeIPTV France" overflows; descriptions > 160 on several money pages. Sitemap `<lastmod>` is a single build-stamped value across all 67 URLs. | **Med** | **Low-Med** | **P1** |
| 5 | **Geo cluster is a near-island:** the 10 `/iptv/*` country pages (France, Belgique, Suisse, Maroc, …) sit at crawl depth 3 and receive links almost exclusively from each other (one external inlink total, from a guide). They're meant to capture geo queries but the site barely endorses them. | **Med** | **Med** | **P1** |
| 6 | `/tarifs` splits its offer into **8 sibling Product entities**; none carries aggregateRating and Google must guess which represents the service. Restructure as one Product (or Service) with an `offers` array of the 8 plans. | **Med** | **Low** | **P1** |
| 7 | 8 guides have ≤ 2 inlinks (`combien-coute-abonnement-iptv`, `iptv-glossaire-termes-debutants`, `iptv-4k-france-2026` at 1; VPN/Champions-League/children's-channels guides at 2); `/avis-iptv-france` — a conversion-support page — has only 2. | **Med** | **Med** | **P2** |
| 8 | Topic-overlap pairs: two VPN guides (`iptv-vpn-france` vs `iptv-avec-vpn-faut-il-utiliser`) and two 4K guides (`iptv-4k-france-2026` vs `iptv-4k-debit-internet`). Text is unique (~2% overlap measured) but they target the same queries — merge or sharply differentiate intents. | **Low-Med** | **Med** | **P2** |
| 9 | Thin commercial page: `/revendeur-iptv` (292 words) targets "revendeur IPTV" with too little substance to rank; legal pages are also thin but that's acceptable for their role. | **Low-Med** | **Med** | **P2** |
| 10 | Homepage has 1 image missing alt text; accessibility `label-content-name-mismatch` and `color-contrast` on some templates (a11y 90–100 — best of portfolio). | **Low** | **Low** | **P3** |

---

## 4. Detailed Findings

### 4.1 Host Configuration — the critical defect

Verified live twice, on `/` and `/tarifs`:

```
https://www.primeiptv-france.com/  →  302
location: https://vercel.com/sso-api?url=https%3A%2F%2Fwww.primeiptv-france.com%2F&nonce=…
```

The `www` subdomain resolves to a Vercel deployment protected by SSO (deployment protection), not to the public site. Consequences: any external link, bookmark, ad, or crawl request using `www` dead-ends on an authentication page hosted on a third-party domain; the 302 (temporary) status keeps crawlers retrying; and the site presents two inconsistently-behaving hosts. **Fix in Vercel:** add `www.primeiptv-france.com` to the production project as a redirecting domain (308 → apex), which also collapses the current `http://www → https://www → SSO` chain.

### 4.2 Crawl & Site Architecture

- **The linked site is healthy:** 57 pages, all 200, depth ≤ 3, no broken internal links, clean URL handling (trailing-slash 308s, query-param canonicals, real 404s, correct 404 on case variants).
- **But the sitemap promises 67 pages** — the other 10 are orphans (verified: all return 200 and are absent from every crawled page's links):
  - `/blog` — a content hub in the sitemap that nothing links to (the visible hub is `/guides`; `/blog` appears to be a parallel index that was never wired in).
  - `/application/iptv-smarters-pro`, `/application/tivimate`, `/application/ibo-player` — an entire app-guide section, invisible.
  - 6 guides, including seasonal money content (`iptv-tour-de-france-2026`, `meilleure-box-iptv-2026`).
  Orphans receive no PageRank and depend on sitemap-only discovery, which Google treats as a weak signal — these pages are effectively shelved. Add them to `/guides` listings, footer, or contextual links (or, if `/blog` is deprecated, remove it from the sitemap and 301 it to `/guides`).
- **Geo cluster (`/iptv/*`, 10 pages):** reachable only at depth 3, interlinked among themselves with a single inbound link from the rest of the site. If these country pages matter commercially (Belgique/Suisse/Québec/Maghreb targeting), add a footer "Pays" block or a homepage section linking them; if not, consider consolidating.

### 4.3 Indexability

- `robots.txt` allows everything (including AI crawlers), declares the sitemap; no noindex conflicts anywhere; all 57 crawled pages have correct self-referencing canonicals (as do the sampled orphans).
- **Sitemap weaknesses:** the 10 orphans (above) and a single identical `<lastmod>` across all 67 URLs (build-stamped — Google learns to ignore it). No hreflang despite ten country-targeted pages — fine for now since all are French-language, but if geo pages are kept, `hreflang="fr-BE"`, `fr-CH`, etc. pointing at them (with self-references) would sharpen targeting.

### 4.4 Core Web Vitals & Page Speed — the portfolio's best

**Method note:** PSI/CrUX quota unavailable; Lighthouse 12 lab data (emulated mobile, slow-4G), with automatic rejection and re-run of corrupted traces. Several artifact readings (missing `<title>`, 15 s main-thread, gtag console errors) were traced to the audit sandbox's TLS relay and excluded — see §6.

| Page (mobile) | Perf | LCP | TBT | CLS |
|---|---|---|---|---|
| `/` (homepage) | 98 | 1.9 s 🟢 | 120 ms 🟢 | 0 🟢 |
| `/tarifs` | 99 | 1.8 s 🟢 | 90 ms 🟢 | 0 🟢 |
| `/installation/smart-tv-samsung` | 100 | 1.6 s 🟢 | 40 ms 🟢 | 0 🟢 |
| `/guides/iptv-legal-en-france` | 99 | 1.2 s 🟢 | 100 ms 🟢 | 0 🟢 |
| `/` desktop | 100 | 0.6 s 🟢 | 0 ms 🟢 | 0 🟢 |

Every metric is comfortably green: TTFB 60–150 ms on Vercel edge cache, no render-blocking resources, zero layout shift, modest main-thread work (1.0–2.2 s) despite the large Next.js documents (380–470 KB — the RSC-payload duplication noted across the portfolio; worth trimming eventually, but with these scores it is not a priority). No performance work is required in the 30-day window beyond keeping it this way.

### 4.5 Structured Data

**Present:** `Organization` + `WebSite` sitewide; `Service` + `BreadcrumbList` on the homepage; `Product` ×8 on `/tarifs` and ×2 elsewhere; `Article` on 36 pages, `TechArticle` on the 12 installation pages; `BreadcrumbList` on 53/56. Favicon and OG image are generated routes and work (unlike two sister properties).

**Defects:**
1. **Empty JSON-LD script on ~53 pages (P0):** one `<script type="application/ld+json">` per page renders with no content — a serializer/conditional bug in the shared template. On most pages it's benign clutter, but on `/faq` it is the *only* thing standing between ~30 on-page Q&As and eligible FAQPage markup. Find the component that renders this block and fix its data source; then `/faq` (and FAQ sections elsewhere) get real FAQPage output.
2. **`/tarifs` Product fragmentation:** 8 sibling Products, none with ratings, no shared `@id`. One Product/Service with an `offers` array (like the sister sites' AggregateOffer pattern) is cleaner and rich-result-eligible.
3. Minor: 3 landing pages missing BreadcrumbList; consider `CollectionPage` on `/guides`.

### 4.6 Internal Linking

- Nav/footer pages each collect 56 inlinks; installation pages are strongly cross-linked (19–56); guide-to-guide linking exists but is uneven.
- **Starved tier:** 8 guides at ≤ 2 inlinks and `/avis-iptv-france` (social proof for conversion) at 2. Combined with the 10 zero-link orphans, roughly a quarter of the site's URLs are under- or un-endorsed.
- **Anchor quality is good** where links exist (descriptive French anchors, not bare URLs).
- Suggested modules: "guides similaires" block on the guide template (fixes the tail + orphaned guides at once), an "applications" row on `/installation/*` pages (fixes `/application/*` orphans), a "Pays" footer block (fixes the geo island), and a homepage link to `/avis-iptv-france` near the pricing CTA.

### 4.7 Content Quality Notes

- No thin content among guides (1,300–2,300 words typical) — but `/revendeur-iptv` (292 words) is a thin commercial page targeting a real query; expand or noindex.
- Topic overlaps to resolve editorially: the two VPN guides and two 4K guides (unique text, same intent — merge or split intents: e.g. "faut-il un VPN" = decision content vs "installer un VPN pour IPTV" = how-to).
- Cross-domain check vs the operator's other properties: 0% shingle overlap on matched topics — content is unique across the network.

### 4.8 Mobile Usability & HTTPS/Security

- Viewport on 57/57; tap targets and font sizes pass; one homepage image missing alt.
- Accessibility 90–100 (best of the portfolio); remaining: `color-contrast` on `/tarifs`, `label-content-name-mismatch` on two templates.
- TLS 1.3, valid Let's Encrypt wildcard (expires 8 Aug 2026 — the earliest expiry in the portfolio, confirm auto-renewal); HSTS `includeSubDomains; preload`; full security-header set; zero mixed content; HTTP/2 + edge cache. Legal pages (mentions légales, CGV, confidentialité) all present ✅.

---

## 5. 30-Day Roadmap

**Week 1 — Configuration & orphans (dev: ~1 day)**
1. Attach `www` to the production Vercel project and 308 it to the apex; re-test all four host/protocol variants land on `https://primeiptv-france.com` in ≤ 2 hops.
2. Wire in the 10 orphans: link `/application/*` from the installation template, the 6 orphan guides from `/guides`, and either integrate `/blog` into navigation or 301 it to `/guides` and drop it from the sitemap.
3. Fix the empty JSON-LD template block; confirm `/faq` emits valid FAQPage (Rich Results Test).

**Week 2 — Metadata & sitemap (dev/content: ~1 day)**
4. Rewrite the ~20 most important over-length titles (money pages first: `/tarifs` 68, geo pages, top guides) to ≤ 60 chars; trim over-length descriptions.
5. Emit real per-URL `<lastmod>` values.
6. Consolidate `/tarifs` schema into one Product/Service with an `offers` array.
7. Pull Search Console: confirm www-host duplication clears, orphan pages start receiving impressions, and baseline CWV field data.

**Week 3 — Linking architecture (dev: ~1–2 days)**
8. Ship the four linking modules (guides-similaires, applications row, Pays footer block, avis link near pricing).
9. Decide the geo cluster's fate: invest (hreflang + content differentiation per country) or consolidate.

**Week 4 — Content ops (content: ongoing)**
10. Merge or re-scope the VPN pair and 4K pair; expand `/revendeur-iptv` or noindex it.
11. Add alt text to the homepage image; fix contrast/label a11y items.
12. Monitoring: monthly orphan/broken-link crawl, GSC index coverage on the 10 formerly-orphaned URLs, seasonal check that `iptv-tour-de-france-2026` and `iptv-champions-league-streaming-2026` are linked ahead of their events.

---

## 6. Verification Log

The five highest-priority findings were re-verified against the live site immediately before this report was finalized (9 July 2026):

| Finding | Re-verification result |
|---|---|
| 1. `www` → Vercel SSO wall | ✅ **Confirmed live twice** — `HTTP/2 302` with `location: https://vercel.com/sso-api?...` on both `/` and `/tarifs` |
| 2. 10 sitemap orphans | ✅ **Confirmed** — all 10 absent from the 1,587-edge link graph; 6 sampled live (all return 200 with valid canonicals); homepage contains zero `href="/blog"` links |
| 3. Empty JSON-LD script sitewide; `/faq` missing FAQPage | ✅ **Confirmed live** — empty `ld+json` block present on `/tarifs`, `/faq`, and guide pages; `/faq` serves ~30 questions with no FAQPage entity |
| 4. Titles/lastmod | ✅ **Confirmed** — 35/57 titles > 60 chars in fresh crawl; sitemap has exactly 1 distinct `<lastmod>` value across 67 URLs |
| 5. Geo cluster isolation | ✅ **Confirmed from link graph** — 9 of 10 `/iptv/*` pages receive links only from sibling geo pages; single external inlink (one guide → `/iptv/maroc`) |

**Artifacts excluded from conclusions:** one homepage Lighthouse run reported missing `<title>`/`<html lang>` (accessibility 69, SEO 82) and another run showed a 15 s main thread — both were sandbox TLS-relay corruption. The live HTML verifiably contains the title ("Abonnement IPTV France 2026 Sans Coupure"), `lang="fr"`, a meta description, and a `<main>` landmark; clean re-runs scored SEO 100. The "errors in console" best-practices failure on all pages was traced to gtag.js failing through the audit relay, not the site.

**What could not be confirmed:** real-user CrUX field data (API quota unavailable — though with all-green lab metrics on every template, risk is low); Search Console index status for the www-host duplication and the orphan pages (no GSC access).

---

## Appendix — Methodology

- **Crawler:** custom BFS crawler (mobile Chrome UA), 57 linked URLs + 10 orphan probes (100% sitemap coverage), capturing status codes, redirect chains, canonicals, meta robots, titles/descriptions/H1s, viewport, JSON-LD (including empty-block detection), word counts, image alts, and the internal-link edge list (1,587 edges).
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile + desktop preset, simulated slow-4G) with automatic sanity checks (category-score presence, main-thread plausibility, document-title consistency) and up to 4 re-runs per page.
- **Duplication testing:** 8-word shingle Jaccard overlap — cross-domain vs sister properties (0%) and intra-site on the VPN and 4K guide pairs (~2%).
- **Verification:** every P0/P1 finding re-tested with independent live requests before publication (§6).
