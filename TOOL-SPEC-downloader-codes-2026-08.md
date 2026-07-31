# Build Spec — Downloader Codes (legit apps) + Downloader Tutorial

**Site:** smarters-live.com (extends the /application-iptv hub) · **Type:** Tier-2 link magnet #2
**Safety rule (absolute):** ONLY legitimate apps. Every code must be verified against an official
source (developer site / AFTVnews registry). Unverifiable → no code; link the official APK/store
URL instead. No piracy apps, ever.

## Pages
1. `/codes-downloader` — "Codes Downloader 2026 : les applications IPTV légales sur Firestick".
   Table: app · code (or — ) · source officielle · appareil · note. Seed: IPTV Smarters Pro,
   TiviMate, VLC, Kodi, Plex, Downloader lui-même. Copy-to-clipboard per code. ItemList schema.
2. `/utiliser-downloader-firestick` — HowTo tutorial: activer les sources inconnues → installer
   Downloader → entrer un code → installer l'app. HowTo schema, screenshots optional.

## Wiring
Both SSG, self-canonical, titles ≤60, meta ≤160, in sitemap; linked once from /application-iptv
hub + each device page's "Comment l'installer" section where relevant. CTA funnel unchanged.

## Copy-paste prompt
```
>>> TARGET WEBSITE: smarters-live.com <<<
Switch to the smarters-live.com project. Do NOT touch any other site.

Extend the /application-iptv hub with two pages (French, SSG, App Router):
1. /codes-downloader — "Codes Downloader 2026" : a table of LEGITIMATE apps only (IPTV Smarters
   Pro, TiviMate, VLC, Kodi, Plex, Downloader). For each: the Downloader code ONLY if you can
   verify it from an official source (developer site or AFTVnews); otherwise put "—" and link
   the official APK/store URL. Never invent a code; never include piracy apps. Columns: app,
   code (copy-to-clipboard button), source officielle, appareils, note. ItemList JSON-LD, FAQ
   (3 items) on code usage. data/downloader-codes.json drives it, each entry {app, code|null,
   official_url, devices[], verified_date}.
2. /utiliser-downloader-firestick — HowTo tutorial (activer sources inconnues → installer
   Downloader depuis l'Appstore → entrer le code → installer/ouvrir l'app), HowTo JSON-LD,
   1,000+ words, keyword-first title ≤60.
SEO/design: self-canonical, unique meta ≤160, both in sitemap.xml, reuse existing components,
Lighthouse ≥90, CLS ~0. Internal links: one link to each new page from /application-iptv and
from device pages' install sections where relevant.
VERIFY: both routes 200 server-rendered; JSON-LD valid; every code in the table traceable to an
official source (list the sources in the PR/commit message); titles ≤60; sitemap updated.
One commit per page: feat(downloader): <page>.
```
