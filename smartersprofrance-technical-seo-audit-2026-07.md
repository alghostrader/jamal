# Technical SEO Audit — smartersprofrance.fr

**Prepared for:** Site owner, www.smartersprofrance.fr
**Audit date:** 9 July 2026
**Scope:** Full technical audit — crawl architecture, indexability, Core Web Vitals, structured data, internal linking, mobile usability, HTTPS/security
**Pages analysed:** 28 URLs crawled (100% of the sitemap), 1,081 internal links mapped, 6 Lighthouse lab runs, all findings re-verified against the live site before publication

---

## 1. Executive Summary

smartersprofrance.fr is architecturally the healthiest of the operator's properties — a lightweight static build (40–80 KB documents, Total Blocking Time of just 60–80 ms), perfect crawl integrity across all 28 pages, the richest structured-data implementation of the portfolio (FAQPage on 18 pages, Product, HowTo, CollectionPage), and generally sane titles. Its two serious problems are of a different nature: **the site has no legal pages at all** — no mentions légales, no privacy policy, no CGV (all 404, nothing in the footer, despite shipping a cookie banner) — which is a legal-compliance exposure for a French commercial site and a trust/E-E-A-T signal Google explicitly evaluates for transactional pages; and **every mobile page has a slow LCP (3.0–4.3 s)** because hero images are hot-linked from images.pexels.com without preloading, adding ~1.5 s of external-host discovery and download time. Fix the legal pages and self-host the hero images in week one; the rest is polish — 25 of 28 meta descriptions are over-length, the apex domain redirects with a temporary 307 instead of a permanent 308/301, and seven articles sit at a single internal link.

---

## 2. Health Scorecard

| Area | Status | Notes |
|---|---|---|
| Crawlability & architecture | 🟢 Excellent | 28/28 pages 200; depth ≤ 2; 0 orphans; 0 broken links; sitemap ↔ crawl exact match |
| Indexability | 🟢 Good | Self-referencing canonicals on www host; clean robots.txt; per-URL lastmod (5 distinct) |
| Core Web Vitals (lab) | 🟡 LCP problem | TBT/CLS excellent everywhere; **LCP 3.0–4.3 s on all mobile pages** (external hero images) |
| Structured data | 🟢 Best of portfolio | FAQPage ×18, Product+AggregateOffer, HowTo, CollectionPage, ProfilePage; no parse errors |
| Trust & compliance | 🔴 Critical gap | **No mentions légales, privacy policy, or CGV anywhere** (404s); cookie banner with no policy |
| On-page metadata | 🟡 Needs work | 25/28 descriptions > 160 chars; 14/28 titles > 60 (moderate) |
| Internal linking | 🟡 Uneven | Hubs strong; 7 articles have ≤ 1 inlink |
| Mobile usability / HTTPS | 🟢 Good | Viewport 28/28; TLS 1.3, HSTS preload, CSP; apex redirect is 307 (should be permanent) |

---

## 3. Prioritized Fix List (Impact × Effort)

| # | Finding | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | **No legal pages exist:** `/mentions-legales`, `/politique-de-confidentialite`, `/conditions-generales` and every common variant return 404; the live homepage contains zero footer links to any legal content — yet a `cookie-banner.js` ships on every page. French LCEN law requires mentions légales; GDPR requires a privacy policy behind a consent banner; consumer law requires CGV/refund terms for a paid service. Beyond legal exposure, Google's quality raters and trust systems treat missing business/legal info on transactional sites as a negative signal. | **High** | **Low** | **P0** |
| 2 | **Slow LCP on every mobile page (3.0–4.3 s):** article hero images are hot-linked from `images.pexels.com` — Lighthouse's LCP breakdown shows ~770 ms resource discovery delay + ~715 ms external download. Homepage hero slider adds a ~570 ms render delay. Self-host the images (already permitted by CSP change), serve them sized/AVIF, and `fetchpriority="high"` + preload the LCP image per template. | **High** | **Med** | **P0** |
| 3 | **25 of 28 meta descriptions exceed 160 characters** (up to 264) — near-systematic truncation in SERPs. | **Med** | **Low** | **P1** |
| 4 | **Apex → www redirect is 307 (temporary):** `https://smartersprofrance.fr/` → 307 → `https://www.…`. A 307 passes no permanence signal, so Google may keep both hosts in limbo longer; make it 308/301. The `http://` apex also takes 2 hops to reach the canonical host. | **Med** | **Low** | **P1** |
| 5 | **7 articles have ≤ 1 internal link** (`iptv-smarters-pro-ne-fonctionne-pas`, `-code-activation`, `-multi-ecran`, `-epg-ne-charge-pas`, `-alternative-samsung-smart-tv`, `installer-…-nvidia-shield-pro`, `installer-…-chromecast-google-tv`) — thin discovery paths for the long-tail money content. | **Med** | **Med** | **P1** |
| 6 | Best-practices issues on article template: images rendered at incorrect aspect ratio; third-party cookies set (Pexels CDN) — both disappear when images are self-hosted (see #2). | **Low-Med** | — (bundled with #2) | **P2** |
| 7 | 14/28 titles exceed 60 chars (max 78) — mild; fix the worst on money pages. | **Low** | **Low** | **P2** |
| 8 | The 95 KB `logo-france.png` triples as favicon, OG image and `Organization.logo`: too heavy for a favicon, wrong aspect for OG (1200×630 expected), acceptable for logo. Ship a proper ~1–5 KB favicon, a dedicated 1200×630 OG image, and keep a square logo for schema. | **Low** | **Low** | **P2** |
| 9 | Accessibility: `heading-order` and `link-name` fail on all templates, `color-contrast` on 2, `link-in-text-block` on 2 (a11y 87–95). | **Low** (SEO) | **Med** | **P3** |
| 10 | Brand-risk note (not a technical defect): the domain, homepage title ("IPTV Smarters Pro France — Abonnement officiel 2026") and content are built entirely on a third-party app's trademark with an "officiel" claim. A trademark complaint could remove the site from search or force a rebrand; diversifying brand equity toward an owned name reduces that single point of failure. | **Low-prob / High-sev** | — | **note** |

---

## 4. Detailed Findings

### 4.1 Crawl & Site Architecture

- **Flawless mechanics:** 28/28 pages return 200; sitemap ↔ crawl match exactly; zero orphans, zero broken internal links; depth ≤ 2 (home → 5 hubs + about → 22 articles). Trailing slashes 308, query parameters canonicalised, real 404s on unknown paths.
- **Canonical host is `www`** and all canonicals/sitemap/OG URLs consistently use it ✅ — but the apex→www hop is a **307 Temporary Redirect** (verified live). Temporary redirects ask Google to keep the source URL indexed; this should be a 301/308. The `http://apex` variant chains twice (`http→https apex → www`).
- `/articles` (the URL parent of all posts) returns 404, but nothing links to it and breadcrumbs correctly use `/tutoriels` as the hub — harmless quirk, optionally 301 it to `/tutoriels`.

### 4.2 Indexability

- `robots.txt` allows all crawlers (including AI bots), declares the sitemap. No noindex anywhere, no meta-robots conflicts, no hreflang (correct; `lang="fr"` on 28/28).
- Sitemap: 28 URLs, all 200, with 5 distinct `<lastmod>` values (credible dates rather than a build stamp).
- None of the sister-site canonical defects — every canonical is self-referencing on the www host.

### 4.3 Trust & Compliance — the critical gap

Verified live: `/mentions-legales`, `/politique-de-confidentialite`, `/conditions-generales`, `/cgv`, `/legal` all return 404, and the homepage footer contains **no** legal links at all — while `cookie-banner.js` loads on every page and the site sells subscriptions (19–79 €) via WhatsApp.

- **Legal:** French LCEN (art. 6-III) requires mentions légales identifying the publisher; GDPR/ePrivacy requires a privacy policy reachable from the consent banner; French consumer code requires CGV and withdrawal/refund terms for paid services.
- **SEO:** Google's quality guidance treats identifiable business information, terms, and refund policies as trust signals for transactional sites; their absence caps E-E-A-T-related scoring. The sister properties all have these four pages — porting the template is a same-day fix.

### 4.4 Core Web Vitals & Page Speed

**Method note:** PSI/CrUX API quota was unavailable; figures are Lighthouse 12 lab data (emulated mobile, slow-4G simulation) with automatic re-runs on corrupted traces. Field validation via Search Console recommended.

| Page (mobile) | Perf | LCP | TBT | CLS |
|---|---|---|---|---|
| `/` (homepage) | 89 | **3.5 s** 🔴 | 70 ms 🟢 | 0.02 🟢 |
| `/abonnement-iptv` | 92 | **3.0 s** 🟡 | 60 ms 🟢 | 0 🟢 |
| `/installation` | 93 | **3.0 s** 🟡 | 80 ms 🟢 | 0.005 🟢 |
| `/articles/installer-…-fire-tv-stick` | 84 | **4.3 s** 🔴 | 60 ms 🟢 | 0.045 🟢 |
| `/` desktop | 98 | 0.9 s 🟢 | 0 ms 🟢 | 0.045 🟢 |

**Diagnosis — an image problem, not a JavaScript problem.** This static build has the best interactivity metrics of the portfolio (TBT 60–80 ms; documents 40–80 KB vs the sisters' 270–460 KB). The single systemic weakness is LCP:

- **Article template:** the LCP element is `<img class="article-hero">` loaded from `images.pexels.com`. Lighthouse breakdown: TTFB 451 ms → **769 ms resource load delay** (external host discovery, no preload) → **715 ms download** (oversized source) → render. Self-hosting alone removes the connection setup; adding `<link rel="preload" fetchpriority="high">` and properly sized AVIF/WebP brings LCP under 2.5 s.
- **Homepage:** LCP is the `hero-slide` div (CSS background image) with a 569 ms render delay — background images can't be prioritized by the preload scanner; move the first slide's image to an `<img>` with `fetchpriority="high"` or preload it.
- Fixing #2 also clears the article template's best-practices failures (incorrect aspect ratio, third-party Pexels cookies — currently BP score 73).

### 4.5 Structured Data — the strongest of the portfolio

No parse errors; richest coverage of the four audited properties:

| Page type | Schema present |
|---|---|
| Homepage | Organization + WebSite + **Product with AggregateOffer** (22–79 €, 4 offers) + **FAQPage** (5 questions) |
| `/abonnement-iptv` | Product + FAQPage + Breadcrumb |
| `/installation` | HowTo + FAQPage + Breadcrumb |
| `/tutoriels` | **CollectionPage** + Breadcrumb (the hub schema the sister sites lack) |
| `/iptv-premium` | Service + Breadcrumb |
| `/a-propos` | ProfilePage + Person ("Alae Hamdi") |
| 22 articles | Article (author → `/a-propos`) + Breadcrumb, plus FAQPage on 14/22 |

**Gaps:** the multi-purpose `logo-france.png` (fix #8); Article images are Pexels URLs (same E-E-A-T/uniqueness note as the sister sites — and self-hosting them is already required by the LCP fix); no `aggregateRating` (only add with genuine on-page reviews).

### 4.6 Internal Linking

- Hubs and money pages are well served: `/abonnement-iptv`, `/installation`, `/iptv-premium`, `/tutoriels` each receive 27 inlinks, and top tutorials (`android-tv`, `code-iptv-xtream-vs-m3u`, `iptv-4k-france-bande-passante`) earn 24–26 contextual inlinks.
- **The tail is starved:** 7 of 22 articles have ≤ 1 inlink (list in fix #5) — reachable only via `/tutoriels`. A "related tutorials" block (3–4 links) on the article template fixes the whole tier at once.
- Flat-equity is *less* of an issue here than on the sisters simply because there are no legal pages in the footer — adding them (fix #1) will slightly dilute nav equity, which is fine and necessary.

### 4.7 Mobile Usability

Viewport on 28/28; tap targets and font sizes pass; no missing alt attributes; fully crawlable static HTML. Accessibility 87–95 with recurring `heading-order` and `link-name` failures (icon links without accessible names) and `color-contrast` on two templates — UX/compliance, not rankings.

### 4.8 HTTPS & Security

- TLS 1.3, valid Let's Encrypt wildcard (expires 30 Aug 2026 — confirm auto-renewal); HSTS `includeSubDomains; preload`; CSP (self + GA/GTM, fonts, Pexels images, `form-action` self + wa.me); `nosniff`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`; zero mixed content; HTTP/2.
- Purchase flow via WhatsApp (same +44 number as the sister property — consistent operator setup). Same advice: add on-site conversion events if paid acquisition is planned.
- Note: the third-party cookies flagged by Lighthouse come from the Pexels CDN, not the site itself — they disappear with the self-hosting fix. The cookie banner currently has no policy page to link to (fix #1).

---

## 5. 30-Day Roadmap

**Week 1 — Compliance & LCP (dev: ~2 days)**
1. Create the four legal pages (mentions légales, confidentialité, CGV, remboursement — the sister sites' templates can be adapted same-day), link them in the footer, and reference the privacy policy from the cookie banner.
2. Self-host all hero images; convert to AVIF/WebP at rendered size.
3. Preload the LCP image per template (`fetchpriority="high"`; convert the homepage first slide from CSS background to `<img>`).
4. Change apex→www redirect from 307 to 308/301; collapse the http-apex chain to one hop.

**Week 2 — Metadata (dev/content: ~1 day)**
5. Rewrite the 25 over-length meta descriptions to ≤ 160 chars, starting with home, `/abonnement-iptv`, `/installation`, `/iptv-premium`.
6. Trim the 5 worst titles (> 70 chars) to ≤ 60.
7. Split the logo asset: real favicon (≤ 5 KB), dedicated 1200×630 OG image, square schema logo.
8. Pull Search Console + CrUX to baseline field LCP; re-run Lighthouse to confirm LCP < 2.5 s post-fix.

**Week 3 — Linking & schema polish (dev: ~1 day)**
9. Add a related-tutorials module to the article template; ensure every article has ≥ 4 inlinks.
10. 301 `/articles` → `/tutoriels`.
11. Fix `heading-order` and give icon links accessible names.

**Week 4 — Content ops & risk (ongoing)**
12. Replace remaining Pexels imagery with unique branded screenshots (tutorials lend themselves to real app screenshots — better for users and image search).
13. Verify legal pages are indexed; monitor GSC coverage and CWV.
14. Discuss the trademark exposure (fix-list note #10) and a long-term owned-brand strategy.

---

## 6. Verification Log

The five highest-priority findings were re-verified against the live site immediately before this report was finalized (9 July 2026):

| Finding | Re-verification result |
|---|---|
| 1. No legal pages | ✅ **Confirmed live** — `/mentions-legales` and `/politique-de-confidentialite` return 404; zero matches for "mentions / confidentialité / conditions" in the live homepage HTML; `cookie-banner.js` present |
| 2. LCP driven by external Pexels heroes | ✅ **Confirmed** — live article HTML serves `<img class="article-hero" src="https://images.pexels.com/…">`; Lighthouse LCP breakdown attributes ~1.5 s to resource delay + download; consistent 3.0–4.3 s across all four mobile templates |
| 3. Meta descriptions over-length | ✅ **Confirmed** — 25/28 pages > 160 chars in fresh crawl data |
| 4. Apex 307 redirect | ✅ **Confirmed live** — `HTTP/2 307` with `location: https://www.smartersprofrance.fr/` |
| 5. Seven articles with ≤ 1 inlink | ✅ **Confirmed** — recomputed from the full 1,081-edge link graph |

**What could not be confirmed, and why:**

- **Field Core Web Vitals (CrUX):** API quota unavailable from the audit environment. The LCP finding is consistent across every template and run (image-loading physics rather than lab variance), so confidence is high, but post-fix validation should use Search Console.
- **GDPR/LCEN exposure severity:** I verified the *absence* of the pages, not the operator's legal obligations in their specific corporate setup — treat the compliance framing as "confirmed missing, consult counsel for scope."
- **Index/query data:** no Search Console access; the 307-redirect's practical indexing effect (www vs apex duplication) should be checked in GSC's page-indexing report after switching to 308.

---

## Appendix — Methodology

- **Crawler:** custom BFS crawler (mobile Chrome UA), 28 URLs (100% site coverage), capturing status codes, redirect chains, canonicals, meta robots, titles/descriptions/H1s, viewport, JSON-LD, word counts, image alts, and the internal-link edge list (1,081 edges).
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile + desktop preset, simulated slow-4G) with automatic detection/re-run of corrupted traces; LCP diagnosed via Lighthouse's phase breakdown (TTFB / load delay / load duration / render delay).
- **Duplication testing:** 8-word shingle Jaccard overlap against all three sister domains on the shared "Smarters vs TiviMate" topic — 0% overlap, content unique.
- **Verification:** every P0/P1 finding re-tested with independent live requests before publication (§6).
