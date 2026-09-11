# DO NEXT — IPTV portfolio · generated 2026-09-11 by the dashboard audit

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

## Do now — 16 tasks, ≈13h 55m

### #1 Compliance — / · iptvesp.com
- id: `07973cd058` · score 100 · Quick ≈105 min · /
- repo: `/Desktop/iptv-espana-pro` (MDX content/blog)
- action: **FIX** → https://iptvesp.com/
- ⚠ legal floor — same day; the scan lists every page
- what: 26 compliance hit(s) on 17 page(s): terms 100 % legal, completamente legal, orange tv, serie a, totalmente legal — pages: /, /blog, /blog/como-elegir-iptv-espana, /blog/cuanto-cuesta-iptv-espana, /blog/iptv-box-espana… Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #2 Compliance — /guides/iptv-vs-apps-streaming-gratuit · primeiptv-france.com
- id: `7aff3549be` · score 100 · Quick ≈30 min · /guides/iptv-vs-apps-streaming-gratuit
- repo: `/Desktop/iptv-pro` (guides-TS (lib/guides-data.ts))
- action: **FIX** → https://primeiptv-france.com/guides/iptv-vs-apps-streaming-gratuit
- ⚠ legal floor — same day; the scan lists every page
- what: 2 compliance hit(s) on 2 page(s): terms 100% légal, sfr tv — pages: /guides/iptv-vs-apps-streaming-gratuit, /guides/iptv-vs-box-orange-free-sfr-bouygues Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #3 Compliance — / · iptvned.com
- id: `7cde570b1c` · score 100 · Quick ≈75 min · /
- repo: `/Desktop/alghostrader.com/iptvflick.nl` (lib/posts.ts)
- action: **FIX** → https://iptvned.com/
- ⚠ legal floor — same day; the scan lists every page
- what: 13 compliance hit(s) on 11 page(s): terms 100% legaal, volledig legaal, ziggo — pages: /, /abonnementen, /blog/iptv-nederland, /blog/iptv-op-android-tv-box-nederland, /blog/iptv-op-iphone-ipad-nederland… Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #4 Compliance — / · iptvpix.com
- id: `4cb24a2ae7` · score 100 · Quick ≈65 min · /
- repo: `iptv-agent-system/output/sites/iptvpix.com` (lib/posts.ts)
- action: **FIX** → https://iptvpix.com/
- ⚠ legal floor — same day; the scan lists every page
- what: 10 compliance hit(s) on 9 page(s): terms 100 % légal, 100% légal, formule 1 — pages: /, /abonnements, /amende-iptv-france, /blog/iptv-gratuit-belgique-suisse, /box-iptv… Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #5 Compliance — /blog/iptv-vpn-france-utile-guide-2026 · smarters-live.com
- id: `4889a2f5da` · score 100 · Quick ≈25 min · /blog/iptv-vpn-france-utile-guide-2026
- repo: `/Desktop/iptv-france-pro` (lib/articles.ts)
- action: **FIX** → https://www.smarters-live.com/blog/iptv-vpn-france-utile-guide-2026
- ⚠ legal floor — same day; the scan lists every page
- what: 1 compliance hit(s) on 1 page(s): terms contourner les restrictions — pages: /blog/iptv-vpn-france-utile-guide-2026 Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #6 Compliance — /articles/code-iptv-xtream-vs-m3u · smartersprofrance.fr
- id: `27eb5345f6` · score 100 · Quick ≈80 min · /articles/code-iptv-xtream-vs-m3u
- repo: `/Desktop/smartersprofrance-fr` (static HTML (articles/))
- action: **FIX** → https://www.smartersprofrance.fr/articles/code-iptv-xtream-vs-m3u
- ⚠ legal floor — same day; the scan lists every page
- what: 15 compliance hit(s) on 12 page(s): terms apple tv+, disney+, ligue des champions, netflix, rtl — pages: /articles/code-iptv-xtream-vs-m3u, /articles/installer-iptv-smarters-pro-android-tv, /articles/installer-iptv-smarters-pro-chromecast-google-tv, /articles/installer-iptv-smarters-pro-iphone-ipad, /articles/installer-iptv-smarters-pro-samsung-smart-tv… Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #7 Compliance — /articles/comment-choisir-un-abonnement-iptv-france · iptvfranceofficiel.fr
- id: `4caa6d5748` · score 100 · Quick ≈45 min · /articles/comment-choisir-un-abonnement-iptv-france
- repo: `/Desktop/iptvfranceofficiel-fr` (MDX content/articles)
- action: **FIX** → https://iptvfranceofficiel.fr/articles/comment-choisir-un-abonnement-iptv-france
- ⚠ legal floor — same day; the scan lists every page
- what: 6 compliance hit(s) on 5 page(s): terms 100 % légal, orange tv, rtl, sfr tv, ufc — pages: /articles/comment-choisir-un-abonnement-iptv-france, /articles/iptv-4k-france, /articles/iptv-legal-en-france, /articles/iptv-sans-buffering-france, /articles/meilleur-abonnement-iptv-2026 Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #8 Compliance — /blog/abonnement-iptv-multi-ecrans · abonnementiptvofficiel.com
- id: `b0eb5b0a02` · score 100 · Quick ≈55 min · /blog/abonnement-iptv-multi-ecrans
- repo: `/Desktop/abonnementiptvofficiel` (MDX content/blog)
- action: **FIX** → https://abonnementiptvofficiel.com/blog/abonnement-iptv-multi-ecrans
- ⚠ legal floor — same day; the scan lists every page
- what: 10 compliance hit(s) on 7 page(s): terms 100 % légal, coupe du monde, formule 1, orange tv, sfr tv — pages: /blog/abonnement-iptv-multi-ecrans, /blog/comment-choisir-un-abonnement-iptv-france, /blog/iptv-arcom-amende, /blog/iptv-legal-en-france, /blog/iptv-sport-premium… Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #9 Compliance — /blog/iptv-a-prawo-w-polsce · rodaktv.com
- id: `06807ca86c` · score 100 · Quick ≈35 min · /blog/iptv-a-prawo-w-polsce
- repo: `⚠ confirm: alghostrader/iptv-polska` (blog/)
- action: **FIX** → https://rodaktv.com/blog/iptv-a-prawo-w-polsce
- ⚠ legal floor — same day; the scan lists every page
- what: 3 compliance hit(s) on 3 page(s): terms 100% legalne, sky — pages: /blog/iptv-a-prawo-w-polsce, /blog/jak-wybrac-dostawce-iptv, /polska-telewizja-w-uk Remove or rewrite every flagged term (title, meta, H1, body, alt); deploy; the next audit re-scans all 11 sites.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: every flagged term removed or rewritten (title, meta, H1, body, alt) / deploy READY / next audit's compliance scan finds zero hits on this site

### #10 Cannibalisation — grupo iptv telegram · iptvsegura.com
- id: `c5801525dd` · score 90 · Quick ≈30 min · GSC pos 1.0 · 0 clicks · 1 impr / 28d
- repo: `⚠ set repo path (not in the owner's report)` (guias/)
- action: **FIX** → https://iptvsegura.com/
- ⚠ owner of the term: iptvesp.com — link to it, never a new URL
- what: segura ranks on 12 term(s) that belong to esp (ES): “grupo iptv telegram” #1, “iptv telegram españa” #2, “iptv m3u telegram” #2, “m3u iptv telegram” #3, “listas iptv telegram” #4, “listas iptv gratis telegram” #6…. Offending page(s): /, /guias/configurar-iptv-apple-tv-iphone, /guias/estafas-iptv-como-evitarlas On segura's page: remove the term from title/H1, keep the page on its own lane, add one contextual link to esp's page for that intent. Do not create a new URL anywhere.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: the term is out of the non-owner page's title and H1 / one contextual link to the owner's page for that intent / next audit: the non-owner site no longer appears in the top 50 for the term (GSC, may lag 2–4 weeks)

### #11 Cannibalisation — iptv prix · abonnementiptvofficiel.com
- id: `ce0229d96a` · score 90 · Quick ≈30 min · GSC pos 2.0 · 1 clicks · 1 impr / 28d
- repo: `/Desktop/abonnementiptvofficiel` (MDX content/blog)
- action: **FIX** → https://abonnementiptvofficiel.com/boitier-iptv
- ⚠ owner of the term: primeiptv-france.com — link to it, never a new URL
- what: aio ranks on 13 term(s) that belong to prime (FR): “iptv prix” #2, “iptv abonnement” #2, “fournisseur iptv” #2, “abonnement iptv 12 mois amazon” #2, “ip tv” #2, “iptv” #2…. Offending page(s): /boitier-iptv, /guide-installation On aio's page: remove the term from title/H1, keep the page on its own lane, add one contextual link to prime's page for that intent. Do not create a new URL anywhere.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: the term is out of the non-owner page's title and H1 / one contextual link to the owner's page for that intent / next audit: the non-owner site no longer appears in the top 50 for the term (GSC, may lag 2–4 weeks)

### #12 Cannibalisation — iptv · smartersprofrance.fr
- id: `58cc2a5ef7` · score 73 · Quick ≈30 min · GSC pos 11.0 · 0 clicks · 2 impr / 28d
- repo: `/Desktop/smartersprofrance-fr` (static HTML (articles/))
- action: **FIX** → https://www.smartersprofrance.fr/
- ⚠ owner of the term: primeiptv-france.com — link to it, never a new URL
- what: spf ranks on 7 term(s) that belong to prime (FR): “iptv” #11, “iptv france” #14, “fournisseur iptv” #19, “iptv prix” #30, “iptv abonnement prix” #39, “iptv abonnement” #48…. Offending page(s): /, /abonnement-iptv, /tutoriels On spf's page: remove the term from title/H1, keep the page on its own lane, add one contextual link to prime's page for that intent. Do not create a new URL anywhere.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: the term is out of the non-owner page's title and H1 / one contextual link to the owner's page for that intent / next audit: the non-owner site no longer appears in the top 50 for the term (GSC, may lag 2–4 weeks)

### #13 Backlink — Substack post · rodaktv.com
- id: `lp-substack-rodak` · score 55 · Quick ≈25 min · P1 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://rodaktv.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: Substack post for rodaktv.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow

### #14 Backlink — Hotfrog listing · rodaktv.com
- id: `lp-hotfrog-rodak` · score 55 · Quick ≈25 min · P2 placement · brand / naked anchor
- repo: `—`
- action: **PLACE** → https://rodaktv.com/
- ⚠ anchor = brand or naked URL only — never money keywords
- what: Hotfrog listing for rodaktv.com. Publish the post, then paste the live URL when you tick it: that write IS the ledger.
- deploy-as: owner publishes (signup + CAPTCHA + publish) · guards: no rights-holder / channel / league names · no fake reviews / address
- done when: post published with a brand or naked-URL anchor / live URL logged on the Backlinks page (that list is the ledger) / live fetch: link present + dofollow

### #15 Backlink — adslzone.net — expert quote · iptvesp.com
- id: `lp-gp-adslzone-esp` · score 52 · Deep work ≈90 min · authority 56 · expert quote
- repo: `—`
- action: **PITCH** → https://adslzone.net/
- ⚠ one contextual link, brand or naked-URL anchor, to a guide page (not the pricing page)
- what: Expert quote on adslzone.net (authority 56) for iptvesp.com. Angle: Listas M3U y Telegram: cómo saber si una lista aguantará (checklist técnico) biggest ES connectivity/streaming media; pitch expert comments on IPTV safety, M3U, Fire TV
- deploy-as: owner sends the pitch and handles the editor; Claude writes pitch + article + quote · guards: no rights-holder / channel / league names · no '100% legal' claims · real screenshots we own · author alghostrader
- done when: pitch sent from the owner's mailbox (draft in seo-tools/links/PITCHES-*.md) / editor accepted · article or quote delivered / live URL pasted here → the audit checks it is live + dofollow

### #16 Backlink — letsgodigital.org — expert quote · iptvned.com
- id: `lp-gp-letsgodigital-ned` · score 50 · Deep work ≈90 min · authority 39 · expert quote
- repo: `—`
- action: **PITCH** → https://letsgodigital.org/
- ⚠ one contextual link, brand or naked-URL anchor, to a guide page (not the pricing page)
- what: Expert quote on letsgodigital.org (authority 39) for iptvned.com. Angle: IPTV op je smart TV zonder bufferen: netwerkinstellingen die werken consumer electronics; pitch smart-TV/streaming expert comments
- deploy-as: owner sends the pitch and handles the editor; Claude writes pitch + article + quote · guards: no rights-holder / channel / league names · no '100% legal' claims · real screenshots we own · author alghostrader
- done when: pitch sent from the owner's mailbox (draft in seo-tools/links/PITCHES-*.md) / editor accepted · article or quote delivered / live URL pasted here → the audit checks it is live + dofollow


## Verifying — 5 built, not live yet (what is still missing)

### … Striking distance — iptv shqiptar · iptvshqiptar.com
- id: `98a4408a71` · score 0 · — ≈0 min · GSC pos 9.5 · 1 clicks · 30 impr / 28d
- repo: `/Desktop/iptvshqip` (lib/posts.ts)
- action: **ENHANCE** → https://iptvshqiptar.com/blog/iptv-shqip
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “iptv shqiptar” sits at position 10 with 25 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-11): page is live but its modified date is before 2026-09-08

### … Content — iptv provider · iptvned.com
- id: `dda33ce6cb` · score 0 · — ≈0 min · 880/mo
- repo: `/Desktop/alghostrader.com/iptvflick.nl` (lib/posts.ts)
- action: **ENHANCE** → https://iptvned.com/blog/iptv-providers-nederland
- ⚠ page already targets this term (/blog/iptv-providers-nederland) — no new URL, enhance it
- what: “iptv provider” (880/mo) has no page anywhere in this market.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: article live at https://iptvned.com/blog/iptv-providers-nederland, ≥ 900 words, real hero image / internal links from 2 related pages + money-page CTA / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-11): page is live but its modified date is before 2026-09-06

### … Striking distance — boitier iptv · abonnementiptvofficiel.com
- id: `8fcbe4f4aa` · score 0 · — ≈0 min · GSC pos 20.3 · 5 clicks · 167 impr / 28d
- repo: `/Desktop/abonnementiptvofficiel` (MDX content/blog)
- action: **ENHANCE** → https://abonnementiptvofficiel.com/boitier-iptv
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “boitier iptv” sits at position 23 with 179 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-11): page is live but declares no modified date — add dateModified / og:updated_time so the change can be verified

### … Striking distance — iptv shqiptare · iptvshqiptar.com
- id: `1f5c56622b` · score 0 · — ≈0 min · GSC pos 13.2 · 1 clicks · 25 impr / 28d
- repo: `/Desktop/iptvshqip` (lib/posts.ts)
- action: **ENHANCE** → https://iptvshqiptar.com/blog/iptv-shqip
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “iptv shqiptare” sits at position 14 with 23 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-11): page is live but its modified date is before 2026-09-08

### … Striking distance — meilleur boitier iptv · abonnementiptvofficiel.com
- id: `737de905a9` · score 0 · — ≈0 min · GSC pos 12.6 · 14 clicks · 313 impr / 28d
- repo: `/Desktop/abonnementiptvofficiel` (MDX content/blog)
- action: **ENHANCE** → https://abonnementiptvofficiel.com/boitier-iptv
- ⚠ page already ranks this term — enhance it, never a new URL
- what: “meilleur boitier iptv” sits at position 15 with 199 impressions/28d.
- deploy-as: alghostrader · git push origin main → Vercel auto · guards: title ≤ 60 chars (build fails otherwise) · no rights-holder / channel / league / broadcaster names · real hero image (no icon fallback) · brand or naked-URL anchors only for links
- done when: 3+ internal links point at the ranking page with varied anchors / on-query section refreshed + dateModified bumped / deploy READY + live fetch finds the keyword on the page
- live check (2026-09-11): page is live but declares no modified date — add dateModified / og:updated_time so the change can be verified


## Shipped (live-verified) — 22

- ✓ Striking distance — listas iptv telegram · iptvesp.com · verified 2026-09-11 · keyword present + modified on/after 2026-09-10
- ✓ Technical — THIN PAGES · iptvesp.com · verified 2026-09-11 · no thin pages left in the crawl
- ✓ Technical — THIN PAGES · iptvned.com · verified 2026-09-11 · no thin pages left in the crawl
- ✓ Technical — THIN PAGES · iptvpix.com · verified 2026-09-11 · no thin pages left in the crawl
- ✓ Technical — THIN PAGES · iptvshqiptar.com · verified 2026-09-11 · no thin pages left in the crawl
- ✓ Striking distance — iptv smarters pro telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Striking distance — telegram iptv · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-06
- ✓ Striking distance — iptv smarters telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Striking distance — listas iptv premium telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Content — smarters player lite apk · smartersprofrance.fr · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Striking distance — listas m3u telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-06
- ✓ Striking distance — iptv listas m3u telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Backlink — iptv polska · rodaktv.com · verified 2026-09-08 · 2 new live placement(s) logged for this site since completion
- ✓ Striking distance — lista m3u premium telegram · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Striking distance — grupos telegram iptv · iptvesp.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Striking distance — estafas iptv · iptvsegura.com · verified 2026-09-08 · keyword present + modified on/after 2026-09-08
- ✓ Technical — /polska-telewizja-za-granica · rodaktv.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection
- ✓ Technical — REDIRECT · rodaktv.com · verified 2026-09-06 · host redirect is 308
- ✓ Technical — /test-iptv · rodaktv.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection
- ✓ Content — /blog/iptv-espana-telegram · iptvesp.com · verified 2026-09-06 · keyword present + modified on/after 2026-09-06
- ✓ Technical — /planes · iptvsegura.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection
- ✓ Technical — /abonament · rodaktv.com · verified 2026-09-06 · page(s) PASS in GSC URL Inspection

## Needs Jamal (owner-only / blocked) — 5

- Owner: Add VERCEL_TOKEN to dash/.env so BLOCKED deploys are detected automatically — no VERCEL_TOKEN in dash/.env — deploy state inferred from the live fetch
- Owner: Create the expert-quote accounts (signup + CAPTCHA are owner-only) — Source of Sources · Featured.com · Qwoted · MentionMatch · PressPlugs · ResponseSource Journalist Enquiry Service
- Owner: Semrush API units are at zero — top up so authority readings refresh (5 sites on yesterday's data) — sites on the last reading: prime, ned, spf, ifo, aio
- Owner: Send this week's sales numbers per site — feeds revenue-weighted prioritisation
- Owner: Fill the ⚠ placeholder fields in seo-tools/briefs/ (95 fields, 11 sites) — aio 8 · esp 9 · ifo 8 · ned 8 · pix 8 · prime 9 · rodak 10 · segura 9 · shqip 10 · slive 8 · spf 8

## Monitor — 29 watch items (do not work on these)

- CTR gap: iptv app fire tv · ned · score 51
- Striking distance: iptv prueba gratis · esp · score 51
- Striking distance: prueba gratis iptv · esp · score 51
- Striking distance: iptv smarters pro lite · spf · score 50
- Striking distance: iptv smarters pro fire stick · spf · score 50
- Striking distance: es seguro el iptv · segura · score 49
- Striking distance: iptv opgerold · ned · score 48
- Striking distance: iptv opgerold 2026 · ned · score 48
- Striking distance: iptv app fire tv · ned · score 47
- Striking distance: lista m3u falas · shqip · score 47
- Striking distance: iptv smarters pro apk · spf · score 47
- Authority gap: iptv premium · ifo · score 47
- Striking distance: iptv fire stick · ned · score 46
- Striking distance: telecharger iptv smarter pro apk · spf · score 46
- Striking distance: iptv player es seguro · segura · score 45
- Striking distance: iptv stick · ned · score 45
- Striking distance: ip tv · ned · score 45
- Striking distance: tv shqip smart tv lg · shqip · score 45
- Striking distance: iptv uit de lucht gehaald 2026 · ned · score 44
- Striking distance: illegale iptv · ned · score 43
- Striking distance: iptv legaal · ned · score 42
- Striking distance: .m3u · segura · score 42
- Content gap: proveedor iptv · esp · score 41
- Content gap: serveur iptv · prime · score 41
- Content gap: mejor lista iptv · esp · score 41

## Excluded — 15 out-of-scope (Arab / MENA + rest of Africa) — never work on these

- iptv algerie · prime
- meilleur iptv algérie 2026 · prime
- abonnement iptv algérie · prime
- prix abonnement iptv algérie · prime
- iptv algérie · prime
- iptv abonnement algérie · prime
- iptv algérie prix · prime
- iptv en algerie · prime
- meilleur iptv algerie · prime
- ip tv algerie · prime
- meilleur abonnement iptv tunisie 2026 · prime
- iptv alger · prime
- iptv prix algérie · prime
- carte iptv 2026 tunisie · prime
- iptv maroc 2026 · prime

## Rules
- One keyword, one page, one site per market — ENHANCE the ranking page, never create a competing URL.
- Commits authored by alghostrader (other authors land BLOCKED on Vercel).
- No rights-holder / channel / league / broadcaster names. Title ≤ 60 chars. Real hero image.
- Backlinks: brand or naked-URL anchors only; signup + CAPTCHA + publish = owner only.
