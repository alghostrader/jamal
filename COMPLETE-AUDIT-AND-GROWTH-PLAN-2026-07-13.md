# Complete Technical Audit & Growth Plan — IPTV Portfolio

**Prepared for:** Site owner — 7 properties
**Audit date:** 13 July 2026
**Data sources:** full crawl of all 7 sites (326 pages, 12,600+ internal links, 11–13 July), 14 Lighthouse lab runs on key templates, Google Search Console API (search analytics through 10 July + URL Inspection on 13 July), DataForSEO API (ranked keywords, search volumes, backlink profiles, 13 July)
**Properties:** iptvpix.com · abonnementiptvofficiel.com · iptvfranceofficiel.fr · smartersprofrance.fr · primeiptv-france.com · iptvned.com · iptvesp.com

---

## 1. Executive Summary

Following the remediation sprint completed on 11 July, the portfolio's technical foundation is now clean — all seven sites crawl perfectly (zero still-linked 404s on six of seven, correct canonicals everywhere, valid structured data, working host configurations), Google has already re-indexed the pages the old canonical bug had erased, and Core Web Vitals are green on 12 of 14 measured templates. The market data now quantifies what the constraint really is: the keywords this portfolio targets carry **27,100 monthly searches for "abonnement iptv", 49,500 for "iptv smarters pro", 12,100 for "iptv nederland" and 4,400 for "iptv españa"**, yet the seven domains together hold only **20 top-100 rankings and 1–37 referring domains each** (three domains have no known backlinks at all) — an authority gap, not a technical one. The 30-day plan therefore has three tracks: finish the 7-item technical punch list (~1 dev-day), protect and monetise iptvesp.com's accelerating win (238 clicks/90d, 81 in the last week alone), and begin systematic link acquisition aimed at the six pages the data shows are within striking distance of page 1.

---

## 2. Portfolio Scoreboard (all data current as of 13 July 2026)

| Site | Tech health | GSC clicks 90d (last 7d) | Top-100 keywords (DFS) | Backlinks / ref. domains | Verdict |
|---|---|---|---|---|---|
| iptvesp.com | 🟢 clean | **238 (81)** 📈📈 | 5 | 41 / 37 | The growth engine — protect it |
| primeiptv-france.com | 🟢 clean | 40 (3) 📈 | 4 | 1 / 1 | Healthy structure, invisible domain |
| iptvned.com | 🟢 clean | 35 (1) ➡️ | 10 | 14 / 13 | News-spike faded; legal cluster consolidating |
| iptvpix.com | 🟢 clean (recovered 11 July) | 25 (0) 🕐 | 0 | 41 / 35 | Re-indexed; traffic recovery pending |
| iptvfranceofficiel.fr | 🟢 clean | 18 (3) ➡️ | 0 | **0** | No footprint despite clean tech |
| abonnementiptvofficiel.com | 🟢 clean | 17 (4) ➡️ | 1 | **0** | Same |
| smartersprofrance.fr | 🟢 clean | **not in GSC** | 0 | **0** | Unmeasured; verify it |

**Technical audit summary per site** (full detail in the round-2 verification report and the seven per-site audits in this repository):

- **Crawl & architecture:** every site ≤ 3 clicks deep; sitemap ↔ crawl reconciliation exact on all seven; consolidation 301s all map to the intended winner URLs; zero orphans remaining; the only crawl defects left are two stray blog hrefs on primeiptv and ~38 internal links that still route through consolidation 301s (work, but pass equity meanwhile).
- **Indexability:** self-referencing canonicals on 316/316 indexable pages; checkout flows correctly noindexed; robots.txt clean with AI-crawler allowances; per-URL sitemap lastmod everywhere; primeiptv's geo cluster now carries a correctly reciprocal fr-XX hreflang set.
- **Core Web Vitals (lab, mobile):** 12 of 14 re-measured templates score 90–99. Remaining ambers: iptvpix homepage (78, LCP 3.5 s — hydration render-delay) and iptvned `/installatie` (93 but LCP ~3.0 s); one template CLS regression persists on iptvfranceofficiel `/application-iptv` (0.145).
- **Structured data:** Organization/WebSite sitewide on all sites; Article/BlogPosting + Breadcrumb on all post templates; merged Product+AggregateOffer on every pricing page; FAQPage live on primeiptv; hub pages carry CollectionPage. No parse errors, no empty blocks, no 404 schema assets anywhere.
- **Mobile & security:** viewport and tap-target checks pass portfolio-wide; TLS 1.3 + HSTS (preload) + CSP on all sites; zero mixed content; both former Vercel SSO walls are gone (www hosts redirect to apex — currently 307, see fix list).
- **Trust:** legal/contact pages now present on all seven sites.

---

## 3. The Market vs. the Portfolio (DataForSEO, 13 July)

**Demand (monthly searches):**

| Market | Keyword | Volume | Portfolio's best position today |
|---|---|---|---|
| FR | iptv smarters pro | **49,500** | — (smartersprofrance not yet ranked top-100; iptvfranceofficiel's Smarters article at ~15 per GSC) |
| FR | abonnement iptv | **27,100** | ~64–76 (GSC; nothing top-100 in DFS) |
| FR | boitier iptv | 14,800 | — |
| FR | iptv france | 9,900 | ~78–83 |
| NL | iptv nederland | 12,100 | 63 (iptvned homepage) |
| NL | iptv kopen | 6,600 | — (`/iptv-kopen` re-indexed 11 July) |
| ES | iptv españa | 4,400 | ~40 (mejor/listas posts) |
| ES | listas iptv | 1,900 | 40–42 (`/blog/iptv-listas-espana`) |
| NL | iptv illegaal | 1,300 | 70 (iptvned legal post) |
| ES | listas iptv españa telegram | 390 | **~5 (GSC — the portfolio's one page-1 asset)** |

**Authority (DataForSEO backlinks):** iptvpix 41 backlinks / 35 ref. domains (domain rank 51/1000); iptvesp 41 / 37; iptvned 14 / 13; primeiptv 1 / 1; **abonnementiptvofficiel, iptvfranceofficiel and smartersprofrance: zero backlinks in the index.** For context, page-1 competitors on "abonnement iptv" typically hold hundreds of referring domains. This — not the code — is why clean sites rank at position 60–90.

**What this means:** the portfolio's only current page-1 ranking ("…telegram", 390 vol) produces 84% of all portfolio clicks. Winning even mid-tail terms (1,000–5,000 vol) at these authority levels requires concentrated links on few pages, not thin effort across seven domains. The roadmap (§5) reflects this: consolidate effort behind one primary domain per market — iptvesp (ES), primeiptv or iptvpix (FR — decide once iptvpix's recovery is measurable), iptvned (NL) — and let the satellites feed them.

---

## 4. Prioritized Fix List (Impact × Effort)

| # | Action | Impact | Effort | Priority |
|---|---|---|---|---|
| 1 | **Verify smartersprofrance.fr in Search Console** (DNS TXT; still absent from the property list as of 13 July) and submit its sitemap. The portfolio's cleanest site is flying blind, and it targets the biggest keyword in the portfolio (49.5k/mo). | **High** | **Trivial** | **P0** |
| 2 | **Get `/suscripciones` (iptvesp) indexed:** page is live and correct, but Google's last crawl (7 July) predates it — it's still "Not found (404)" in the index while real demand queues behind it. Request indexing in GSC UI today; add 2–3 internal links from the Telegram post (the site's only authority page). | **High** | **Trivial** | **P0** |
| 3 | **Authority track — start now:** target list = iptvesp `mejor-iptv-espana` (pos ~40, 720 vol) + `iptv-listas-espana` (pos 40, 2×320 vol), iptvfranceofficiel `/articles/iptv-smarters-pro` (GSC pos 14.6, 49.5k-vol query family), primeiptv `/installation/mag-box` (pos 11, 170 vol — one push from page 1) + `qu-est-ce-que-l-iptv` (pos 30–39, ~900 vol combined), iptvned consolidated legal page (pos 25–82 across a 1.9k-vol query family). Tactics: FR/NL/ES tech-forum presence, comparison-site inclusions, guest contributions, digital-PR angle on the (already-ranking) legality/enforcement content. Target: +10 referring domains per priority page in 30 days. | **High** | **High (ongoing)** | **P0** |
| 4 | **Finish the technical punch list** (≈1 dev-day, from the round-2 report): switch the three 307 host redirects to 308 (smartersprofrance apex, primeiptv + iptvned www); update the ~38 internal links that point at consolidation-301 URLs; fix primeiptv's 2 stray blog hrefs; fix CLS 0.145 on iptvfranceofficiel `/application-iptv` (apply the font fallback that fixed its homepage). | **Med** | **Low** | **P1** |
| 5 | **iptvpix homepage LCP (3.5 s, Perf 78):** apply the server-component/dynamic-import treatment that took iptvned's identical template to LCP 1.3 s. Also bundle iptvned `/installatie` (LCP ~3.0 s). | **Med** | **Med** | **P1** |
| 6 | **iptvesp monetisation of momentum:** the Telegram post (81 clicks/wk and compounding) needs a conversion module (inline offer block linking `/suscripciones`), and the site needs 2–3 more posts in the same intent family (e.g. "grupos telegram iptv riesgos", "alternativas a telegram iptv") interlinked with it — extend the win before competitors copy it. | **Med-High** | **Med** | **P1** |
| 7 | **FR head-term decision:** four French sites split the same head terms with zero combined top-100 presence. Within 30 days, pick the primary FR commercial domain (recommendation: decide after 2 weeks of iptvpix recovery data — if impressions return strongly, iptvpix's content depth makes it the flagship; otherwise primeiptv's healthier distribution wins) and redirect effort — not necessarily domains — accordingly: links, new content, and internal cross-referencing go to the chosen one. | **High** | **Low (a decision)** | **P1** |
| 8 | Watch iptvpix recovery weekly (GSC coverage + impressions). If impressions haven't begun recovering by ~25 July, escalate: the domain may carry trust baggage beyond the fixed technical issues, which strengthens the case for primeiptv as FR flagship. | **Med** | **Low** | **P2** |
| 9 | smarters-live.com: fold into smartersprofrance.fr (301 its 2 pages) once #1 is done — three "Smarters" presences dilute one 49.5k-vol opportunity. | **Low-Med** | **Low** | **P2** |
| 10 | Optional polish from round 2: FAQPage on abonnementiptvofficiel home; iptvned `/pers-media` thin page; iptvesp home TBT 360 ms; smartersprofrance's 8 titles at 61–70 chars. | **Low** | **Low** | **P3** |

---

## 5. 30-Day Roadmap

**Week 1 (13–19 July) — unblock and aim**
1. Verify smartersprofrance in GSC + submit sitemap (#1). Request indexing on `/suscripciones` (#2).
2. Ship the 1-day technical punch list (#4).
3. Add the conversion module to the iptvesp Telegram post; brief the 2–3 follow-up posts (#6).
4. Compile the outreach target list for the six priority pages (#3): 20 FR / 10 NL / 10 ES prospects (forums, blogs, comparison sites, newsletters).

**Week 2 (20–26 July) — build**
5. Publish iptvesp follow-up posts, interlinked with the Telegram winner and `/suscripciones`.
6. First outreach wave (15–20 contacts); aim for the first 5 placements.
7. iptvpix homepage LCP work (#5).
8. Checkpoint: iptvpix impressions trend (#8); `/suscripciones` indexation confirmed; smartersprofrance's first GSC data lands.

**Week 3 (27 July – 2 Aug) — decide**
9. FR flagship decision (#7) based on iptvpix's two-week recovery curve; re-point internal cross-site links and outreach targets accordingly.
10. Second outreach wave; digital-PR pitch on the legality/enforcement angle (iptvned's `iptv-opgerold` heritage + iptvfranceofficiel's Arcom content — journalists already search this topic: "iptv nieuws" is a ranked query).
11. Fold smarters-live.com into smartersprofrance (#9).

**Week 4 (3–9 Aug) — measure and iterate**
12. Full data re-pull (GSC + DataForSEO ranked-keywords; scripts are in this repository — run with fresh keys). KPIs: portfolio ≥ 25 top-100 keywords (from 20); iptvesp ≥ 300 clicks/90d pace with `/suscripciones` earning impressions; every priority page +≥5 ref. domains; iptvpix impressions ≥ 100/week or FR-flagship decision executed.
13. Write the August plan from the deltas — by then the data will say which of the six priority pages is moving and deserves the concentrated push.

---

## 6. Verification of the 5 Highest-Priority Findings

| Finding | Verification (13 July) |
|---|---|
| 1. Authority gap is the binding constraint | ✅ **Confirmed via two independent sources** — DataForSEO: 0–10 top-100 keywords and 0–37 referring domains per domain (three domains: zero backlinks); GSC: money terms at positions 60–90 while the sole page-1 asset delivers 84% of clicks |
| 2. Technical remediation held | ✅ **Confirmed** — 55/60 round-1 findings re-verified fixed on 11 July (full matrix in the round-2 report); spot re-checks 13 July consistent; remaining items enumerated in fix #4 |
| 3. iptvesp momentum is real and accelerating | ✅ **Confirmed** — GSC refresh: 238 clicks/90d vs 191 three days prior; 81 clicks in the last 7 days; still 84% single-post concentrated (hence fixes #2/#6) |
| 4. `/suscripciones` not yet indexed despite being live | ✅ **Confirmed** — page returns 200 with correct schema (verified live); GSC URL Inspection still shows "Not found (404)" from the 7 July crawl — indexing request needed |
| 5. smartersprofrance.fr absent from Search Console | ✅ **Confirmed** — property list re-pulled 13 July; not present (and DataForSEO shows zero backlinks — the site needs both measurement and its first links) |

**What could not be confirmed:**
- **Real-user CWV (CrUX):** still unavailable — traffic volumes remain below CrUX thresholds on all properties, so lab Lighthouse remains the best signal; re-check as traffic grows.
- **DataForSEO index freshness:** its ranked-keywords database did not yet reflect iptvesp's Telegram rankings that GSC shows live (DFS databases lag by weeks). Where the two sources disagreed, GSC (Google's own data) was treated as authoritative.
- **iptvpix's recovery trajectory:** re-indexation is confirmed, but with pages indexed only 2 days ago there is no traffic signal yet either way — hence the week-2 checkpoint rather than a verdict.
- **Competitor backlink benchmarks:** stated directionally ("hundreds of referring domains") from market norms; a per-competitor DataForSEO pull is a cheap follow-up if you want exact gap numbers per target keyword.

---

## Appendix — Method & Housekeeping

- Crawl/Lighthouse/verification methodology as per the round-1 and round-2 reports in this repository (BFS crawler, Lighthouse 12 with corrupted-trace rejection via the sandbox TLS relay, scripted live re-verification).
- GSC: Search Analytics 12 Apr – 10 Jul window + URL Inspection, service account (restricted).
- DataForSEO: Labs ranked_keywords (per market: FR/NL/ES), Google Ads search_volume, Backlinks summary — total spend ≈ $0.60 of the account balance.
- **Rotate both credentials now that the pulls are done:** the GSC service-account key (Google Cloud Console → IAM & Admin → Service Accounts → Keys) and the DataForSEO password (app.dataforseo.com dashboard) — both have passed through this chat. The pull scripts in this repository accept fresh credentials for the week-4 re-measurement.
