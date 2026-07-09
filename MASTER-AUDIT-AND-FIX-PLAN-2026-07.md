# Master Technical Audit & Fix Plan — IPTV Portfolio

**Prepared for:** Site owner — 8 properties
**Date:** 9 July 2026
**Basis:** 7 full technical audits (390+ pages crawled, 40+ Lighthouse runs, every P0/P1 finding re-verified live) + 90 days of Search Console data pulled via API + Google URL Inspection verification of 24 problem URLs.
**Properties:** iptvpix.com · abonnementiptvofficiel.com · iptvfranceofficiel.fr · smartersprofrance.fr · primeiptv-france.com · iptvned.com · iptvesp.com · (smarters-live.com, discovered in GSC)

This document is the one to work from. It consolidates everything into: the state of the portfolio (§1), the 10 systemic problems and **exactly how to fix each one** (§2), per-site punch lists (§3), the content consolidation maps (§4), a sequenced 90-day program (§5), and the measurement plan (§6). Individual per-site reports with full detail are in the same repository.

---

## 1. State of the Portfolio — the honest picture

**Traffic reality (Search Console, 90 days):** 320 clicks total across all properties.

| Site | Clicks (90d) | Trend | Status |
|---|---|---|---|
| iptvesp.com | 191 | 43 → 148 📈 | Growing fast; 84% from one post; pricing page 404s |
| primeiptv-france.com | 37 | 16 → 21 📈 | Healthiest spread; www host serves a login wall; 10 orphans |
| iptvned.com | 35 | 23 → 12 📉 | One news post fading; sitewide nav 404; 2 pages de-indexed |
| iptvpix.com | 25 | 25 → **0** 🔴 | **Collapsed.** 3 pages unknown to Google; 66 broken links |
| iptvfranceofficiel.fr | 17 | 11 → 6 📉 | CTA funnel points at a URL Google has never seen |
| abonnementiptvofficiel.com | 14 | 7 → 7 ➡️ | Flat at page-5 rankings; favicon 404 |
| smarters-live.com | 1 | — | No presence; strategic decision needed |
| smartersprofrance.fr | *unknown* | — | **Not verified in Search Console** |

**The three layers of the problem:**

1. **Technical defects are actively deleting pages from Google.** URL Inspection confirmed: five hub/landing pages across three sites are *"unknown to Google"* because of a canonical bug; two www hosts are indexed with `vercel.com/login` as their canonical; orphan pages were crawled and discarded exactly as predicted. These are hours-of-work fixes with outsized returns.
2. **The content strategy manufactures internal competition.** ~120 of the portfolio's ~390 pages sit in keyword-cannibalization clusters (up to 13 URLs targeting one query). GSC shows the result live: e.g. "iptv abonnement nederland legaal" splits across three iptvned pages at positions 72–85 — none can rank.
3. **Authority is the ceiling.** Money terms sit at positions 60–90 everywhere. Each site's actual traffic comes from one specific low-competition topic it happens to own (Telegram lists, a police-raid news query, MAG-box setup, Canal+ sport). After the fixes below, the binding constraint becomes links and brand, not code.

---

## 2. The 10 Systemic Problems — and exactly how to fix them

These recur across sites because the sites share codebases (two Next.js template families + one static build). **Fix once in the shared template, deploy everywhere.** Ordered by impact.

### FIX 1 — Canonical + hreflang pointing at the homepage (de-indexes pages)

**Where:** iptvpix.com (`/blog`, `/iptv-acheter`, `/box-iptv`, `/pandora-iptv`) · iptvned.com (`/blog`, `/iptv-kopen`) · iptvesp.com (`/instalacion`).
**Proof of damage:** iptvpix's three pages and iptvned's `/iptv-kopen` are **"unknown to Google"** (URL Inspection, 9 July). Google rescued the other two by overriding the canonical — a coin flip you lost 4 times out of 6.

**How to fix (Next.js App Router):** in each affected route's `layout.tsx`/`page.tsx` metadata, the canonical is hardcoded to the site root. Make it self-referencing and delete the hreflang block (single-locale sites don't need hreflang; `<html lang>` is enough):

```ts
// app/blog/page.tsx (and each affected route)
export const metadata: Metadata = {
  alternates: {
    canonical: "https://iptvpix.com/blog",   // ← was "https://iptvpix.com"
    // languages: {...}  ← DELETE this block entirely
  },
};
```
If the canonical is computed in a shared helper, the bug is one place: look for where `alternates.canonical` falls back to `siteUrl` instead of `siteUrl + pathname`. Fix the helper:
```ts
canonical: `${SITE_URL}${pathname === "/" ? "" : pathname}`,
```
**Verify:** `curl -s https://iptvpix.com/blog | grep canonical` shows the page's own URL → then GSC → URL Inspection → "Request indexing" for all 7 affected URLs.

### FIX 2 — www hosts locked behind Vercel SSO (login wall for users and Google)

**Where:** primeiptv-france.com, iptvned.com. Google's chosen canonical for these www homepages is literally `https://vercel.com/login`.

**How to fix (Vercel dashboard, ~2 minutes per site):**
1. Project → **Settings → Domains** → check that `www.primeiptv-france.com` is listed. If it's attached to a *different* (preview/protected) project, remove it there first.
2. Add `www.primeiptv-france.com` to the **production** project and select **"Redirect to primeiptv-france.com"** with a **308** permanent redirect.
3. If the project has **Deployment Protection** (Settings → Deployment Protection), ensure it applies only to preview deployments, not production aliases.

**Verify:** `curl -sI https://www.primeiptv-france.com/` returns `308` with `location: https://primeiptv-france.com/` (no `vercel.com/sso-api`). Repeat for iptvned. Also fix the same setting on smartersprofrance.fr, whose apex→www is a **307** — change to 308 (in that site's static-host config, redirect status is set where the domain redirect is defined).

### FIX 3 — Broken internal links at scale (≈260 dead links portfolio-wide)

**Where / what:**
- **iptvned.com:** `/pandora-iptv` in the sitewide nav — **68 pages** link to a 404. `/contact` ×27.
- **iptvesp.com:** 91 links → 12 dead URLs, incl. pricing `/suscripciones` ×15 and payment `/pago` ×14 (245 impressions served on the 404 — demand proven), plus French leftovers `/offres`, `/villes/paris`, `/contact`.
- **iptvpix.com:** 66 links → `/contact` ×24, `/villes/paris` ×22, `/offres` ×16, 2 moved guides.
- **iptvfranceofficiel.fr:** 11 commercial CTAs → `/abonnement-iptv` (unknown to Google).

**How to fix — two halves, do both:**

*(a) Redirects for URLs that have/had equity* — in `next.config.js` (or `vercel.json`) of each site:
```js
async redirects() {
  return [
    // iptvfranceofficiel.fr
    { source: "/abonnement-iptv", destination: "/iptv-france", permanent: true },
    // iptvpix.com
    { source: "/iptv-firestick-france", destination: "/blog/iptv-firestick-france", permanent: true },
    { source: "/iptv-legal-france-gratuit", destination: "/blog/iptv-legal-france-gratuit", permanent: true },
    // iptvesp.com (until real pages ship — see (b))
    { source: "/suscripciones", destination: "/checkout", permanent: false },
    { source: "/pago", destination: "/checkout", permanent: false },
  ];
}
```
*(b) Fix the link sources in the templates* — these links live in 2–3 shared components, not 90 places: the nav/footer component (iptvned's `/pandora-iptv`), the blog-post CTA fragment (`/contact`, `/offres`, `/villes/*` on iptvpix + iptvesp), and the in-article link helper (iptvfranceofficiel's "abonnement IPTV" anchor). Grep the codebase for the dead hrefs, fix each component once.
*(c) Build what should exist:* iptvesp needs a real `/suscripciones` (Spain's demand is proven — copy `/abonnements` from the French sibling, translate properly, Product+AggregateOffer schema from day one, then change the redirect in (a) to the real page). iptvned needs `/pandora-iptv` built or the nav item removed. A `/contact` page on every site (see FIX 7).

**Verify:** re-crawl each site (any crawler / Screaming Frog) → 0 internal 404s.

### FIX 4 — Broken structured-data assets & blocks

**Where / what:**
- `Organization.logo` → `https://…/icon.svg` **404** on iptvpix (~72 pages) and iptvned (~68 pages). iptvesp already has the file — proof the fix is just shipping the asset.
- abonnementiptvofficiel.com: declared `<link rel="icon" href="/favicon.ico">` → **404** on all 36 pages (costs SERP favicon display).
- primeiptv-france.com: an **empty** `<script type="application/ld+json">` on ~53 pages; `/faq` has ~30 Q&As and no FAQPage because that block fails to serialize.
- `/abonnements` (iptvpix) & `/tarifs` (primeiptv): Product schema split/fragmented (offers separated from ratings; 8 sibling Products).

**How to fix:**
1. Drop the actual files into `public/` (`icon.svg` 512×512, `favicon.ico`, `apple-icon.png`) on iptvpix + iptvned; on abonnementiptvofficiel add `favicon.ico`. In Next.js App Router you can instead place `app/icon.svg` and reference the generated URL in the JSON-LD — but the simplest durable fix is a real static file matching the URL the JSON-LD already emits.
2. primeiptv: find the schema component that renders conditionally (almost certainly `faqSchema && <script …>` where `faqSchema` is undefined serialized to empty). Fix the data source; guard with `if (!data) return null` so empty blocks never render.
3. Merge Product entities — one `Product` node containing `offers` (AggregateOffer or array) **and** `aggregateRating` **and** `review`, sharing one `@id`:
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://iptvpix.com/abonnements#product",
  "name": "Abonnement IPTV IPTVPIX",
  "image": "https://iptvpix.com/icon.svg",
  "brand": {"@type": "Brand", "name": "IPTVPIX"},
  "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
             "lowPrice": "19.00", "highPrice": "89.00", "offerCount": 4},
  "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.7",
                      "reviewCount": "6"},
  "review": [ /* existing reviews */ ]
}
```
**Verify:** Rich Results Test on `/abonnements`, `/tarifs`, `/faq`; `curl -sI` each icon URL → 200.

### FIX 5 — Title-template bugs (every site)

**Where / what:**
- **Doubled brand:** iptvned — "… — IPTVNED · IPTVNED" on **56/68 pages**; abonnementiptvofficiel — brand twice on 5 pages.
- **Wrong-market brand:** iptvesp checkout — "Finaliza tu **commande** — IPTV Smarters **France** · IPTV Smarters España".
- **Over-length:** 60–100% of titles exceed 60 chars on every site (suffixes of 15–26 chars are the root cause).

**How to fix:** in each site's root layout, titles use Next's template: `title: { template: "%s · IPTVNED", default: … }`. The doubling happens because page components *also* append the brand to their own title strings. Rule: **brand lives only in the template**; page titles are raw. Grep for the brand string in page-level metadata and strip it. For iptvesp's checkout, the page metadata was copy-pasted from the French repo — retranslate that one string. Then shorten suffixes (`· IPTVNED` is fine; `· Abonnement IPTV Officiel` at 26 chars is not — use `· IPTV Officiel`), and rewrite the top-20 money/hub titles per site to ≤ 60 chars, front-loading the keyword.

**Verify:** crawl → `SELECT title WHERE length > 60 OR title LIKE '%brand%brand%'` → zero rows.

### FIX 6 — Orphans and half-wired sections

**Where / what (URL Inspection proved sitemap-only pages don't get indexed):**
- primeiptv: **10 orphans** — `/blog` (crawled–not-indexed), 3 × `/application/*` (unknown to Google), 6 guides.
- iptvned: `/iptv-merken` orphan; 4 × `/steden/*` live but missing from sitemap, 1–2 inlinks.
- iptvpix: `/a-propos` orphan — also the author-entity URL of every BlogPosting.
- primeiptv geo cluster: 10 `/iptv/*` country pages linked only to each other at depth 3.

**How to fix:** links, not sitemaps, are what Google acts on:
1. Add an "Applications" row to primeiptv's installation template (3 links), the 6 orphan guides to the `/guides` listing page, and either put `/blog` in the nav or 301 it to `/guides` + drop from sitemap.
2. iptvned: footer link to `/iptv-merken`; add `/steden/*` to sitemap + a "Steden" footer block (or delete the section).
3. iptvpix: footer + author-byline link to `/a-propos` on every post.
4. primeiptv geo pages: a "Pays" footer block, or consolidate — don't leave them islanded.

**Verify:** re-crawl → every sitemap URL has ≥ 3 inlinks. In 2–4 weeks, URL-inspect the former orphans → "Submitted and indexed".

### FIX 7 — Missing trust/legal pages

**Where:** smartersprofrance.fr — **none** (no mentions légales/privacy/CGV, despite a cookie banner; LCEN+GDPR exposure). iptvesp — no aviso legal, no condiciones, no contact (LSSI exposure). Most sites lack `/contact` even where templates link to it.

**How to fix:** the portfolio already contains complete legal templates (iptvpix, abonnementiptvofficiel have all four pages). Port them: mentions légales/aviso legal (operator identity), privacy policy (link it from the cookie banner), CGV/condiciones + refund terms, contact page (a form or the WhatsApp contact presented properly). Half a day per site including translation. This is simultaneously legal risk reduction and the trust signal Google weighs on transactional sites.

### FIX 8 — JavaScript weight on the Next.js family (TBT/LCP)

**Where:** homepage TBT/main-thread on iptvpix (~5 s main-thread), iptvned (710 ms TBT, 6.4 s), iptvesp home+blog hub (LCP 3.3–3.6 s, 1.25 s hydration render-delay), iptvfranceofficiel `/installatie`-equivalent. HTML documents 300–570 KB from RSC payload duplication; double analytics (gtag **and** Plausible) on iptvpix + iptvned.

**How to fix (one afternoon per template family):**
1. **One analytics stack.** Keep Plausible (2 KB) or GA4 — not both. If GA4 stays, load it after first interaction:
```js
const load = () => { /* inject gtag script */ };
["scroll","click","touchstart"].forEach(e =>
  addEventListener(e, load, { once: true, passive: true }));
```
2. **Server components for static sections.** The hero, pricing cards, FAQ and testimonial sections don't need hydration. Remove `"use client"` where there's no interactivity; wrap the few interactive widgets (carousel, accordion) in `next/dynamic(() => import(...), { ssr: true })` so their JS loads in a later chunk.
3. That alone typically cuts the 500 KB documents toward ~250 KB and moves text-LCP render delay under 500 ms.
4. smartersprofrance (static site) has the opposite problem — **image LCP**: self-host the Pexels heroes, serve AVIF/WebP at rendered size, `<img fetchpriority="high">` for the LCP image, convert the homepage hero from CSS background to `<img>`.
5. abonnementiptvofficiel + iptvfranceofficiel: font-swap CLS — add metric-compatible fallback:
```css
@font-face { font-family: "Brand-fallback"; src: local("Arial");
  size-adjust: 106%; ascent-override: 92%; descent-override: 24%; }
/* font-family: Brand, Brand-fallback, sans-serif */
```
**Verify:** Lighthouse mobile after deploy — targets: TBT < 200 ms, LCP < 2.5 s, CLS < 0.1 on home + 1 template per site. Then watch GSC → Experience → CWV as field data accumulates.

### FIX 9 — Sitemap lastmod stamped at build

**Where:** iptvpix, abonnementiptvofficiel, primeiptv (all URLs share one timestamp — Google learns to ignore it; the other sites already do this right).
**How to fix:** in `app/sitemap.ts`, emit the content's real `updatedAt` (frontmatter date / CMS field), not `new Date()`:
```ts
{ url: `${SITE}/blog/${post.slug}`, lastModified: post.updatedAt }
```

### FIX 10 — Measurement gaps

**Where:** smartersprofrance.fr not verified in Search Console at all; iptvesp has **zero** analytics installed; smarters-live.com unaudited/undecided.
**How to fix:**
1. Verify smartersprofrance.fr in GSC: Search Console → Add property → Domain → add the shown TXT record at the DNS host → Verify. Submit the sitemap.
2. Add Plausible (or GA4) to iptvesp — one script tag in the root layout; it currently measures nothing.
3. Decide smarters-live.com: fold its 2 pages into smartersprofrance.fr with 301s (recommended — three "Smarters" web presences split a thin brand), or invest separately.

---

## 3. Per-Site Punch Lists

Each list references the systemic fixes (F1–F10) plus site-specific items. Order = do top-down.

**iptvpix.com — recovery project (traffic 25 → 0)**
1. F1 canonicals (4 URLs) → request indexing on each. 2. F3 broken links (66). 3. F4 icon.svg + merged Product. 4. F6 `/a-propos`. 5. F8 analytics + hydration. 6. F9 lastmod. 7. Request re-indexing of `/france-iptv-m3u` (last crawl 18 May; it's the only page that ever earned clicks). 8. §4 consolidation (worst cluster: 13 × "IPTV légal France"). Watch GSC coverage weekly — if impressions don't begin recovering ~3–4 weeks after fixes, the problem escalates from technical to trust/authority and link acquisition becomes the lever.

**iptvesp.com — protect and extend the winner**
1. Build real `/suscripciones` (+ `/pago` → checkout) — F3c. Demand proven (245 imp on the 404). 2. F1 `/instalacion` canonical. 3. Fix checkout FR→ES strings (F5). 4. Legal pages (F7). 5. Analytics (F10). 6. Add internal links **from** `/blog/iptv-espana-telegram` (the site's only authority page, 161 clicks) to `/suscripciones` and the money cluster. 7. Build the 4 missing landings as cluster winners (§4). 8. Push `mejor-iptv-espana` (pos 34, 143 imp) to page 1 via consolidation + links.

**iptvned.com — fix the funnel while the news post still has juice**
1. F3 `/pandora-iptv` nav link (68 pages) + `/contact`. 2. F1 `/blog` + `/iptv-kopen`. 3. F4 icon.svg. 4. F5 doubled titles (56 pages). 5. F2-adjacent: www host = SSO wall → Vercel domains. 6. F6 steden/merken. 7. F8 one analytics stack + hydration. 8. §4: consolidate the legal cluster now — GSC shows "iptv abonnement nederland legaal" split across 3 pages at pos 72–85; add internal links from `/blog/iptv-opgerold-nederland` (its only ranking asset) to the consolidated page.

**primeiptv-france.com — wire it together**
1. F2 www SSO (Google canonical = vercel.com/login). 2. F6 all 10 orphans. 3. F4 empty JSON-LD block → unlock FAQPage on `/faq`. 4. F5/F9 titles + lastmod. 5. Merge `/tarifs` 8-Product fragmentation (F4.3). 6. Geo cluster: footer "Pays" block or consolidate. 7. Opportunity: `mag box` (pos 14, 43 imp) and the kids-channels guide (pos 9) are near page 1 — a few internal links + 2-3 external links each.

**iptvfranceofficiel.fr — un-break the CTA funnel**
1. F3 301 `/abonnement-iptv` → `/iptv-france` + update the 11 article links. 2. Differentiate home vs `/iptv-france` (H1s verified nearly identical): home = brand + "meilleur abonnement IPTV", `/iptv-france` = "pas cher" + price in H1. 3. F5 titles (31/36 long, kw doubled on home). 4. `/articles` hub JSON-LD (CollectionPage). 5. Font CLS (F8.5). 6. Opportunity: `/articles/iptv-smarters-pro` is at pos 14.6 with 180 imp — internal links from all Smarters-adjacent posts + a couple of external links to reach page 1.

**abonnementiptvofficiel.com — quick wins, then lean into sport**
1. F4 favicon.ico. 2. F5 doubled brand (5 pages) + shorten suffix sitewide (36/36 long). 3. `/blog` hub JSON-LD. 4. F8.5 font CLS; gtag defer. 5. F9 lastmod. 6. Editorial: the Canal+/sport angle is the only thing ranking (pos 5–16) — extend it (per-competition pages) and interlink to `/test-iptv` (its top clicked page, stuck at pos 47.9) and `/iptv-premium`.

**smartersprofrance.fr — compliance + images**
1. F7 legal pages (all four; link cookie banner → privacy). 2. F8.4 self-host + preload hero images (LCP 3.0–4.3 s everywhere). 3. F2 apex 307 → 308. 4. Descriptions (25/28 over-length). 5. F10 verify in GSC + submit sitemap. 6. Related-tutorials module for the 7 single-inlink articles. 7. Strategic: domain rides the "IPTV Smarters" trademark — plan brand diversification.

---

## 4. Content Consolidation Maps

Method for every cluster: pick the **winner** (usually the landing page, or the URL GSC shows with most impressions), merge any unique material from satellites into it, then **301 satellites → winner** (or `rel=canonical` if a page must stay visible). Update internal links to point at winners. Expected portfolio effect: ~390 URLs → ~300 stronger ones.

**iptvpix.com**
| Cluster (URLs) | Winner | 301 away |
|---|---|---|
| IPTV légal France (13) | `/iptv-legal-france` | all `/blog/iptv-legal-*`, `/blog/iptv-legalite-*`, `/blog/iptv-interdit-*`; keep `/amende-iptv-france` as distinct sub-topic, 301 `/blog/*amende*` into it |
| Generic "IPTV France" (10) | `/blog/iptv-france-2026-guide-complet` | `iptv-france`, `iptv-france-2`, `iptv-en-france`, `tv-iptv-france`, `premium-`, `france-iptv-pro`, avis/reddit/pas-cher variants |
| Meilleur IPTV (7) | `/meilleur-abonnement-iptv` | all `/blog/meilleur*` except app-comparison post |
| M3U (3) | `/france-iptv-m3u` (only page that earned clicks) | both blog M3U posts |
| Firestick (4) / Samsung (3) / Apps (5) | keep 1 install guide + 1 comparison each | rest |

**iptvned.com**
| Cluster | Winner | 301 away |
|---|---|---|
| beste IPTV (9) | `/beste-iptv-abonnement` | all 8 `/blog/beste-*` + `wat-is-de-beste-*` |
| legaal/illegaal (10) | `/iptv-legaal-nederland` | 6 legal blog variants; keep `/iptv-boete-nederland` + `/blog/iptv-opgerold-nederland` (distinct intents, GSC-proven) |
| generic Nederland (13) | `/abonnementen` (commercial) + 1 guide | `iptv-nederland`, `-2`, `-app`, `-forum`, `-forum-2024`, `-reddit`, `-review`, `-trustpilot`, etc. |
| M3U (3) | `/nederland-iptv-m3u` | 2 blog posts |

**iptvesp.com** — build the winners first (they don't exist yet):
| Cluster | Winner (to build) | 301 away |
|---|---|---|
| listas/M3U (5) | new landing `/listas-iptv-m3u` | `listas-iptv-espana`, `iptv-listas-espana`, `listas-iptv-gratis-espana`, `listas-iptv-espana-2025-gratis`, `iptv-m3u-espana` |
| mejor (4) | new `/suscripciones` (commercial) + keep `mejor-iptv-espana` (pos 34) as guide | `mejores-iptv-espana`, `mejor-iptv-suscripcion-2026` |
| legal/multa (3) | new `/iptv-legal-espana` | the 3 blog posts |
| Telegram (2) | `/blog/iptv-espana-telegram` (161 clicks — never touch) | `-telegram-2` |
| Smarters (6) | keep install + comparison | consolidate the rest |

**primeiptv-france.com:** merge the VPN pair (`iptv-vpn-france` wins — GSC 41 imp) and the 4K pair (`iptv-4k-debit-internet` wins); expand or noindex `/revendeur-iptv`.
**iptvfranceofficiel.fr / abonnementiptvofficiel.com:** no mass consolidation needed — differentiate the 3 commercial pages (titles/H1s/angles) as per punch lists.

**Execution tip:** do consolidations 1 cluster/week/site max, and keep a redirect log. After each: update sitemap, request indexing of the winner, watch its query set in GSC for 2–3 weeks.

---

## 5. The 90-Day Program

**Weeks 1–2 — "Stop the damage" (dev-heavy; F1–F5, F7)**
- Shared-template fixes: canonical helper (F1), title templates (F5), icon/schema assets (F4) → deploy to all Next.js sites at once.
- Vercel domain fixes on primeiptv + iptvned (+ smartersprofrance 307) (F2).
- Broken-link sweep on all sites (F3) incl. building iptvesp `/suscripciones` and iptvned `/pandora-iptv`.
- Legal pages: smartersprofrance + iptvesp (F7).
- GSC: verify smartersprofrance; request indexing on the 7 de-indexed URLs + iptvpix `/france-iptv-m3u`.

**Weeks 3–4 — "Wire and measure" (F6, F9, F10)**
- Orphan wiring on primeiptv + iptvned + iptvpix; related-posts modules on all blog templates.
- Sitemap lastmod fixes; schema additions (CollectionPage hubs, FAQPage on primeiptv `/faq`, merged Products).
- Analytics: iptvesp install; iptvpix/iptvned de-duplicate stacks.
- First checkpoint: URL-inspect all previously broken URLs — expect "Submitted and indexed" on the canonical victims.

**Weeks 5–8 — "Performance + consolidation round 1" (F8, §4)**
- Hydration/JS work on the Next.js family; image LCP work on smartersprofrance; font fallbacks.
- Consolidate the highest-value cluster per site (iptvpix legal ×13, iptvned beste ×9, iptvesp listas ×5, primeiptv VPN/4K pairs).
- Re-run Lighthouse portfolio-wide; confirm lab targets met.

**Weeks 9–12 — "Authority" (the real ceiling)**
- Consolidation round 2 (generic-country clusters).
- Link acquisition focused on the six near-page-1 assets: iptvesp `mejor-iptv-espana` (pos 34) & the Telegram post's money links, iptvfranceofficiel `/articles/iptv-smarters-pro` (14.6), primeiptv MAG-box (14) & kids-channels (9), abonnementiptvofficiel Canal+ sport (5–16), iptvned consolidated legal page. Tactics that fit this niche: French/Dutch/Spanish tech forums, comparison-site inclusion, HARO-style quotes, the press pages that already exist (`/presse-media` is currently pure decoration).
- Second checkpoint: GSC month-over-month — iptvpix impressions recovering; iptvesp clicks >300/90d pace; each consolidated cluster showing ONE url per query.

**Budget reality:** weeks 1–4 ≈ 6–8 dev-days total across the portfolio (most fixes are shared); weeks 5–8 ≈ 6 dev-days + content time; weeks 9–12 mostly content/outreach.

---

## 6. Measurement Plan

| What | Where | Cadence | Success signal |
|---|---|---|---|
| Index status of the 7 de-indexed URLs + orphans | GSC URL Inspection | weekly, weeks 1–6 | "Submitted and indexed", Google canonical = user canonical |
| iptvpix recovery | GSC Performance | weekly | impressions > 100/wk by week 6; any clicks by week 8 |
| Broken links | site crawl | monthly | 0 internal 404s |
| Cannibalization | GSC query×page (the API script in this repo re-runs it) | after each consolidation | 1 URL per target query |
| CWV | Lighthouse (lab) now; GSC Experience report as traffic grows | after each perf deploy | TBT<200ms, LCP<2.5s, CLS<0.1 mobile |
| iptvesp concentration risk | GSC pages report | monthly | top-page click share falling below 60% as money pages grow |
| smartersprofrance baseline | GSC (once verified) | from week 1 | data exists at all |

**Housekeeping:** rotate/delete the service-account key used for this analysis (Google Cloud Console → IAM & Admin → Service Accounts → `anawclaude@map-api-279117…` → Keys) once you no longer need me to re-pull data. The re-usable pull script lives in the session workspace and can be re-run with any future key.

---

*Full per-site detail, verification logs, and methodology: see the seven individual audit reports and the GSC performance review in this repository.*
