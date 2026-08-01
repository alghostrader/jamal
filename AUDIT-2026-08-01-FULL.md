# Full Portfolio Audit — 1 Aug 2026 (post-fix verification round)

Scope: fresh BFS crawl of all 9 sites · GSC (verified property list + 90d traffic) ·
DataForSEO (backlinks, volumes) · 34 keyword targets re-probed in live Google SERPs ·
fix-prompt verification against the previous crawl.

## 1. Fix verification — what landed (crawl-proven)

| Fix | Before | After | Status |
|---|---|---|---|
| Titles >60 chars, portfolio-wide | 13 (spf 11, ifo 1, aio 1) | **0** | ✅ first time ever |
| smartersprofrance → Search Console | not connected (API-verified) | **connected**, 48 days history | ✅ owner did it |
| ifo /iptv-premium money page | thin | "IPTV Premium 4K — 22 000+ chaînes" + pricing | ✅ live-verified |
| aio /test-iptv + /boitier-iptv strengthening | ~900 words | ~3,100 / ~2,800 words, schema, healthy | ✅ shipped (see §2) |
| spf apex redirect 308 | 307 | **still 307** | ❌ not done (Vercel Domains setting) |
| spf internal links off the redirect | 37 via apex | **still 37** | ❌ not done (one find-and-replace) |
| esp redirect-link nit | 1 | 1 | ⏸ open |

## 2. The one alarm — abonnementiptvofficiel rankings

At reactivation (31 Jul): "essai iptv 7 jours" **#8**, "meilleur boitier iptv" **#11**.
Today (1 Aug, probed twice independently): **both out of the top 100**.

Diagnosis — NOT a technical break: both pages return 200, self-canonical, `index,follow`,
substantial content. The drop coincides exactly with the heavy content overhaul; this is the
classic Google re-evaluation dip after a big edit. Supporting evidence that the underlying
momentum is real: GSC impressions ramped 30 → 67/day on 26–29 Jul, right before the edit.

**Standing rule (2–3 weeks): FREEZE both pages.** No edits, no retitles, no slug/canonical
changes. Support them from around — 2–3 internal links from blog posts with natural anchors.
Positions are re-probed automatically on every audit. Escalate only if still absent ~3 weeks in.
Stakes: "boitier iptv" is a **14,800/mo** head term; the "meilleur" variant is 720/mo.

## 3. SERP probe results (34 targets, live)

- 🏆 **iptvesp.com #1** for "listas iptv españa telegram" — the Telegram cluster play confirmed at the top.
- iptvpix brand query: best position 30 (recovery continuing; impressions still returning daily in GSC).
- Everything else: not yet in top 100 — consistent with the authority ceiling (links are the bottleneck, not content).
- "meilleur boitier iptv" added as a tracked target (page-hinted to /boitier-iptv).

## 4. New keywords added to the market pools (live volumes)

FR: iptv sur pc, **iptv freebox (590)**, iptv orange, iptv erreur de lecture (90), meilleur iptv
france, iptv chromecast, **iptv vlc (590)** · ES: iptv legal españa, iptv vlc (260), iptv
chromecast, mejor iptv españa (720) · NL: iptv legaal, iptv werkt niet, iptv chromecast (90).

Next-gap queue after refresh: **prime/pix/slive → "iptv vlc" (590)** (one of them gets it —
the queue issues exactly one), esp → "iptv vlc" ES (260), ned → "iptv chromecast" (90).

## 5. New pipeline guard — cross-site cannibalization (portfolio level)

Trigger: the refreshed pool almost queued "meilleure application iptv" (2,400/mo) on
primeiptv — **iptvpix already published that exact article** ("Meilleure application IPTV
2026 — top 7"). The guard now:
1. marks a keyword covered for ALL same-market sites once any focus/support site covers it
   ("sibling owns it" badge on the Keywords tables);
2. lets KT `page` hints claim keywords market-wide (aio's /test-iptv owns "test iptv gratuit"
   everywhere, not just on aio);
3. satellites' legacy pages do NOT block focus sites (they claim only via explicit hints).

Also flagged and given a fix item: **ifo /application-iptv competes with smarters-live's
device-checker hub** for the "application iptv" head term. Fix: retitle ifo's page to a
premium-angle title, keep it as an internal hub — never two portfolio sites on one head term.

## 6. Portfolio state after this audit

- Tech: cleanest it has ever been — 0 long titles, 0 orphans, 0 canonical mismatches anywhere;
  open items are only spf's apex/links pair and esp's single redirect link.
- Traffic 7d: esp 113 clicks · prime 17 · ned 5 · aio 5 · spf 1 · others 0.
- aio is the satellite with real momentum (240 impressions/7d and ramping) — protect mode.
- Authority remains THE ceiling: prime still 2 backlinks / 2 ref domains. The Links matrix
  (now 9 columns) is the highest-leverage manual work available.

## 7. Standing plan deltas

1. aio: WATCH status — frozen money pages, weekly re-probe (automated in the audit).
2. spf: only 2 items left (apex 308 in Vercel; internal links find-and-replace) — then it
   moves to content refresh phase (install library → 2026).
3. ifo: head-term conflict fix, then premium/HDR lane content only.
4. Content queue continues one-article-per-cycle; next up "iptv vlc" (590/mo FR).
5. Links: platform matrix reopened rows for the 3 satellites — continue top-to-bottom.
