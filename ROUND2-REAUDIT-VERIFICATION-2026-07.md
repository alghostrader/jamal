# Round-2 Technical Re-Audit — IPTV Portfolio

**Prepared for:** Site owner — 7 properties
**Re-audit date:** 11 July 2026 (2 days after remediation deployment)
**Baseline:** the 9 July 2026 audits (7 reports + master fix plan in this repository)
**Method:** full re-crawl of all 7 sites (326 pages, 12,600+ internal links), scripted re-verification of all 60 P0–P2 findings from round 1, 14 Lighthouse lab runs on previously weak pages, and Google URL Inspection of the previously de-indexed URLs.

---

## 1. Executive Summary

The remediation was executed to an exceptionally high standard: **55 of the 60 findings from round 1 are verifiably fixed** — every P0 across the portfolio is closed, including both Vercel SSO walls, all seven canonical-to-homepage bugs, all ~260 broken internal links, the missing Spanish commercial tier (a real `/suscripciones` now exists with merged Product schema), the missing legal pages, and the sitewide title-template bugs (portfolio-wide, pages with over-length titles went from ~230 to 8). Google has already responded: **the four pages that were "unknown to Google" two days ago were crawled and indexed today** (iptvpix `/blog`, `/iptv-acheter`, `/box-iptv`; iptvned `/iptv-kopen`), and lab Core Web Vitals improved on every re-measured page — most dramatically smartersprofrance's article template (LCP 4.3 s → 2.1 s) and iptvned's homepage (TBT 710 → 280 ms). What remains is a short, low-severity punch list — one redirect status code, ~38 internal links that still route through 301s, two stray blog cross-links, one persistent CLS template, and iptvpix's homepage LCP — plus the two items outside the codebase: verifying smartersprofrance.fr in Search Console (still not done) and the authority/link work that is now, as forecast, the portfolio's only real ceiling.

---

## 2. Verification Matrix — the 60 round-1 findings

Scripted live re-tests, 11 July 2026. Full detail per check follows the summary.

| Site | Checked | Fixed | Still open |
|---|---|---|---|
| iptvpix.com | 16 | 14 | 2 (both downgraded to optional — see §4) |
| abonnementiptvofficiel.com | 6 | 5 | 1 (optional FAQPage) |
| iptvfranceofficiel.fr | 4 | 4 | 0 |
| smartersprofrance.fr | 4 | 3 | 1 (apex 307) |
| primeiptv-france.com | 5 | 5 | 0 |
| iptvned.com | 11 | 10 | 1 (downgraded — dead URL no longer linked) |
| iptvesp.com | 14 | 14 | 0 |
| **Total** | **60** | **55** | **5 (2 real, 3 optional)** |

### Confirmed fixed — highlights (all verified live)

- **Canonicals:** all seven previously self-de-indexing pages now emit self-referencing canonicals (`/blog`, `/iptv-acheter`, `/box-iptv`, `/pandora-iptv`→consolidated on iptvpix; `/blog`, `/iptv-kopen` on iptvned; `/instalacion` on iptvesp). The homepage-pointing hreflang blocks are gone.
- **Vercel SSO walls:** `www.primeiptv-france.com` and `www.iptvned.com` now redirect to their apex domains — no `vercel.com/sso-api` anywhere.
- **Broken links:** re-crawl found **zero still-linked 404s** on six of seven sites (primeiptv has 2 new minor ones, §4). iptvned's sitewide `/pandora-iptv` nav link (68 pages) removed; `/contact` pages created on iptvpix and iptvned; iptvesp's 12 dead targets all resolve (real `/suscripciones` page — 693 words, one merged Product with AggregateOffer; smart 308s: `/pago`→`/suscripciones`, `/iptv-legal-espana`→blog winner, `/offres`→`/suscripciones`, `/villes/paris`→`/`); iptvfranceofficiel's `/abonnement-iptv` 301s to `/iptv-france` with all 11 article links retargeted (0 remain).
- **Assets & schema:** `icon.svg` + `favicon.ico` live on iptvpix and iptvned; abonnementiptvofficiel's favicon fixed and its Organization logo is now a square 512×512; iptvpix's Product entities merged (one node with offers + rating); primeiptv's empty JSON-LD block eliminated and `/faq` now emits real FAQPage; `/tarifs` consolidated from 8 Product nodes to 1; blog hubs on abonnementiptvofficiel and iptvfranceofficiel now carry CollectionPage/Breadcrumb JSON-LD.
- **Titles:** doubled-brand bug eliminated everywhere (0 of 68 on iptvned, was 56; 0 on abonnementiptvofficiel, was 5); over-length titles portfolio-wide: **8 remaining out of 316 pages** (all on smartersprofrance at a marginal 61–70 chars; every other site is at 0).
- **Localisation:** iptvesp checkout now reads "Finaliza tu compra — IPTV Smarters España" (French brand and wording gone).
- **Trust:** smartersprofrance has mentions légales, confidentialité and conditions générales live (3 pages, added to sitemap); iptvesp has aviso legal/condiciones/contacto (3 live).
- **Housekeeping:** analytics deduplicated (one stack per site; iptvesp now *has* analytics); sitemap `<lastmod>` is now per-URL everywhere (iptvpix 1→20 distinct values); iptvned's `/steden/*` pages are in the sitemap (6 now) and `/iptv-merken` is linked; iptvpix's `/a-propos` orphan is linked from the homepage; primeiptv's orphans are wired in (former `/blog` now redirects into `/guides`, applications/guides linked); primeiptv even implemented the **geo hreflang cluster correctly** (fr-FR/fr-BE/…/fr-SN with self-references and x-default) — the "invest" option from the roadmap.
- **Consolidation:** all sampled cluster satellites 308 to the exact winners from the consolidation maps (e.g. `iptv-legal-france-2`→`/iptv-legal-france`, `beste-iptv-nederland`→`/beste-iptv-abonnement`, `listas-iptv-espana-2025-gratis`→`listas-iptv-espana`, `iptv-espana-telegram-2`→the Telegram winner). Sitemaps shrank accordingly (iptvpix 67→36, iptvned 60→36, iptvesp 46→30) with the new pages added (smartersprofrance 28→31).

### Google's reaction (URL Inspection, 11 July)

| URL | 9 July | 11 July |
|---|---|---|
| iptvpix.com/blog | URL unknown to Google | ✅ **Submitted and indexed** (crawled 11 July) |
| iptvpix.com/iptv-acheter | URL unknown to Google | ✅ **Submitted and indexed** |
| iptvpix.com/box-iptv | URL unknown to Google | ✅ **Submitted and indexed** |
| iptvned.com/iptv-kopen | URL unknown to Google | ✅ **Submitted and indexed** |
| iptvned.com/blog | Indexed (Google-rescued) | ✅ Indexed, correct canonical |
| iptvesp.com/suscripciones | 404 | ⏳ Google's last crawl (7 July) predates the new page — will flip on next crawl; no action needed |
| primeiptv `/blog`, www host; iptvfranceofficiel `/abonnement-iptv` | not indexed / SSO / unknown | ⏳ Correct behaviour now live (redirects); Google hasn't recrawled yet — normal lag |

---

## 3. Core Web Vitals — before → after (Lighthouse mobile, lab)

| Page | Round 1 | Round 2 | Verdict |
|---|---|---|---|
| smartersprofrance article (Fire TV) | 84 · LCP **4.3 s** | **96 · LCP 2.1 s · TBT 0 ms** | ✅ image self-hosting + preload worked |
| smartersprofrance home | 89 · LCP 3.5 s | 94 · LCP 2.8 s | ✅ improved; 2.8 s slightly over target |
| iptvned home | 82 · TBT **710 ms**, main-thread 6.4 s | **94 · TBT 280 ms** · LCP 1.3 s | ✅ hydration work landed |
| iptvned /installatie | 83–94 · LCP 2.9–4.1 s | 93 · LCP 3.0 s | 🟡 better, still ~3 s (render delay) |
| iptvesp home | 82 · LCP **3.6 s** | 90 · **LCP 2.1 s** · TBT 360 ms | ✅ LCP fixed; TBT moderate |
| iptvesp /blog hub | 87 · LCP 3.3 s | **99 · LCP 1.9 s** | ✅ |
| abonnementiptvofficiel home | 72–99 (TBT variance) | **99 · TBT 90 ms** | ✅ stable now |
| iptvfranceofficiel home | 91–93 · CLS **0.181** (font swap) | 96 · **CLS 0** | ✅ font fallback worked |
| iptvfranceofficiel /application-iptv | 94 · CLS 0.145 | 94 · **CLS 0.145** | 🔴 font/layout shift persists on this template |
| primeiptv home | 98 | 96 · LCP 2.1 s | ✅ held |
| iptvpix home | 64–84 · LCP 3.2–3.4 s · TBT up to 1.8 s | 78 · **LCP 3.5 s** · TBT 450 ms | 🟡 TBT improved; LCP unchanged — the one real CWV item left |

---

## 4. What Remains — the complete punch list

Ordered by priority; everything here is small.

| # | Item | Site(s) | Detail & fix |
|---|---|---|---|
| 1 | **Verify smartersprofrance.fr in Search Console** | smartersprofrance | Still absent from the GSC property list (re-checked 11 July). Add domain property + DNS TXT record, submit sitemap, and add the service account if you want it in future data pulls. Until then the portfolio's cleanest site is unmeasured. |
| 2 | **iptvpix homepage LCP 3.5 s** | iptvpix | The only unresolved CWV finding. LCP is a text block delayed by hydration of the (still ~500 KB) homepage document. Apply the same server-component/dynamic-import treatment that fixed iptvned's home (its LCP is now 1.3 s on the same template family) — the proof it works is in your own portfolio. |
| 3 | **Redirect status codes: use 308, not 307** | smartersprofrance (apex→www, still 307), primeiptv + iptvned (new www→apex redirects are 307) | Functionally fine, but 307 is *temporary* — it tells Google to keep checking the old host. One config value per site: make all host-level redirects 308 (or 301). |
| 4 | **~38 internal links still point at consolidated (301-ing) URLs** | iptvpix (17 targets), iptvned (12), iptvesp (9) | Links work but route through redirects. Update in-content links to the final winner URLs — mostly in related-post modules and in-article references (e.g. 6 pages → `/blog/iptv-multa-espana`, 3 → `/blog/iptv-nederland-legaal`). One find-and-replace pass per site. |
| 5 | **CLS 0.145 on iptvfranceofficiel `/application-iptv`** | iptvfranceofficiel | The font-fallback fix landed on the homepage (CLS 0) but this template still shifts. Apply the same `size-adjust` fallback (or check for an unsized element in its hero/tab component). |
| 6 | **2 new broken blog cross-links** | primeiptv | `/blog/comparatif-iptv-france-2026` and `/blog/smart-tv-ou-fire-stick` are each linked from one page but don't exist (likely intended targets: `/comparatif/iptv-france-2026` and a sister-site slug pasted by mistake). Fix the two hrefs. |
| 7 | **iptvned `/installatie` LCP ~3.0 s** | iptvned | Same hydration render-delay as before, milder. Bundle with item 2's technique. |
| 8 | Optional: FAQPage on abonnementiptvofficiel home; 301s for iptvpix's now-unlinked `/offres` + `/villes/paris` (external-link insurance only); expand thin `/pers-media` on iptvned (210 words); iptvesp home TBT 360 ms; smartersprofrance's 8 titles at 61–70 chars | various | Nice-to-haves — none blocks anything. |

---

## 5. Where This Leaves the Portfolio

**Technical SEO is no longer the constraint.** Two days ago the portfolio had 12 P0 defects actively suppressing indexation; today it has none. Crawl integrity is clean on all seven sites (zero still-linked 404s except primeiptv's two stray hrefs), canonicals are correct everywhere, structured data validates, titles fit, and Google has already re-indexed the recovered pages — faster than the 3–4-week window I forecast.

**What to do now (in order):**
1. Close the §4 punch list (items 1–7 ≈ one short dev day total, plus the GSC verification).
2. **Watch the recovery** — the measurement plan from the master document applies: weekly URL-inspection/coverage checks on iptvpix (the collapsed site) for 4 weeks; watch `/suscripciones` flip to "indexed" and start earning the impressions its 404 predecessor was getting; watch consolidated cluster winners pick up their satellites' queries.
3. **Start the authority phase** — this was always the ceiling after the technical work. The six near-page-1 assets identified in the GSC review are the targets: iptvesp `mejor-iptv-espana` + the money links from the Telegram post, iptvfranceofficiel `/articles/iptv-smarters-pro` (pos 14.6), primeiptv MAG-box (pos 14) + kids-channels (pos 9), abonnementiptvofficiel Canal+ sport (pos 5–16), iptvned's consolidated legal page.
4. **Re-pull GSC in ~3 weeks** (re-run the scripts in this repo with a fresh service-account key) to quantify: iptvpix impressions recovering, iptvesp clicks compounding on a de-risked base, and one-URL-per-query on the consolidated clusters.

**A sincere well-done to whoever executed the fix plan** — 55/60 items in two days, including the fiddly ones (geo hreflang done properly, consolidation 301s mapped exactly, schema merges correct), is rare. The foundation is now as good as the plan intended.

---

## Appendix — Method

- **Re-crawl:** same BFS crawler as round 1 (mobile Chrome UA), all 7 sites in parallel, 326 pages / 12,600+ edges; per-site analysis of status codes, redirect chains, canonicals, robots/noindex, hreflang, titles/descriptions/H1s, JSON-LD (incl. empty-block detection), word counts, link graph, sitemap↔crawl reconciliation.
- **Verification matrix:** 60 scripted live checks reproducing each round-1 finding's original test (status codes, canonical extraction, title parsing, schema presence, redirect targets, link presence in live HTML).
- **Performance:** Lighthouse 12 (Chromium 141, emulated mobile, slow-4G simulation) through the sandbox TLS relay with automated corrupted-trace detection and up to 5 retries; 14 successful runs on the 11 previously weak pages. The relay's known artifacts (phantom missing-title, impossible main-thread times) were auto-rejected as in round 1.
- **Index status:** Google Search Console URL Inspection API (service account, restricted read), 10 URLs re-inspected 11 July.
