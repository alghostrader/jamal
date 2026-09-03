# Handoff: IPTV Portfolio Dashboard redesign

## Overview
A redesign of the internal SEO + sales dashboard at iptv.alghostrader.com (10 IPTV sites across ES / FR / NL / SQ markets). One owner-user, desktop, light theme. Goal: one place to track alerts, rankings, backlink progress, traffic, sales and clients — every page reachable from a single top bar.

## About the design files
`IPTV Dashboard.dc.html` is a **design reference built in HTML** — a clickable prototype showing intended look and behaviour. It is NOT production code. Recreate it inside the existing repo `alghostrader/jamal` (branch `claude/iptvpix-seo-audit-l68bmx`), where the dashboard is generated as static HTML by `seo-tools/daily/generate_v3.py` and deployed to the `dashboard` branch on Vercel. Keep that pipeline: replace the HTML templates/`_styles.html` the generator emits so the output matches this design. No framework is required; if one is desired, keep static output (Vercel).

## Fidelity
**High-fidelity.** Colors, type, spacing, radii and copy are final. Match them.

## Data sources (already in the repo)
| Screen | Fed by |
| --- | --- |
| Overview | `goals.json` (north star), `dash_data.json` (clicks, sparklines), `keyword_targets.json` (rankings), `prev_snapshot.json` vs `cur_snapshot.json` (what changed), `audit_findings.json` + spam deltas (alerts) |
| Work | `daily_plan()` in `generate_v3.py` — group tasks by role: Developer / Content / Links / Owner |
| Trends | `history.json`, `dash_data.json`, `semrush.json` (ai_* fields) |
| Backlinks | `checkbox_state.json`, `semrush.json`, `dash_data.json.dfs` |
| Plan | `_sites.py`, `briefs/*/site-brief.md` |
| Site detail | `content.json`, `keyword_targets.json`, `audit_findings.json`, `semrush.json` |
| Sales / Clients / Replies | the existing browser-local sales app (`/sales`, `/replies`, `/support`) — same data model (client, site, plan, screens, price, payment, app, panel, status, MAC/device key, notes). Add `clicks30` per site (from GSC) to compute revenue-vs-clicks. |
| Settings | `_sites.py`, `goals.json`, credentials status (GSC service account, DataForSEO, Semrush manual paste, Vercel) |

Sales/Client rows in the prototype are **sample data**; the live app currently holds €0.

## Global shell
- Page background `#f5ead8`. Max content width 1400px, horizontal padding 32px, `main` padding 28px 32px 60px.
- **Top bar** (sticky, `rgba(245,234,216,.92)` + `backdrop-filter: blur(8px)`, bottom border `rgba(32,30,29,.1)`):
  - Row 1 (padding 12px 32px, gap 20px): brand mark (34px terracotta circle `#c67139`, Caprasimo "i" in `#f5ead8`) + wordmark "IPTV **Portfolio**" (Caprasimo 19px, "Portfolio" in `#c67139`); nav pill group (background `#ebddc5`, radius 999, padding 4px; items: Overview, Work, Trends, Backlinks, Plan, Sales, Clients, Replies, Settings — Figtree 13px/600, padding 7px 14px, radius 999; active = `#c67139` bg / `#f5ead8` text, inactive = transparent / `#645c50`; group scrolls horizontally with hidden scrollbar if narrow); spacer; audit status (8px sage dot `#7a8a5e` + "Audit 2 Sep · 05:27 UTC", 12px `#82796a`, nowrap); **Run audit** primary button (Caprasimo 14px, `#c67139` bg, `#f5ead8` text, padding 9px 18px, radius 999, hover `#b2622d`).
  - Row 2 (padding 0 32px 10px, gap 6px, horizontal scroll, hidden scrollbar): label "SITES" (11px/600 uppercase, letter-spacing .08em, `#82796a`) then one chip per site: 7px colour dot + slug, 12px, padding 3px 10px, border 1px `rgba(32,30,29,.14)`, radius 999; active chip: border `#c67139`, bg `#ffe1d0`, text `#8c491a` 700.
- Site colours (used for dots everywhere): iptvesp `#c67139`, primeiptv-france `#7a8a5e`, abonnementiptvofficiel `#f6a06b`, iptvned `#8c491a`, smartersprofrance-fr `#aebf92`, iptvshqiptar `#645c50`, iptvsegura `#56633f`, iptvfranceofficiel-fr `#c0b6a5`, smarters-live `#402310`, iptvpix `#ffc6a5`.

## Shared components
- **Page title**: Caprasimo 40px/1.05, margin 0 0 8px; subtitle Figtree 15px `#82796a`.
- **Section title**: Caprasimo 20–22px, weight 400.
- **Card**: bg `#f9f4ed`, radius 16px, padding 16–18px 20px, shadow `0 1px 2px rgba(46,43,37,.14)`. Table-cards use padding 0 and `overflow:hidden` (or `overflow-x:auto` for wide tables).
- **Alert card / warning tint**: bg `#ffe1d0`, text `#402310`, kicker `#8c491a`, numbers `#8c491a`.
- **Positive tint**: bg `#e1eecc`, text `#3d472b` / `#56633f`.
- **Inset tile** (inside cards): bg `#ebddc5`, radius 12px, padding 12px 14px.
- **Kicker**: 10px/700 uppercase, letter-spacing .1em, `#c67139` (or `#82796a` neutral, `#8c491a` on warning, `#56633f` on positive).
- **Big number**: Caprasimo 32–36px (KPI cards), 26–28px (small tiles), line-height 1.1.
- **Progress bar**: track `#ebddc5` 8px radius 999; fill `#c67139` (in progress) or `#7a8a5e` (complete).
- **Tag / phase pill**: inline-block, radius 999, padding 2px 9px, 10px/700 uppercase letter-spacing .06em. GROW/FLAGSHIP → `#e1eecc`/`#3d472b`; WATCH/RECOVERING → `#ffe1d0`/`#8c491a`; others (REBUILD, BUILD, BASELINE, SATELLITE, ONBOARD) → `#eee7db`/`#645c50`. Task kinds: FIX warning, WRITE positive, others neutral. Status: Activated/Active positive; Expiring/Expired/Lapsed warning; Paid/Renewed neutral.
- **Delta text**: ▲ n in `#56633f` 600, ▼ n in `#8c491a` 600, "—" in `#a19786`.
- **Spam score**: ≥58 warning pill; 50–57 `#8c491a` 600 text; <50 `#645c50`; null "—" `#a19786`.
- **Buttons**: primary (above); secondary = transparent, border 1px `rgba(32,30,29,.16)`, radius 999, 13px/600 `#201e1d`, hover bg `rgba(32,30,29,.07)`; sage soft = bg `#e1eecc`, text `#3d472b`, hover `#ccdbb2`; link-button = `#8c491a` 12px/600 no bg.
- **Segmented pill toggle**: group bg `#ebddc5` radius 999 padding 3px; active option `#c67139`/`#f5ead8`, inactive `#645c50`; 12px/600, padding 4px 12px.
- **Table**: `th` 11px/600 uppercase letter-spacing .06em `#82796a`, padding 8px 12px, bottom border `rgba(32,30,29,.16)`; `td` padding 10px 12px, bottom border `rgba(32,30,29,.08)`, tabular numerals; row hover `rgba(32,30,29,.04)`; last row no border.
- **Sparkline**: SVG 72×22, polyline stroke `#c67139` 1.75 (or `#7a8a5e` 2 on Trends tiles), 12 points scaled to max.
- **Check circle** (matrix / milestones): 24px (20px milestones) circle, border 1.5px `rgba(32,30,29,.2)`; checked = bg + border `#7a8a5e`, `✓` in `#f5ead8` 12px/700.
- Focus ring: `outline: 2px solid #c67139; outline-offset: 2px`.

## Screens

### 1. Overview (`/`)
Column gap 24px.
1. Header row: title "Good morning. One thing needs you." (dynamic — count of alerts) + subtitle "10 sites · 58 keywords probed · 755 clicks this week"; right: pills "1 fix" (warning) and "8 tasks open" (positive).
2. **Alert banner** (warning card, flex, gap 16, padding 16px 20px): 40px terracotta circle with "!" (Caprasimo 18px), kicker "NEEDS ATTENTION · SPAM WATCH", 15px message; buttons "Open site" (secondary → that site page) and "Pause links" (primary). Render one banner per open alert; hide when none.
3. **North star** — h2 "North star — 4 goals" + "set 14 Aug · 1 complete". 4-col grid gap 14: each card kicker (goal label), current (Caprasimo 32) + "/ target" (`#82796a` 14px), progress bar, footer row 12px `#82796a`: percentage (or "goal complete") | "due 31 Oct" (or "done ✓"). Data from `goals.json`.
4. Two-column grid `1.6fr 1fr` gap 20:
   - **Sites — 7 days** table card with Clicks | Revenue segmented toggle. Columns: Site (dot + slug, clickable → site page), Phase pill, Clicks (right, 600), Δ wk, 30d sparkline, Best rank (12px `#645c50`, ellipsis, max 170px), Ref.dom, Spam, Rev € (`#56633f` 600). 10 rows sorted by clicks desc.
   - Right stack (gap 20): **Rankings movement** card — header "11 / 58 in top 100"; stacked distribution bar (segments flex 3/5/3/47 colours `#7a8a5e`, `#aebf92`, `#f6a06b`, `#ebddc5`, 6px, gap 6); legend row 11px; list rows (padding 7px 0, border-bottom `rgba(32,30,29,.07)`): 8px site dot, keyword 13px, move (▲/▼ n), position Caprasimo 16px "#n". **Backlink engine** card — 3 mini stats (Ref. domains 522, Checklist 12%, Spam max 62 in `#8c491a`), sage progress bar, "45 of 371 placements done · next: Facebook Page × 10 sites", "Open →" link to Backlinks.
5. Two-column grid `1fr 1fr`: **Work — by role** (4 inset tiles: role name 11px `#645c50` + count Caprasimo 28px; "All 8 tasks →" link) and **What changed** (rows: site 600 min-width 150, description `#645c50`, delta coloured; header "since 1 Sep · 11 changes").

### 2. Work (`/today`)
Title "Work — 8 tasks", subtitle "Organised by role. Tasks auto-clear when the next audit verifies them done." Right: Open | Done this week toggle. 4-column kanban grid gap 16: column header (Caprasimo 18px role + count pill `#ebddc5`), task cards (card, padding 14px 16px, gap 8): kind tag + site (11px `#82796a`), task text 14px/1.4, buttons "Copy prompt" (secondary, small: padding 5px 12px 12px) and "Mark done" (sage soft). Roles: Developer, Content, Links, Owner.

### 3. Trends (`/trends`)
Title "Trends — are we winning?". Grid `2fr 1fr`:
- Clicks chart card (padding 20px 24px): kicker "CLICKS PER DAY · 90 DAYS", 3,374 (Caprasimo 40) + "▼ 30 vs last week"; Impressions | Clicks toggle; SVG 800×180 (3 gridlines `rgba(32,30,29,.08)` at 45/90/135; area fill `rgba(198,113,57,.15)`; line `#c67139` 2.5); x-axis labels 11px `#82796a` every ~15 days.
- **Weekly scorecard** table: Week (`#645c50`), Clicks (600), Δ (coloured), Impr. (`#82796a`). 10 ISO weeks.
Second grid `1fr 1fr`: **AI search — 24 pages cited** (intro 13px `#645c50`; table Site / Visibility / Cited pages) and **Per site — 90-day trajectory**: 2-col grid of clickable tiles (card padding 12px 14px, hover bg `#fff`): dot, slug 13px/600, "{c90} clicks · 90d · {PHASE}" 11px, sage sparkline 56×20.

### 4. Backlinks (`/links`)
Title "Backlinks — step by step"; right "Copy progress code" (secondary). 3 KPI cards: Referring domains 522; Checklist progress (percentage + sage bar + "N of 371 boxes done", live from ticks); Spam watch (warning card) 62 "highest: smarters-live · +4 pts on any site = pause it".
- **Authority — two indexes** table: Site (dot + domain), DFS rank, DFS ref.dom, Δ (sage 600), Semrush AS, SR ref.dom (600), Top-100 kw, Spam.
- **Step 1 — Profile foundation** table card: header + "Copy batch prompt" primary. Columns: Platform (13px, note 11px `#82796a`, e.g. "⏳ drip 1-2/day"), one centred column per site (short codes esp/prime/aio/ned/spf/shqip/segura/ifo/slive/pix, th padding 8px 4px), Done "n/10". Cells are check circles; clicking toggles (persist to `checkbox_state.json` via the existing "copy progress" flow). Footer line: "Step 2 — Max-backlinks matrix (206 placements) · Step 2b — Tool launches (8 directories × 4 tools) · Expand all steps ↓" — Steps 2/2b use the same matrix component, collapsed by default.
- Grid `1fr 1fr`: **Step 3 — Weekly cycle** (numbered 26px circles `#ebddc5` Caprasimo 13px, text 13px, "Prompt" link per row) and **Milestones — tick when true** (check circle 20px + text; done = `#82796a` strikethrough).

### 5. Plan (`/plan`)
Title "Plan — where we are going". 4 KPI cards: Active sites 10 ("4 markets + Poland planned"), Pages live 523, Articles 449, Page-1 rankings 3. **Where each site stands** table: Site (dot + domain), Phase pill, This cycle's job (13px `#645c50`), Status "{kw} kw · {dfsRd} ref.dom" (12px `#82796a` right). Grid `1fr 1fr`: **Standing strategy** (6 items, bold lead + `#645c50` body, 13px, gap 10) and **Content OS — 5-skill pipeline** (rows: sage numbered circle 0–5, skill name in `code` pill `#ebddc5` 12px radius 999, output text 13px `#645c50`).

### 6. Sales (`/sales`)
Title "Sales — clicks to money"; right: "Export" secondary, "+ Add sale" primary (opens existing New-sale dialog — same fields as today). 5 KPI cards: Revenue · month (€ + "n sales"), This week (+ "▲ n sales" sage), € per 100 clicks (portfolio 7d), Your profit (sage number, "since last payout · €x for panels"), Expiring ≤ 7 days (warning card, "Renew now →" → Clients).
Grid `1.6fr 1fr`: **Revenue vs clicks — by site** table (Site, Clicks 30d, Sales, Revenue 600, Conv. %, €/100 clicks, Share bar sage 8px width = share of revenue). Right stack: **Panel stock** (4 inset tiles Dino/Mega/Max/IBO: credits Caprasimo 24 + burn rule 10px; "+ Add credits" link) and **Payout** (two-segment bar `#c0b6a5` for panels / `#7a8a5e` yours, 14px, radius 999; totals row 12px; "Add payout" link).
**Recent sales** table with filter chips (All sites ▾ / All panels ▾ / All statuses ▾, outlined pill 12px): Date, Client 600, Site, Plan, Price 600, App, Panel, Ends, Status tag.

### 7. Site detail (`/<slug>`)
"← All sites" link (12px `#8c491a`), header: 22px site dot + domain (Caprasimo 40) + phase pill; subtitle "{market} · {this cycle's job}". Right: "Visit site ↗" secondary (nowrap) + "Copy article workflow" primary.
5 KPI cards: Clicks · 7 days (+ delta "vs last week"), Clicks · 90 days (+ impressions), Best live ranking (#n + keyword ellipsis), Authority ("129 ref.dom", "AS 7 · spam 56"), Health · today (positive card, "7 / 7", "verified clean"; turns warning when any check fails).
Health chips row (wrap, gap 8): pill `#f9f4ed` with 14px sage ✓ circle — Titles ≤60, No redirect-links, No orphans, Canonicals, No broken links, www 308, Favicon.
Grid `1.4fr 1fr`: **Keyword targets** table (Target keyword 600, Vol/mo, Rank pill: ≤10 positive, ≤30 neutral, else warning, "not in top 100" `#a19786` 12px; Move). Right: **Biggest opportunity** warning card (volume Caprasimo 30 + "searches / mo", "“kw” — uncovered here and unclaimed in this market.", "Write it — run pipeline" primary) and **Ongoing priorities** (KPI / DO tags + lines).
Grid `1fr 1fr`: **Articles — n published** ("n thin (<600 words)" right, `#8c491a`) table path (monospace 12px) / words; **Next article — keyword gaps** table keyword / vol / status ("GAP — write it" warning tag, "has article" 12px `#82796a`).

### 8. Clients (`/clients`) — new page
Title "Clients & renewals"; toggle Due ≤ 14d | Active | Lapsed | All. 4 KPI: Expiring ≤ 7 days (warning), Expiring 8–14 days, Lapsed · 30 days, Active clients (+ "renewal rate 68%"). Table: Client (name 600 + masked WhatsApp 11px), Language, Site, Plan · screens, Panel, Ends (Expiring `#8c491a` 600 / Lapsed `#a19786` / else `#645c50`), Lifetime € 600, Status tag, actions "Message" (secondary small) + "↻ Renew" (sage soft small).

### 9. Replies & support (`/replies`, `/support`) — merged
Title "Replies & support tools". Grid `1.4fr 1fr`: **Reply templates** card with language toggle ES/FR/NL/EN/SQ; 2-col grid of inset tiles (title 13px/600 + "Copy" link; body 12px `#645c50`). Six templates per language: welcome + credentials, renewal reminder, buffering, device change, payment methods, closing (copy in prototype). Right: **Support tools** (rows: 32px sage circle glyph, name 13px/600, description 11px, "Open ↗") — Device compatibility checker, Downloader codes, Xtream ⇄ M3U converter, Bandwidth calculator; **Activation checklist** (5 numbered lines 13px `#645c50`).

### 10. Settings (`/settings`) — new page
Title "Settings & integrations". Grid `1fr 1fr`: **Integrations** list (status dot sage/neutral/terracotta, name 13px/600, description 11px, status tag: Connected positive / Manual paste neutral / Sign in warning) — Google Search Console, DataForSEO, Semrush, Vercel, Sales sync. **North-star goals** editor: rows label | target input | due input (pill inputs: bg `#ebddc5`, border `rgba(32,30,29,.16)`, radius 999, 13px, min-height 34px); "+ Add goal". **Sites** table (+ "Add site" primary): Slug, Domain, Market, Lane, Phase, GSC "✓ verified" sage, Canonical host (monospace). **Audit schedule & rules**: 3 inset tiles — Daily audit 05:30 UTC sequence, Re-probe rule, Spam pause rule.

## Interactions & state
- `page` (overview | work | trends | links | plan | sales | site | clients | support | settings) — top-bar nav; as static HTML, one file per page with identical shell.
- `site` — selected slug for site detail; site chips highlight the active one.
- `checked` — set of `"<platform>|<slug>"` keys for Step 1/2/2b matrices and milestones; toggled on click, persisted through the existing "Copy progress code" flow → `checkbox_state.json`.
- `lang` — reply-template language toggle.
- Hover: buttons per component spec; table rows `rgba(32,30,29,.04)`; trajectory tiles bg `#fff`. No animations beyond default transitions (150ms ease on background is fine).
- Alerts: computed from spam deltas ≥ +4, failed health checks, frozen-page probes — one banner each, sorted FIX first.

## Design tokens (Organic design system)
- Background `#f5ead8`; surface `#ebddc5`; card `#f9f4ed`; text `#201e1d`.
- Neutral ramp: 100 `#f9f4ed`, 200 `#eee7db`, 300 `#dcd3c4`, 400 `#c0b6a5`, 500 `#a19786`, 600 `#82796a`, 700 `#645c50`, 800 `#474238`, 900 `#2e2b25`.
- Accent (terracotta) ramp: 100 `#fff2eb`, 200 `#ffe1d0`, 300 `#ffc6a5`, 400 `#f6a06b`, 500 `#d67f48`, base `#c67139`, 600 `#b2622d`, 700 `#8c491a`, 800 `#643312`, 900 `#402310`.
- Accent-2 (sage) ramp: 100 `#f0fae1`, 200 `#e1eecc`, 300 `#ccdbb2`, 400 `#aebf92`, 500 `#8fa073`, base `#7a8a5e`, 600 `#728157`, 700 `#56633f`, 800 `#3d472b`, 900 `#272e1b`.
- Divider `rgba(32,30,29,.16)`; row rule `rgba(32,30,29,.08)`.
- Type: headings Caprasimo 400 (Google Fonts); body Figtree 400/500/600/700. Sizes: 40 / 22 / 20 / 15 / 14 / 13 / 12 / 11 / 10. Numbers tabular.
- Radii: 12px tiles, 16px cards, 999px pills/buttons/inputs.
- Shadow sm `0 1px 2px rgba(46,43,37,.14)`.
- Icons: Lucide, stroke 2.75 (prototype uses glyph placeholders).

## Assets
None — Google Fonts (Caprasimo, Figtree) only. Site colour dots are CSS.

## Files
- `IPTV Dashboard.dc.html` — the full clickable prototype (all 10 pages, switch via top bar and site chips). Data arrays live in the logic class at the bottom of the file and mirror the repo's JSON shapes.
