# Satellite Reactivation — 1 Aug 2026

Owner decision: the three retired domains are **active sites** again (overriding the earlier
consolidate-via-301 recommendation). All three are now fully wired into the dashboard —
audit pipeline, Today queue (one reactivation step per site with its full fix prompt),
Trends, Links matrix (9 columns), Plan and per-site pages.

## The portfolio is now 9 sites

Focus (unchanged): iptvesp · primeiptv-france (flagship) · iptvned · iptvpix
Support: smarters-live · iptvshqiptar
**Satellites (reactivated):** smartersprofrance.fr · iptvfranceofficiel.fr · abonnementiptvofficiel.com

## Lane discipline (the anti-cannibalization contract)

Four French sites now coexist. Each satellite owns ONE lane and never builds pages against
another site's head terms:

| Site | Lane | Money page | Never touches |
|---|---|---|---|
| smartersprofrance.fr | "iptv smarters" install/config long-tail (8,100/mo) | /abonnement-iptv | "application iptv" (smarters-live), "abonnement iptv" (prime) |
| iptvfranceofficiel.fr | "iptv premium" / "iptv hdr" quality angle | /iptv-premium | head terms (prime), free-code bait queries |
| abonnementiptvofficiel.com | trial/deal intent: "test iptv gratuit", "iptv pas cher", "essai iptv 7 jours" | /test-iptv → /iptv-premium | head terms (prime); hardware stays HERE (it ranks) |

Pipeline enforcement: satellites draw article recommendations ONLY from their own keyword
targets (never the shared FR pool), and keywords owned by a money page are marked
"strengthen the page" — the queue can never recommend a parallel article against them.

## Audit state at reactivation (live-verified 1 Aug)

**smartersprofrance.fr** — 38 pages, ~10 Smarters device install guides (the asset).
Defects: apex 307 (should be 308); all 37 internal links route through that redirect
(one root cause — hrefs written against the apex, canonical host is www); 11 titles > 60 chars;
**NOT in Search Console** (verified via sites.list API — the only portfolio site missing).
DataForSEO has no backlink data for it yet.

**iptvfranceofficiel.fr** — 43 pages, in GSC (15 impressions/7d, 18 clicks/90d), www 308 ✓,
1 long title. Problem: query profile skews to free-code/credential hunting that never converts.
Play: /iptv-premium becomes the money page (Offer schema, pricing), reframe gratuit-bait angles,
2026 refresh.

**abonnementiptvofficiel.com** — 43 pages, in GSC (240 impressions/7d, 27 clicks/90d),
www 308 ✓, 1 long title, spam score 15, 1 referring domain. **Still ranks:**
"essai iptv 7 jours" #8 (/test-iptv) and "meilleur boitier iptv" #11 (/boitier-iptv) —
the only page-1/2 money rankings outside the focus sites. Priority: protect (no restructuring,
no slug changes), strengthen both pages, push boitier to page 1.

## Owner actions required

1. **smartersprofrance.fr → Search Console**: add the sc-domain property (DNS verification),
   submit sitemap.xml, add the monitoring service account as a user. Until then the dashboard
   cannot track its traffic. (Also on Today → Step 1.)
2. Vercel → smartersprofrance.fr → Domains: apex→www redirect set to permanent (308).

## Dashboard changes shipped

- 9-site wiring everywhere: sidebar, home site list, hero KPIs, gauges (x/9), country split,
  authority tables, trends cards, keyword pages.
- Today queue: 3 new "Reactivate — <site>" steps, each a complete copy-paste fix prompt.
- Links: matrix is 9 columns (spf/ifo/aio join every platform row; completed rows reopen
  until their 3 new boxes are ticked); platform-batch prompt covers all 9; satellites are
  "light" link tier.
- New crit alert when any site is missing from Search Console (verified fact, not inference).
- Series colors s7–s9 added to the design system (light + dark).
