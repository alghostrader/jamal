# Search Console Performance Review — IPTV Portfolio

**Prepared for:** Site owner (7 GSC properties, service-account API access)
**Data window:** 10 April – 8 July 2026 (90 days), pulled 9 July 2026 via the Search Console API
**Properties analysed:** iptvpix.com, abonnementiptvofficiel.com, iptvfranceofficiel.fr, primeiptv-france.com, iptvned.com, iptvesp.com, smarters-live.com
**Method:** Search Analytics (daily totals, top queries/pages, query×page pairs, devices, countries) + URL Inspection API on 24 problem URLs diagnosed in the July 2026 technical audits

---

## 1. Executive Summary

The portfolio is at an early, fragile stage — **320 total clicks across all seven properties in 90 days** — and the Search Console data confirms the technical audits' central diagnoses with hard evidence: iptvpix.com has **collapsed to zero clicks** in the last 45 days and its three canonical-to-homepage pages are literally *"unknown to Google"*; the www hosts locked behind Vercel SSO are indexed with **`https://vercel.com/login` as their Google-selected canonical**; and iptvesp.com's missing pricing page threw away 245 impressions while returning 404. The one clear success is iptvesp.com — clicks **more than tripled half-over-half (43 → 148)** — but 84% of its traffic rides on a single blog post ranking ~#5 for "listas iptv españa telegram", making it a one-post site. Across every property, the commercial head terms ("abonnement iptv", "iptv nederland", "iptv españa") sit at positions 60–90 — a domain-authority problem that technical fixes alone won't solve, but which the week-one fixes (restoring de-indexed hubs, killing 404 funnels, consolidating cannibalizing clusters) are the prerequisite for.

---

## 2. Portfolio Scoreboard (90 days)

| Property | Clicks | Impressions | Click trend (45d → 45d) | Top-page share of clicks | Verdict |
|---|---|---|---|---|---|
| **iptvesp.com** | **191** | 2,141 | 43 → **148** 📈 | 84% (one post) | Growing fast, dangerously concentrated |
| primeiptv-france.com | 37 | 799 | 16 → 21 📈 | 16% (well spread) | Healthiest distribution, small base |
| iptvned.com | 35 | 1,429 | 23 → 12 📉 | 66% (one post) | News-post spike fading |
| **iptvpix.com** | 25 | 114 | 25 → **0** 🔴 | 92% | **Collapsed — effectively invisible** |
| iptvfranceofficiel.fr | 17 | 594 | 11 → 6 📉 | 35% | Sliding, money terms nowhere |
| abonnementiptvofficiel.com | 14 | 206 | 7 → 7 ➡️ | 50% | Flat, page-5 rankings |
| smarters-live.com | 1 | 13 | 1 → 0 | — | Effectively no presence |
| **Total** | **320** | **5,296** | | | |

Two portfolio-level gaps surfaced immediately:
- **smartersprofrance.fr is not in Search Console at all** — your technically best site (per the audit) is flying blind. Verify it (DNS TXT record) as a priority.
- **smarters-live.com is an eighth property** I hadn't audited — it exists in GSC but has essentially zero search presence (1 click / 13 impressions; its two pages rank for "smarter live" typo queries and a World Cup post at position 79).

---

## 3. URL Inspection — the audits' findings, confirmed by Google

I inspected 24 URLs flagged in the technical audits. Google's own index data:

| Audit finding | Google's verdict (URL Inspection API) |
|---|---|
| iptvpix.com `/blog`, `/iptv-acheter`, `/box-iptv` canonicalised to homepage | **"URL is unknown to Google" — never crawled, never indexed.** The canonical bug didn't just weaken these pages; combined with their absence of ranking signals, they don't exist for Google. |
| iptvned.com `/iptv-kopen` (same canonical bug) | **Unknown to Google.** |
| iptvned.com `/blog` (same bug) | Indexed — Google *overrode* the bad canonical and chose `/blog` itself. Proof the bug's outcome is coin-flip: one clone lost the page, the other survived on Google's judgement. Fix it everywhere. |
| iptvesp.com `/instalacion` (same bug) | Indexed under its own URL — Google overrode it here too. Still fix it. |
| iptvesp.com `/suscripciones` (missing pricing page) | **"Not found (404)", last crawled 7 July 2026** — Google knew this URL, kept it long enough to serve **245 impressions at position 34.8** in the window, and is still re-crawling the 404. A pricing page with demonstrated demand is being served as an error. |
| primeiptv-france.com `/blog` (orphan) | **"Crawled — currently not indexed"** — the textbook fate of a zero-inlink page. |
| primeiptv-france.com `/application/iptv-smarters-pro` (orphan) | **Unknown to Google** — despite being in the submitted sitemap. Sitemap-only discovery failed exactly as the audit predicted. |
| primeiptv-france.com `https://www.…/` (Vercel SSO wall) | "Page with redirect" — **Google's selected canonical for the www host is `https://vercel.com/login`.** |
| iptvfranceofficiel.fr `/abonnement-iptv` (the 404 target of 11 commercial CTAs) | **Unknown to Google** — every one of those 11 in-content links passes equity into a void. |
| All audited money pages (`/abonnements`, `/abonnementen`, `/tarifs`, `/iptv-premium`, `/iptv-france`, `/test-iptv`) and top earners | ✅ Submitted and indexed, correct canonicals, crawled within the last 2–4 weeks. |

---

## 4. Per-Site: What's Working / What Isn't

### iptvesp.com — the growth story, and its fragility
- **Working:** `/blog/iptv-espana-telegram` earns **161 of the site's 191 clicks**, ranking #4–5 across a family of Telegram-related queries ("listas iptv españa telegram" 329 imp, "iptv españa telegram", "iptv telegram" — combined ~600 impressions). Google shows it with sitelinks (the `#fragment` rows), a sign it's the recognised authority for the topic. `/blog/iptv-movistar-plus` (pos 11.8) and `/blog/iptv-lg-smart-tv-espana` (pos 8.7) are secondary winners.
- **Not working:** 84% single-post dependency — one algorithm update or a competitor targeting "iptv telegram" erases the site's traffic. The homepage ranks pos 18 for its own cluster; `/blog/mejor-iptv-espana` sits at pos 34 with 143 impressions (real demand, page 4). And the 404 `/suscripciones` (245 imp) means **the demand exists but lands on an error page**.
- **Do next:** build `/suscripciones` immediately (Google is still crawling it — a 200 with pricing content inherits the equity); add strong internal links from the Telegram post (the site's only authority page) to the money pages; push `mejor-iptv-espana` from pos 34 into the top 10 via the cluster consolidation from the audit.

### iptvpix.com — confirmed collapse
- **Not working (everything):** clicks went **25 → 0** and impressions 101 → 13 half-over-half. The only page that ever earned clicks, `/france-iptv-m3u` (23 clicks, pos 18.6 on M3U-list queries), hasn't been crawled since 18 May. The blog hub and two landing pages are *unknown to Google*. The homepage was last crawled 20 June and now gets ~0 impressions.
- **Reading:** this pattern — a working page going stale + hub pages self-canonicalised away + traffic to zero — is consistent with the site's crawl/indexing signals degrading until Google largely gave up. The audit's week-one fixes (self-referencing canonicals, fix the 66 broken links, restore the icon asset) are the prerequisites for recovery; after deploying, request re-indexing of `/blog`, `/iptv-acheter`, `/box-iptv`, `/pandora-iptv` and `/france-iptv-m3u` in GSC and watch coverage weekly.

### iptvned.com — a news post carrying the site
- **Working:** `/blog/iptv-opgerold-nederland` ("IPTV busted in the Netherlands" — a news-demand query) delivers 23 of 35 clicks at pos ~9, with sitelinks. Proof the domain *can* rank for fresh, specific topics.
- **Not working:** that spike is fading (clicks 23 → 12) as the news cycle cools; the homepage ranks **pos 73–88 for "iptv nederland"** (page 8); `/abonnementen` has 8 impressions total. The audit's legal-cluster cannibalization is visible in the wild: "iptv abonnement nederland legaal" splits across **three** posts at positions 72–85 — none rankable.
- **Do next:** the audit's P0s (fix the sitewide `/pandora-iptv` 404 nav link, canonical on `/iptv-kopen` — currently unknown to Google — and `/blog`), then consolidate the legal cluster into one page; use the opgerold post's authority for internal links while it still has momentum.

### primeiptv-france.com — small but structurally healthiest
- **Working:** the only French site growing (16 → 21 clicks); traffic is spread across 25 pages (installation guides, kids-channels guide, IPTV-vs-streaming, `/tarifs`, `/abonnement-12-mois`) — the guide/landing architecture works. Brand queries ("prime iptv" family) convert at pos 7–11.
- **Not working:** the orphans are confirmed dead weight (`/blog` crawled-not-indexed; `/application/*` never discovered); brand queries scatter across `/`, `/tarifs`, `/abonnement-12-mois` (mild, watch it); `mag box` (43 imp, pos 14) shows the MAG guide could reach page 1 with a few links.
- **Do next:** the audit's week-one items (SSO host, wire in the 10 orphans) — Google has already demonstrated it won't index them otherwise.

### iptvfranceofficiel.fr — sliding, funnel broken at the top
- **Working:** `/articles/iptv-smarters-pro` is the only asset with traction (6 clicks, 180 imp, pos 14.6). The app-guide angle ranks; "iptv smarters pro" clicked at pos 2 once.
- **Not working:** clicks fell 11 → 6. Money terms are nowhere: "abonnement iptv" pos 74, "abonnement iptv france" pos 64, "iptv premium" pos 67. The home/`/iptv-france` cannibalization from the audit shows up live: the query "iptv france" splits between `/iptv-france` (pos 83) and `/` (pos 78). And the 11-link CTA target `/abonnement-iptv` is confirmed unknown to Google.
- **Do next:** audit P0s (301 `/abonnement-iptv` → `/iptv-france`, differentiate home vs `/iptv-france`), then build links to `/articles/iptv-smarters-pro` — it's 4 spots from page 1 on a high-volume query family.

### abonnementiptvofficiel.com — flat at page 5
- **Working:** `/blog/iptv-canal-plus-sport` ranks pos 5–16 on a family of "canal+ sport iptv" queries (34 imp) — closest thing to a winner. `/test-iptv` collects half the clicks but at pos 47.9.
- **Not working:** dead flat (7 → 7 clicks); nothing on pages 1–2 except the Canal+ post; `/iptv-premium` at pos 38 with 24 impressions.
- **Do next:** audit quick wins (favicon, titles), then double down editorially on the sport/Canal+ angle where the domain demonstrably ranks, and interlink it to `/test-iptv` and `/iptv-premium`.

### smarters-live.com — decision needed
1 click in 90 days; ranks only for "smarter live" typos. It wasn't part of the audit engagement. Options: fold its content into smartersprofrance.fr (same topic, same market), or invest in it separately — but running two "Smarters" sites plus the unverified smartersprofrance.fr splits an already-thin brand presence three ways.

---

## 5. Cross-Portfolio Insights

1. **Everything ranks on pages 4–9 for money terms.** "abonnement iptv" (pos 64–76), "iptv nederland" (73–88), "mejor iptv" (34), "iptv premium" (67). This is not a technical ceiling — it's authority. After the week-one technical fixes, the constraint becomes links and brand signals; no amount of further on-page work moves pos 75 → pos 5.
2. **Every site's traffic is won by one specific, low-competition topic** — M3U lists (iptvpix), a police-raid news query (iptvned), Telegram lists (iptvesp), MAG-box setup (primeiptv), Canal+ sport (abonnementiptvofficiel), the Smarters app (iptvfranceofficiel). The playbook that works on this portfolio is *specific intent + thorough page*, not another "best IPTV {country}" variant — which is exactly what the cannibalization clusters keep producing.
3. **Google is inconsistent in rescuing the canonical bug** — it overrode the bad canonical on 2 of 5 affected pages and dropped the other 3 from existence. The shared-template fix protects all sites at once.
4. **Traffic is 64–93% mobile** across the portfolio — the mobile CWV findings in the audits are the ones that matter.
5. **Geography checks out** (FR sites → France + Maghreb, NL → Netherlands, ES → Spain), so targeting is fine; volume is the issue.

## 6. Priority Actions from this Data (order of expected impact)

1. **iptvesp.com:** ship `/suscripciones` (demand proven: 245 imp on a 404) + internal links from the Telegram post. Fastest revenue path in the portfolio.
2. **iptvpix.com:** deploy the audit's week-one fixes, then request indexing on the 5 key URLs; treat as a recovery project with weekly GSC coverage checks.
3. **Verify smartersprofrance.fr in GSC** (DNS TXT) — currently unmeasured.
4. **iptvfranceofficiel.fr:** 301 `/abonnement-iptv` → `/iptv-france` (11 links currently feeding a URL Google has never seen) and push `/articles/iptv-smarters-pro` toward page 1.
5. **iptvned.com:** consolidate the legal cluster (three pages splitting one query at pos 72–85 can become one page at a rankable position) before the opgerold momentum fades.
6. **primeiptv-france.com:** wire in the orphans — Google has explicitly confirmed it won't index them without links.
7. **Portfolio:** after technical fixes land, shift budget from producing more cluster variants to earning links/brand mentions for the 6 pages that are within striking distance of page 1 (listed per site above).

---

## Appendix — Method & Caveats

- Data via Google Search Console API (Search Analytics + URL Inspection), service account `anawclaude@map-api-279117…`, restricted read access, 90-day window ending 8 July 2026.
- Low absolute volumes mean percentage trends are directional, not statistical. Query rows under ~5 impressions are anecdotal.
- GSC anonymises rare queries; totals by dimension may not sum to property totals.
- CWV field data (CrUX) is not exposed via this API; the Core Web Vitals report in the GSC UI (Experience → Core Web Vitals) is worth a manual look — with current traffic levels most properties likely show "not enough data", which itself means lab metrics from the audits remain the best available signal.
- **Security note:** the service-account JSON key used for this pull should be rotated or deleted in Google Cloud Console (IAM & Admin → Service Accounts → Keys) once you're done with this analysis.
