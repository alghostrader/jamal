# Off-Page Authority / Backlink Session — 2026-07-31

**Portfolio (6 IPTV sites):** iptvesp.com · primeiptv-france.com · iptvned.com · iptvpix.com · smarters-live.com · iptvshqiptar.com
**Session type:** off-page authority building (profile citations, contextual backlinks, entity `sameAs` wiring)
**Prepared for:** technical SEO audit

---

## Summary of work

| # | Task | Result |
|---|------|--------|
| 1 | about.me brand profiles | ✅ 6/6 live, each with a backlink to its site |
| 2 | `Organization` schema `sameAs` wiring | ✅ 6/6 deployed + verified live (bidirectional entity cluster) |
| 3 | Medium contextual articles | 4/6 live (2 published today), 2 written & queued |
| 4 | Facebook Pages | 1/6 created (IPTVESP), 5 pending FB creation limit |
| 5 | Crunchbase org profiles (prior in session) | ✅ 6/6 |

**Net today:** 16 external citations/backlinks live (Crunchbase ×6 + about.me ×6 + Medium ×4) + a bidirectional `sameAs` entity cluster on all 6 sites. 1 compliance risk remediated (trademark removal on a live article).

---

## 1. about.me — 6/6 live

Each profile carries a "Visit my company website" backlink to its domain + a brand bio in the site's language (no trademarks). All verified: HTTP 200 + the domain link present in the public HTML.

| Profile URL | Backlinks to |
|---|---|
| https://about.me/iptvesp | iptvesp.com |
| https://about.me/primeiptv | primeiptv-france.com |
| https://about.me/iptvned | iptvned.com |
| https://about.me/iptvpix | iptvpix.com |
| https://about.me/smarterslive | smarters-live.com |
| https://about.me/shqiptar | iptvshqiptar.com |

## 2. Organization `sameAs` — 6/6 deployed & verified

Wired each site's about.me URL into its `Organization` JSON-LD `sameAs`, making the citation bidirectional (profile → site AND site → profile). Committed per repo, deployed via Vercel, confirmed present in each site's rendered HTML.
Note: **smarters-live.com had no `sameAs` at all before today** — now added.

Auditor check: view-source each homepage → JSON-LD `Organization.sameAs` should include the matching `about.me/...` URL.

## 3. Medium — 4/6 live, 2 queued (single author: medium.com/@j.oughia)

High-DA contextual backlinks; different topic/language per site to avoid a templated footprint; paced ~1–2/day (Medium limit: 2 published stories / 24h).

| Article | Site | Status | URL |
|---|---|---|---|
| How to Set Up IPTV Smarters Pro on Any Device (2026) | smarters-live | ✅ published today | https://medium.com/@j.oughia/how-to-set-up-iptv-smarters-pro-on-any-device-2026-step-by-step-guide-1763785249ab |
| Comment choisir un abonnement IPTV en 2026 | primeiptv | ✅ published today | https://medium.com/@j.oughia/comment-choisir-un-abonnement-iptv-en-2026-7-points-à-vérifier-avant-de-payer-c349618e481a |
| IPTV op een Samsung Smart TV instellen (NL) | iptvned | ✅ live (Jul 13) | https://medium.com/@j.oughia/iptv-op-een-samsung-smart-tv-instellen-in-nederland-de-complete-gids-e256acf12868 |
| Cómo elegir un servicio de IPTV fiable en España (ES) | iptvesp | ✅ live + remediated today | https://medium.com/@j.oughia/cómo-elegir-un-servicio-de-iptv-fiable-en-españa-y-no-caer-en-una-estafa-2026-464f579fb352 |
| IPTV en Belgique et en Suisse (FR) | iptvpix | ⏳ written, queued | — |
| IPTV Shqip 2026 (SQ) | iptvshqiptar | ⏳ written, queued | — |

**Compliance remediation (iptvesp article):** removed trademarked league names ("LaLiga", "Champions" — the terms behind the earlier La Liga takedown) → replaced with generic categories; removed a leaked editor note. Preserved the iptvesp.com link and the post's original publish date. Zero trademarks remain on the live page.

## 4. Facebook Pages — 1/6 started

- **IPTVESP** Page created. Action pending: set **Website = https://iptvesp.com** (the backlink), profile picture, @username `iptvesp`, and bio.
- Other 5 (primeiptv, iptvned, iptvpix, smarters-live, iptvshqiptar) pending Facebook's Page-creation limit — will drip out over the next days.
- 6 brand logo avatars (512×512 PNG, matched to each site's favicon) produced for the Page profile pictures.

## 5. Crunchbase — 6/6 (completed earlier in session)

Organization profiles created for all 6 brands. (Exact profile slugs to be captured for future `sameAs` inclusion.)

---

## Pipeline (rate-limited, drips over coming days)
- Medium: publish iptvpix + iptvshqiptar (1/day)
- Facebook: create remaining 5 Pages (1–2/day as limit lifts) + set each Website field
- Optional: add Crunchbase + Facebook URLs into `sameAs` once captured

## Auditor verification checklist
1. Open each about.me URL (section 1) → confirm HTTP 200 + outbound link to the brand domain.
2. View-source each of the 6 homepages → confirm `Organization.sameAs` contains the about.me URL.
3. Open each live Medium URL (section 3) → confirm the in-body outbound link to the brand domain; confirm **no trademarked channel/league names** anywhere in the iptvesp article.
