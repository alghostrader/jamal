# Free-Tools Roadmap — Portfolio Link Magnets (Aug 2026)

**Principle:** tools are the un-rate-limitable link channel — forums/blogs link utilities forever.
**Rules (non-negotiable):**
1. **One tool = one site.** Never duplicate a tool across sites (duplicate/thin footprint). Localized *variants* only if the original proves itself (different language + market + angle).
2. **100% client-side.** Converters/generators never send or store user playlists/credentials — all in-browser, with a visible privacy note ("nothing leaves your device").
3. **Legit-only content.** Downloader-code lists include ONLY legitimate apps (IPTV Smarters, TiviMate, VLC, Kodi, Plex, official store apps). No piracy-app codes, ever — that's the suppression trigger in this niche.
4. One tool per build cycle, through the daily queue. Each ships → Product Hunt (free) + listicle outreach + Links-matrix promotion.

---

## Build order

| # | Tool | Site | Why there | Target queries | Status |
|---|---|---|---|---|---|
| 1 | **Device/app compatibility checker** (`/application-iptv`) | smarters-live | The app hub; feeds the 49,500/mo Smarters Pro play | application iptv (6,600), device long-tail | 🔨 prompt issued |
| 2 | **Downloader codes list (legit apps) + Downloader tutorial** | smarters-live | Extends the app hub; huge Firestick intent | "downloader codes", "code downloader firestick" FR/EN long-tail | next |
| 3 | **Xtream ⇄ M3U URL generator** (client-side) | iptvesp | The "listas iptv" market (1,900/mo cluster); Spanish playlist intent | "convertir xtream a m3u", "generar lista m3u", "xtream codes a m3u" | queued |
| 4 | **IPTV bandwidth calculator** ("Quel débit pour l'IPTV ?" — channels/quality → Mbps) | primeiptv | Upgrades its existing /guides/iptv-4k-debit-internet into an interactive asset | "debit iptv", "vitesse internet iptv", 4k requirements | queued |
| 5 | **Legality checker** (`/iptv-legal`) | primeiptv | Spec ready; E-E-A-T + journalist-pitch credential | "iptv légal france/belgique/suisse…" | ⏸ waiting on owner legal facts (FR/BE/NL) |
| 6 | **NL buyer's checklist** (interactive "waar let je op bij iptv kopen") | iptvned | Buy-intent tool for "iptv kopen" (6,600) | iptv kopen, iptv aanbieders | later |
| 7 | FR M3U generator variant | iptvpix | Only if #3 performs; pix targets "iptv m3u" (590) | iptv m3u france | later (post-recovery) |

**Technical notes**
- #2: "conversion" is really URL generation — Xtream creds (server/user/pass) → `get.php` m3u URL, and m3u URL → parsed creds. Pure client-side string work; trivial build, heavily searched, endlessly forum-linked.
- #3/#4: static pages + a small client component; keep Lighthouse ≥90, schema (HowTo/FAQ), self-canonical, in sitemap.
- Tutorials ("how to sideload apps with Downloader", per-device) are content that wraps tools #1–2 — they go through the normal article queue, on smarters-live.
- Cross-promotion: each sibling site links a relevant tool **once, contextually** (no sitewide tool links — footprint).

**Cadence:** one tool per cycle through /today. After each ships: crawl verification → Product Hunt → 5 listicle/broken-link emails aimed at it (Friday outreach slot).
