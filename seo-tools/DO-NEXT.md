# DO NEXT — IPTV portfolio · generated 2026-09-08 by the dashboard audit

This file IS the task board (same data as iptv.alghostrader.com/today, lane **Do now**). Work top-down: #1 is the next task.
A task is DONE only when it is live-verified by the next audit (deploy READY + change confirmed on the live URL).

## How to mark a task done (no browser needed)
Append ONE line per task to `seo-tools/daily/task_updates.jsonl`, then commit + push this repo (branch `claude/iptvpix-seo-audit-l68bmx`):
```
{"id": "<id from the task>", "state": "completed", "url": "https://<exact live URL you changed or published>", "date": "YYYY-MM-DD", "by": "iptv-session", "note": "what was changed (1 line)"}
```
States: `completed` (built + deployed) · `deferred` · `dismissed` (with a note why) · `active` (started). Always give the live URL for content/enhance tasks:
the audit fetches it and checks keyword + modified date (add `dateModified` / `og:updated_time` to the page). For a backlink id (`lp-…`) the url is the placement URL.
The next audit merges these lines with the owner's browser ticks (Firestore) and moves the task to Shipped only after the live check passes.

## Do now — 11 tasks, ≈5h 50m

### #1 Backlink — Medium article (max 2/day) · rodaktv.com
- id: `lp-medium-rodak` · score 55 · Quick ≈25 min · P1 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://rodaktv.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: Medium article (max 2/day) for rodaktv.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow

### #2 Backlink — Tumblr blog + 1 post · rodaktv.com
- id: `lp-tumblr-rodak` · score 55 · Quick ≈25 min · P1 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://rodaktv.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: Tumblr blog + 1 post for rodaktv.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow

### #3 Striking distance — grupos telegram iptv · iptvesp.com
- id: `7a02bb1649` · score 52 · Medium ≈40 min · GSC pos 4.0 · 10 clicks · 92 impr / 28d
- repo: `/Desktop/iptv-espana-pro` (MDX content/blog)
- action: **ENHANCE** → https://iptvesp.com/blog/listas-telegram-iptv-espana
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “grupos telegram iptv” sits at position 4 with 92 impressions/28d. Strengthen internal links to the ranking page and refresh the content section matching this query.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page

### #4 Striking distance — iptv smarters telegram · iptvesp.com
- id: `42611f0848` · score 52 · Medium ≈40 min · GSC pos 8.2 · 1 clicks · 10 impr / 28d
- repo: `/Desktop/iptv-espana-pro` (MDX content/blog)
- action: **ENHANCE** → https://iptvesp.com/blog/telegram-listas-iptv-espana
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “iptv smarters telegram” sits at position 8 with 10 impressions/28d. Strengthen internal links to the ranking page and refresh the content section matching this query.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page

### #5 Striking distance — iptv listas m3u telegram · iptvesp.com
- id: `b0afa996c9` · score 52 · Medium ≈40 min · GSC pos 4.2 · 20 clicks · 67 impr / 28d
- repo: `/Desktop/iptv-espana-pro` (MDX content/blog)
- action: **ENHANCE** → https://iptvesp.com/blog/telegram-listas-iptv-espana
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “iptv listas m3u telegram” sits at position 4 with 67 impressions/28d. Strengthen internal links to the ranking page and refresh the content section matching this query.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page

### #6 Striking distance — lista m3u premium telegram · iptvesp.com
- id: `7532ac80e4` · score 52 · Medium ≈40 min · GSC pos 11.9 · 3 clicks · 12 impr / 28d
- repo: `/Desktop/iptv-espana-pro` (MDX content/blog)
- action: **ENHANCE** → https://iptvesp.com/blog/telegram-listas-iptv-espana
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “lista m3u premium telegram” sits at position 12 with 12 impressions/28d. Strengthen internal links to the ranking page and refresh the content section matching this query.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page

### #7 Striking distance — estafas iptv · iptvsegura.com
- id: `5b7c04cc72` · score 52 · Medium ≈40 min · GSC pos 17.9 · 1 clicks · 12 impr / 28d
- repo: `⚠ set repo path (not in the owner's report)` (guias/)
- action: **ENHANCE** → https://iptvsegura.com/guias/estafas-iptv-como-evitarlas
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “estafas iptv” sits at position 18 with 12 impressions/28d. Strengthen internal links to the ranking page and refresh the content section matching this query.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page

### #8 Backlink — Medium article (max 2/day) · iptvesp.com
- id: `lp-medium-esp` · score 45 · Quick ≈25 min · P1 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://iptvesp.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: Medium article (max 2/day) for iptvesp.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow

### #9 Backlink — Tumblr blog + 1 post · primeiptv-france.com
- id: `lp-tumblr-prime` · score 45 · Quick ≈25 min · P1 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://primeiptv-france.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: Tumblr blog + 1 post for primeiptv-france.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow

### #10 Backlink — WordPress.com blog + 1 post · iptvned.com
- id: `lp-wordpress-ned` · score 45 · Quick ≈25 min · P1 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://iptvned.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: WordPress.com blog + 1 post for iptvned.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow

### #11 Backlink — Medium article (max 2/day) · iptvpix.com
- id: `lp-medium-pix` · score 45 · Quick ≈25 min · P1 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://iptvpix.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: Medium article (max 2/day) for iptvpix.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow


## Verifying — 12 built, not live yet (what is still missing)

### … Striking distance — iptv shqiptare · iptvshqiptar.com
- id: `1f5c56622b` · score 0 · — ≈0 min · GSC pos 13.6 · 1 clicks · 23 impr / 28d
- repo: `/Desktop/iptvshqip` (lib/posts.ts)
- action: **ENHANCE** → https://iptvshqiptar.com/blog/iptv-shqip
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “iptv shqiptare” sits at position 14 with 23 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-08): page is live but its modified date is before 2026-09-08

### … Striking distance — iptv shqiptar · iptvshqiptar.com
- id: `98a4408a71` · score 0 · — ≈0 min · GSC pos 10.2 · 1 clicks · 25 impr / 28d
- repo: `/Desktop/iptvshqip` (lib/posts.ts)
- action: **ENHANCE** → https://iptvshqiptar.com/blog/iptv-shqip
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “iptv shqiptar” sits at position 10 with 25 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-08): page is live but its modified date is before 2026-09-08

### … Technical — Thin Pages · iptvshqiptar.com
- id: `f6e1c07475` · score 0 · — ≈0 min · no volume data
- repo: `/Desktop/iptvshqip` (lib/posts.ts)
- action: **FIX** → https://iptvshqiptar.com/
- what: 1. THIN PAGES (P2). 5 page(s) under 300 words: checkout, checkout, checkout, checkout, checkout.
   Expand each to answer its query properly, or consolidate/noindex if they serve n
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: defect fixed in the repo (all flagged pages) / deploy READY / live re-check passes (thin pages ≥ 300 words / redirect 308 / zero broken links)
- live check (2026-09-08): 5 page(s) still under 300 words live: /checkout?plan=1ekran-3m, /checkout?plan=1ekran-6m, /checkout?plan=1ekran-12m, /checkout?plan=1ekran-24m

### … Striking distance — boitier iptv · abonnementiptvofficiel.com
- id: `8fcbe4f4aa` · score 0 · — ≈0 min · GSC pos 22.3 · 3 clicks · 175 impr / 28d
- repo: `/Desktop/abonnementiptvofficiel` (MDX content/blog)
- action: **ENHANCE** → https://abonnementiptvofficiel.com/boitier-iptv
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “boitier iptv” sits at position 23 with 179 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-08): page is live but declares no modified date — add dateModified / og:updated_time so the change can be verified

### … Striking distance — listas m3u telegram · iptvesp.com
- id: `70f507b6f5` · score 0 · — ≈0 min · GSC pos 5.7 · 40 clicks · 257 impr / 28d
- repo: `/Desktop/iptv-espana-pro` (MDX content/blog)
- action: **ENHANCE** → https://iptvesp.com/blog/telegram-listas-iptv-espana
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “listas m3u telegram” sits at position 6 with 250 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-08): live URL returned HTTP unreachable

### … Backlink — iptv polska · rodaktv.com
- id: `1ec40f062e` · score 0 · — ≈0 min · 1,900/mo
- repo: `⚠ confirm: alghostrader/iptv-polska` (blog/)
- action: **PLACE** → https://rodaktv.com/
- ⚠ links, not content — content alone will not close this gap
- what: Money target “iptv polska” (1,900/mo) is unranked and the site has only 0 referring domains (Semrush).
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow
- live check (2026-09-08): no new live placement logged for this site since completion (tick it on Backlinks with its URL)

### … Technical — Redirect · rodaktv.com
- id: `8162a0a994` · score 0 · — ≈0 min · no volume data
- repo: `⚠ confirm: alghostrader/iptv-polska` (blog/)
- action: **FIX** → https://rodaktv.com/
- what: 1. REDIRECT (P1). A host redirect is 307 (temporary). In Vercel -> Settings -> Domains set it to permanent (308). Verify with curl -sI.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: defect fixed in the repo (all flagged pages) / deploy READY / live re-check passes (thin pages ≥ 300 words / redirect 308 / zero broken links)
- live check (2026-09-08): redirect check failed: HTTPSConnectionPool(host='www.rodaktv.com', port=443): Max r

### … Content — iptv provider · iptvned.com
- id: `dda33ce6cb` · score 0 · — ≈0 min · 880/mo
- repo: `/Desktop/alghostrader.com/iptvflick.nl` (lib/posts.ts)
- action: **ENHANCE** → https://iptvned.com/blog/iptv-providers-nederland
- ⚠ page already targets this term (/blog/iptv-providers-nederland) — no new URL, enhance it
- what: “iptv provider” (880/mo) has no page anywhere in this market.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: article live at https://iptvned.com/blog/iptv-providers-nederland, ≥ 900 words, real hero image / internal links from 2 related pages + money-page CTA / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-08): page is live but its modified date is before 2026-09-06

### … Technical — Thin Pages · iptvpix.com
- id: `e91c45e957` · score 0 · — ≈0 min · no volume data
- repo: `iptv-agent-system/output/sites/iptvpix.com` (lib/posts.ts)
- action: **FIX** → https://iptvpix.com/
- what: 1. THIN PAGES (P2). 5 page(s) under 300 words: checkout, checkout, checkout, checkout, checkout.
   Expand each to answer its query properly, or consolidate/noindex if they serve n
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: defect fixed in the repo (all flagged pages) / deploy READY / live re-check passes (thin pages ≥ 300 words / redirect 308 / zero broken links)
- live check (2026-09-08): 5 page(s) still under 300 words live: /checkout?plan=3mois-1ecran, /checkout?plan=6mois-1ecran, /checkout?plan=12mois-1ecran, /checkout?plan=24mois-1ecran

### … Striking distance — meilleur boitier iptv · abonnementiptvofficiel.com
- id: `737de905a9` · score 0 · — ≈0 min · GSC pos 14.4 · 9 clicks · 232 impr / 28d
- repo: `/Desktop/abonnementiptvofficiel` (MDX content/blog)
- action: **ENHANCE** → https://abonnementiptvofficiel.com/boitier-iptv
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “meilleur boitier iptv” sits at position 15 with 199 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-08): page is live but declares no modified date — add dateModified / og:updated_time so the change can be verified

### … Technical — Thin Pages · iptvesp.com
- id: `984cc3c4dc` · score 0 · — ≈0 min · no volume data
- repo: `/Desktop/iptv-espana-pro` (MDX content/blog)
- action: **FIX** → https://iptvesp.com/
- what: 1. THIN PAGES (P2). 5 page(s) under 300 words: checkout, checkout, checkout, checkout, checkout.
   Expand each to answer its query properly, or consolidate/noindex if they serve n
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: defect fixed in the repo (all flagged pages) / deploy READY / live re-check passes (thin pages ≥ 300 words / redirect 308 / zero broken links)
- live check (2026-09-08): 5 page(s) still under 300 words live: /checkout?plan=1pant-3m, /checkout?plan=1pant-6m, /checkout?plan=1pant-12m, /checkout?plan=1pant-24m

### … Technical — Thin Pages · iptvned.com
- id: `7ef248c3f6` · score 0 · — ≈0 min · no volume data
- repo: `/Desktop/alghostrader.com/iptvflick.nl` (lib/posts.ts)
- action: **FIX** → https://iptvned.com/
- what: 1. THIN PAGES (P2). 5 page(s) under 300 words: afrekenen, afrekenen, afrekenen, afrekenen, afrekenen.
   Expand each to answer its query properly, or consolidate/noindex if they se
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: defect fixed in the repo (all flagged pages) / deploy READY / live re-check passes (thin pages ≥ 300 words / redirect 308 / zero broken links)
- live check (2026-09-08): 5 page(s) still under 300 words live: /afrekenen?plan=3-maanden-1-scherm, /afrekenen?plan=6-maanden-1-scherm, /afrekenen?plan=12-maanden-1-scherm, /afrekenen?plan=24-maanden-1-scherm


## Shipped (live-verified) — 9

- ✓ Content — smarters player lite apk · smartersprofrance.fr · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Striking distance — telegram iptv · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-06
- ✓ Striking distance — listas iptv premium telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Striking distance — iptv smarters pro telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Content — /blog/iptv-espana-telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-06
- ✓ Technical — /polska-telewizja-za-granica · rodaktv.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection
- ✓ Technical — /test-iptv · rodaktv.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection
- ✓ Technical — /planes · iptvsegura.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection
- ✓ Technical — /abonament · rodaktv.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection

## Needs Jamal (owner-only / blocked) — 5

- Owner: Add VERCEL_TOKEN to dash/.env so BLOCKED deploys are detected automatically — no VERCEL_TOKEN in dash/.env — deploy state inferred from the live fetch
- Owner: Send this week's sales numbers per site — feeds revenue-weighted prioritisation
- Owner: Fill the ⚠ placeholder fields in seo-tools/briefs/ (95 fields, 11 sites) — aio 8 · esp 9 · ifo 8 · ned 8 · pix 8 · prime 9 · rodak 10 · segura 9 · shqip 10 · slive 8 · spf 8
- Owner: Review the newest links on abonnementiptvofficiel.com (spam 58) and decide: resume or disavow — link building is paused on this site until you decide
- Owner: Review the newest links on smarters-live.com (spam 62) and decide: resume or disavow — link building is paused on this site until you decide

## Monitor — 93 watch items (do not work on these)

- Striking distance: meilleur boîtier iptv 2026 · aio · score 51
- Striking distance: lista iptv telegram · esp · score 51
- Striking distance: grupos de telegram iptv gratis · esp · score 51
- Striking distance: test iptv · esp · score 51
- Striking distance: iptv essai 7 jours · aio · score 50
- Striking distance: cuentas iptv telegram · esp · score 50
- Striking distance: iptv gratis telegram · esp · score 50
- Striking distance: telegram listas iptv · esp · score 50
- Striking distance: m3u telegram · esp · score 50
- Striking distance: grupos iptv telegram · esp · score 50
- Striking distance: cuentas de iptv gratis telegram · esp · score 50
- Striking distance: cuentas iptv gratis telegram · esp · score 50
- Striking distance: m3u iptv telegram · esp · score 50
- Striking distance: grupo telegram iptv · esp · score 50
- Striking distance: listas iptv gratis telegram · esp · score 50
- Striking distance: canal iptv telegram · esp · score 50
- Striking distance: grupo iptv telegram · esp · score 50
- Striking distance: telegram iptv m3u · esp · score 50
- Striking distance: lista iptv gratis telegram · esp · score 50
- Striking distance: lista m3u gratis telegram · esp · score 50
- Striking distance: grupos de iptv telegram · esp · score 49
- Striking distance: iptv cuentas gratis telegram · esp · score 49
- Striking distance: iptv ios · esp · score 49
- Striking distance: iptv definition · prime · score 49
- Striking distance: listas iptv telegram 2026 · esp · score 49

## Excluded — 15 out-of-scope (Arab / MENA + rest of Africa) — never work on these

- iptv algerie · prime
- meilleur iptv algérie 2026 · prime
- abonnement iptv algérie · prime
- prix abonnement iptv algérie · prime
- iptv algérie · prime
- iptv abonnement algérie · prime
- iptv algérie prix · prime
- ip tv algerie · prime
- iptv en algerie · prime
- meilleur abonnement iptv tunisie 2026 · prime
- iptv alger · prime
- meilleur iptv algerie · prime
- iptv prix algérie · prime
- algerie iptv · prime
- iptv maroc 2026 · prime

## Rules
- One keyword, one page, one site per market — ENHANCE the ranking page, never create a competing URL.
- Commits authored by alghostrader (other authors land BLOCKED on Vercel).
- No rights-holder / channel / league / broadcaster names. Title ≤ 60 chars. Real hero image.
- Backlinks: brand or naked-URL anchors only; signup + CAPTCHA + publish = owner only.
