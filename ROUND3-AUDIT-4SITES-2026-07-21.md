# Round-3 Technical Audit — iptvesp · iptvned · iptvpix · primeiptv

**Prepared for:** Site owner
**Audit date:** 21 July 2026 (8 days after the round-2 verification)
**Scope:** full re-crawl (233 pages, 8,900+ internal links), 20 Lighthouse lab runs (homepage + 3 key templates per site, suspect readings re-run solo), Search Console refresh (through 19 July) + URL Inspection, sitemap/content-diff vs. 11 July.

---

## 1. Executive Summary

Crawl hygiene is now flawless on all four sites — zero broken internal links, zero canonical defects, orphans eliminated (one new unlinked page on iptvesp excepted), and every site shipped new content this week (+8 to +11 pages each, including exactly the Telegram-cluster follow-ups recommended for iptvesp, correctly interlinked). The scoreboard has split decisively: **iptvesp keeps compounding (125 clicks last week, `/suscripciones` now indexed) and primeiptv's impressions tripled week-over-week (90 → 289) with flagship-grade CWV (95–100 on all four templates)** — while **iptvpix remains at zero impressions ten days after full re-indexation**, which now points to domain-level suppression rather than anything technical, and iptvned's traffic is fading with its news query. The fix list this round is short and specific: the `/suscripciones` page's own performance (LCP ~4.2 s on the portfolio's most important new URL), homepage TBT regressions on iptvpix and iptvned, a title-length regression in the newly published content (27 pages > 60 chars across the four sites), and two strategic decisions — anoint primeiptv as the French flagship, and give iptvned a new query target to replace the dying "opgerold" spike.

---

## 2. Site-by-Site State

### iptvesp.com — the engine, still accelerating 📈
- **GSC:** 125 clicks last week (94 the week before; ~10 clicks/wk in April). `/suscripciones` **indexed since 15 July** ✅ and beginning to receive impressions. Traffic still concentrated on the Telegram winner but the base is broadening (34 pages with impressions, up from 32).
- **Crawl:** 48 pages, 0 broken links, 0 canonical issues. The three recommended Telegram-cluster posts are live and correctly interlinked (each links the winner and `/suscripciones`; the winner links `/suscripciones` 7×). +11 new pages total (device guides, MotoGP, pricing guide).
- **New issues:** ① `/blog/que-app-iptv` → actually `que-app-iptv` is in the sitemap with **zero internal links** (new orphan — add it to the app-guides linking block). ② **`/suscripciones` performance: Perf 63–67, LCP 4.1–4.3 s across two independent runs** — the money page is the slowest page on the site (text LCP delayed by hydration; same pattern the other sites fixed). ③ 4 new titles > 60 chars; 6 descriptions > 170.
- **Templates measured:** home 90 (LCP 2.0 s) · `/instalacion` 95 · Telegram post 87 (LCP 2.1 s) · **`/suscripciones` 63–67 (LCP 4.1–4.3 s)** 🔴

### primeiptv-france.com — flagship-grade, and Google is responding 📈
- **GSC:** impressions **90 → 289 week-over-week**, clicks 3 → 8. The orphan wiring, FAQPage, and geo-hreflang from the fix rounds are being rewarded. (`/blog` correctly redirects into `/guides`; the www host was recrawled 20 July and processes as a normal redirect.)
- **Crawl:** 76 pages (+10 new guides incl. Formuler Z11, TiviMate, EPG, Xtream-vs-M3U — good intent coverage), sitemap ↔ crawl exact, **zero defects of any kind, zero links via redirects** — the cleanest crawl in the portfolio.
- **CWV: all four templates 95–100** (home 95, `/tarifs` 97, MAG-box guide 100, legal guide 98) — best in portfolio.
- **New issues:** 8 new guide titles > 60 chars. That's the entire list.
- **Strategic:** this is the French flagship on every metric that matters (structure, CWV, Google's response curve). Recommendation below.

### iptvned.com — clean but fading, needs a new play 📉
- **GSC:** clicks 1 → 0, impressions 313 → 198 week-over-week. The "iptv opgerold" news spike is over and the consolidated pages haven't picked up the slack yet.
- **Crawl:** 51 pages, 0 broken links, 0 canonical issues, **0 links via redirects** (was 12 — fully cleaned). +10 new pages: a smart pivot into legal long-tail (`iptv-strafbaar`, `iptv-illegaal-gevolgen`, `iptv-horeca-legaal` — a genuinely un-served B2B angle) plus device guides and a `welke-iptv-app` landing.
- **New issues:** ① **Homepage TBT regression: 780–2,070 ms across three runs** (was 280 ms on 11 July, main-thread back up to 6.4 s) — something shipped with the new content undid the hydration win; diff the homepage bundle. ② **12 new titles > 60 chars** — the worst of the title regression. ③ `/installatie` LCP still ~2.9 s (unchanged, known).
- **Templates measured:** home 71–81 (TBT 🔴) · `/abonnementen` 90 · `/installatie` 88 · opgerold post 96.

### iptvpix.com — technically perfect, commercially flat 🔴
- **GSC:** **zero clicks, 2 impressions in the last week** — ten days after every page was re-indexed (re-confirmed today: `/blog` indexed, `/france-iptv-m3u` recrawled 17 July). The technical explanation is exhausted: with clean tech, full indexation, 41 backlinks (the portfolio's most) and still no impressions, this is domain-level suppression — likely a quality/trust classifier position that predates the fixes.
- **Crawl:** 58 pages, 0 broken links, 0 canonical issues; +8 new pages (device guides + a `test-iptv-gratuit` landing); redirect-routed links down to 9; 3 titles > 60.
- **CWV:** `/abonnements` 99, legal landing 100, blog post 92 — but **homepage 59–70, LCP 3.5–3.7 s, TBT 860 ms+ (main-thread ~6 s)** — the one page never given the hydration treatment, now measured worse than round 2.
- **Strategic:** keep publishing is fine (it costs little), but per the growth plan's week-3 decision gate: **stop waiting for iptvpix.** Move FR links, content priority and internal cross-references to primeiptv. Re-evaluate iptvpix at the 30-day mark; if impressions are still ~zero in mid-August, consider it a sandbox casualty and plan around it.

---

## 3. Prioritized Fix List (Impact × Effort)

| # | Action | Site | Impact | Effort | Priority |
|---|---|---|---|---|---|
| 1 | **Fix `/suscripciones` LCP (4.1–4.3 s, Perf 63–67):** the portfolio's most important new page is its slowest. Same recipe as the sister templates: server-render the pricing cards, defer below-the-fold widgets, keep the page's JS minimal. Target < 2.5 s. | iptvesp | **High** | **Med** | **P0** |
| 2 | **Anoint primeiptv as FR flagship** (decision, then execution): point new FR content, outreach links, and any cross-site references at primeiptv; pause net-new investment in iptvpix pending the mid-August re-check. Google's response curve (impressions ×3 in a week) says it converts effort into visibility *now*. | portfolio | **High** | **Low** | **P0** |
| 3 | **Diagnose the iptvned homepage TBT regression** (280 ms → 780–2,070 ms since 11 July): diff what shipped with the new content wave (a new widget/script is the likely culprit), restore the hydration win. Bundle the same check for iptvpix home (TBT 860 ms+, never fixed). | iptvned, iptvpix | **Med-High** | **Med** | **P1** |
| 4 | **Title-length regression in new content: 27 pages > 60 chars** across the four sites (ned 12, prime 8, esp 4, pix 3) — the old template discipline slipped in the new publishing wave. Trim now while the pages are young, and add a length check to the publishing checklist. | all 4 | **Med** | **Low** | **P1** |
| 5 | **Link the new orphan** `que-app-iptv` (iptvesp) from the app/device guides block + sitemap sanity pass on the other new pages (all others verified linked). | iptvesp | **Med** | **Trivial** | **P1** |
| 6 | **iptvned new query target:** the legal-B2B pivot (`horeca`, `strafbaar`, `gevolgen`) is the right instinct — now concentrate it: interlink the three new legal posts with the consolidated legal landing, and put the site's remaining authority (the opgerold post, while it still has links/history) behind them. Goal: replace the dead news query with evergreen legal long-tail. | iptvned | **Med** | **Med** | **P1** |
| 7 | Update the last redirect-routed internal links (pix 9 targets, esp 3). | pix, esp | **Low** | **Low** | **P2** |
| 8 | `/instalacion`-family LCP (~2.9 s on ned `/installatie`; esp `/instalacion` CLS 0.096 borderline) — fold into #3's performance pass. | ned, esp | **Low-Med** | **Med** | **P2** |

---

## 4. 30-Day Focus (updated)

**This week:** #1 (`/suscripciones` perf) + #5 (orphan link) — iptvesp is where clicks are compounding; every day of a slow money page is paid traffic-conversion lost. Then #2: communicate the flagship decision and re-point the outreach list (the six priority link targets from the growth plan stand, with primeiptv's MAG-box and legal guides promoted to the top).
**Next week:** #3 TBT diagnostics on ned/pix homes; #4 title trims; #6 iptvned legal-cluster concentration.
**Mid-August checkpoint:** re-pull GSC + DataForSEO (scripts in repo, fresh keys): iptvesp target ≥ 175 clicks/wk with `/suscripciones` earning clicks (not just impressions); primeiptv target ≥ 600 impressions/wk and first top-20 rankings on guide queries; iptvned target: legal long-tail impressions replacing the opgerold decline; iptvpix verdict: recover-or-deprioritize.

---

## 5. Verification of the 5 Highest-Priority Findings

| Finding | Verification (21 July) |
|---|---|
| 1. `/suscripciones` slow (LCP 4.1–4.3 s) | ✅ **Confirmed on two independent solo runs** (4.3 s and 4.1 s, Perf 67/63). ⚠️ Its TBT (780–1,100 ms) is directionally real but one trace was corrupted (80 s main-thread — sandbox relay artifact); treat TBT magnitude as approximate. |
| 2. iptvpix zero recovery despite full re-indexation | ✅ **Confirmed via GSC** — 2 impressions in the last 7 days; URL Inspection re-confirms `/blog` indexed and `/france-iptv-m3u` recrawled 17 July. The suppression conclusion is inference from exclusion, not a Google-stated status — noted as such. |
| 3. iptvned homepage TBT regression | ✅ **Confirmed across three runs** (2,070 / 780 ms vs 280 ms on 11 July; main-thread 6.4 s on both recent clean runs). Exact value varies run-to-run; the regression itself is consistent. |
| 4. primeiptv impressions ×3 + flagship CWV | ✅ **Confirmed** — GSC 90 → 289 impressions wk/wk; all four templates 95–100 in this round's lab runs; crawl has zero defects. |
| 5. Title regression in new content (27 pages) | ✅ **Confirmed from today's crawl data** across all four sites; sampled live titles match crawl values. |

**Could not confirm:** real-user CWV (CrUX — still below thresholds portfolio-wide); exact TBT magnitudes on the three flagged pages (relay-induced run variance — ranges reported instead of point values); the *cause* of the iptvned TBT regression (needs a bundle diff, not black-box measurement); and whether iptvpix's suppression is algorithmic or a manual-action-adjacent state — GSC's Manual Actions / Security Issues panels (UI-only, not exposed via API) should be checked by you: if both are clean, the algorithmic-suppression reading stands.

---

*Method as in prior rounds (BFS crawler, Lighthouse 12 with corrupted-trace rejection through the sandbox TLS relay, GSC API with the existing service account). Reports for rounds 1–2 and the growth plan are in this repository.*
