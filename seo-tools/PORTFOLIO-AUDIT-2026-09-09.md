# Portfolio full audit — what's missing (2026-09-09)

Scope: 11 in-scope sites (ES/FR/NL/PL/AL). Layers checked: technical (live crawl), authority (DataForSEO backlinks), rankings/visibility (DataForSEO Labs, each site in its own market).

**Bottom line:** technical health is *good everywhere* — the gap is **authority** (near-zero portfolio-wide) and, downstream of it, **rankings**. Only iptvesp converts. This confirms the lever is editorial links + low-comp niche content, not more on-page.

---

## Layer 1 — Technical: GOOD (not the problem)

All 11 homepages return 200 with title, meta description, canonical, JSON-LD, single H1, robots.txt and a populated sitemap.xml.

- **No real title-length breaches.** iptvned's title measures 62 only because of the `&amp;` entity (58 rendered).
- **No noindex leaks**, all canonicals present.
- **No hreflang anywhere** — fine for single-market sites; a minor opportunity for pix (BE/CH/FR) and the diaspora sites (rodak, shqip).
- **Thin content:** iptvshqiptar = 16 sitemap URLs, iptvsegura = 33. Everything else 39–106.

Verdict: nothing technical is holding the portfolio back.

---

## Layer 2 — Authority: THE binding constraint

| Site | Domain rank /100 | Ref domains | Nofollow | Backlinks |
|---|---|---|---|---|
| iptvpix.com | **8** | 40 | 16 | 46 |
| iptvesp.com | 0 | 42 | 12 | 45 |
| iptvned.com | 0 | 21 | 11 | 22 |
| abonnementiptvofficiel.com | 0 | 14 | 2 | 14 |
| smarters-live.com | 0 | 13 | 4 | 13 |
| primeiptv-france.com | 0 | 12 | 4 | 12 |
| iptvshqiptar.com | 0 | 7 | **7 (all)** | 10 |
| iptvsegura.com | 0 | 3 | 0 | 3 |
| iptvfranceofficiel.fr | — | not in index | — | — |
| rodaktv.com | — | not in index (5 days old) | — | — |
| smartersprofrance.fr | — | not in index | — | — |

- Only **iptvpix** has any measurable domain rank. Everything else is 0 or too thin to index.
- Links are overwhelmingly nofollow / low-DA → they don't move authority. **This is exactly why daily directory/bookmark links haven't raised DR/AS.**
- **Fix = the editorial guest-post program already drafted** (10 drafts ready to send). That's the single highest-leverage action.

---

## Layer 3 — Rankings/visibility: one winner, the rest mostly invisible

| Site | Market | KW | Top-3 | 4–10 | 11–20 | Est. traffic (ETV) | Read |
|---|---|---|---|---|---|---|---|
| **iptvesp.com** | ES | 23 | **4** | 2 | 0 | **423** | the winner; owns Telegram/M3U niche |
| abonnementiptvofficiel.com | FR | 12 | 0 | 1 | 2 | 103 | best of the FR pack |
| primeiptv-france.com | FR | 17 | 0 | 0 | 1 | 353* | *inflated by one high-CPC term |
| smartersprofrance.fr | FR | 19 | 0 | 0 | 0 | 35 | all pos 21–80 |
| iptvned.com | NL | 24 | 0 | 1 | 0 | 17 | many kw, none in top-3 |
| iptvsegura.com | ES | 4 | 0 | 0 | 0 | 11 | new, all 21–40 |
| smarters-live.com | FR | 1 | 0 | 0 | 0 | 4 | effectively invisible |
| iptvfranceofficiel.fr | FR | **0** | — | — | — | 0 | live but invisible |
| iptvpix.com | FR + BE | **0** | — | — | — | 0 | **best links, 0 rankings — investigate** |
| rodaktv.com | PL | **0** | — | — | — | 0 | 5 days old, expected |
| iptvshqiptar.com | AL | **0** | — | — | — | 0 | invisible + content-thin |

**iptvesp fast wins** — 4 keywords stuck at pos 4–6, all LOW competition, all in its proven Telegram niche:

| Keyword | Vol/mo | Position | Page |
|---|---|---|---|
| iptv futbol telegram | 210 | **4** | /blog/iptv-espana-telegram |
| grupo telegram iptv | 140 | **4** | /blog/telegram-listas-iptv-espana |
| listas m3u telegram | 260 | 6 | /blog/telegram-listas-iptv-espana |
| iptv telegram 2025 españa | 110 | 6 | /blog/telegram-listas-iptv-espana |

A handful of authority links + light on-page pushes these to top-3 — the fastest traffic gain available.

---

## What's missing → prioritized actions

1. **Authority (portfolio-wide, #1).** Send the 10 editorial guest drafts already written. Nothing else moves the needle as much. Owner-gated (accounts/sending).
2. **iptvpix paradox.** Best link profile in the portfolio, yet 0 visible rankings in FR *and* BE. Diagnose: are the money pages indexed in BE/CH? brand-only rankings? a canonical/market mismatch? Highest-ROI single diagnostic — I can run it.
3. **iptvesp top-3 push.** 4 Telegram terms at pos 4–6. A few links + minor on-page = top-3. Fastest win.
4. **Six FR sites, one market, ~0 authority = mutual invisibility.** The structural gap. Each FR site needs a *distinct* low-comp niche (the iptvesp Telegram playbook) instead of all chasing the same head terms — or consolidate the weakest. Decision needed from you on direction.
5. **Zero-ranking live sites (iptvfranceofficiel, iptvshqiptar).** Live but invisible; shqip is also content-thin (16 URLs). Need links + niche content; shqip needs depth.
6. **New sites (rodaktv, iptvsegura).** On track; just need time + the link program.
7. **Minor.** Google is serving a stale pre-de-brand snippet for iptvesp /blog/iptv-espana-telegram (live page is clean). Will refresh; a re-index request would speed it.

---

*Data: DataForSEO backlinks + Labs, live crawl. Rankings are DFS Labs estimates in each site's primary market; BE/CH coverage is thinner, which may understate iptvpix. Pulled 2026-09-09.*
