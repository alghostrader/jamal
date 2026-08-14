# HANDOFF — how to update iptv.alghostrader.com (for any Claude assistant)

Written 12 Aug 2026 by the cloud session that built this system. Everything needed to
run a full audit and deploy is in THIS repo. Read `CLAUDE.md` first — it carries the
standing rules ("update the dashboard" = full audit, verified facts only, one keyword →
one page → one site, frozen pages stay frozen).

## 1. Source

- **Repo:** `https://github.com/alghostrader/jamal`
- **Branch `claude/iptvpix-seo-audit-l68bmx`** — the working branch: toolchain
  (`seo-tools/`), data state, docs, CLAUDE.md. Work here.
- **Branch `dashboard`** — deploy target: 14 flat HTML files + `vercel.json`. Never
  develop here; only copy generated HTML in and push.
- **No framework.** The dashboard is plain static HTML produced by a Python generator
  (`seo-tools/daily/generate_v3.py`). No Node, no npm, no build system.

## 2. Run locally

```bash
python3 --version          # 3.11+
pip install requests beautifulsoup4 lxml google-auth
```
That is the entire setup. To preview: generate (see §5) and `open seo-tools/daily/out/index.html`.

## 3. Deploy

- Vercel project (name: the repo's project in the owner's Vercel account) is
  **git-connected to the `dashboard` branch**. A `git push origin dashboard` IS the deploy.
- Procedure: generate → `git checkout dashboard` → copy `seo-tools/daily/out/*.html` to
  repo root → inject a marker comment `<!-- pipeline:<name>-<HHMM> -->` into
  `index.html`'s `<title>` line → commit → push → **verify the marker is live** at
  https://iptv.alghostrader.com/ — then **check it again ~60s later** (Vercel once
  served a stale queued build after rapid pushes; a re-push fixes it).

## 4. Data sources (all JSON, all in `seo-tools/`)

Displayed numbers are **computed at generate time** from these files — nothing is
hand-edited into HTML, and there is no database:

| File | Shape | Feeds |
|---|---|---|
| `daily/_sites.py` | `SITES = [(slug, domain, canonical_host), ...]` ×9 | the 9-site list everywhere |
| `dash/dash_data.json` | per site: `daily[{date,clicks,impressions}]`, `in_gsc`, `dfs{backlinks,ref_domains,domain_rank,spam_score,ranked_top100}` | traffic, authority; header sums (e.g. "keywords top-100" = Σ ranked_top100; "referring domains" = Σ ref_domains) |
| `daily/keyword_targets.json` | `{domain:[{kw,vol,pos,url?,page?}]}` — `pos`=live SERP position, `page`=money-page ownership hint | Rankings board, per-site keyword tables, prompts |
| `daily/audit_findings.json` | per site: `titles_over60, redirect_links, linked404, orphans, canonical_mismatch, www_redirect/apex, favicon, thin` | **"Urgent — fix now"** + Fix Prompts (both computed from this) |
| `daily/content.json` | per site: `articles[{path,title,words}]`, `recommend[{kw,vol,covered,sibling?,page?}]` | article prompts, gap detection, opportunity cards |
| `daily/content_keywords.json` | `{market:[{kw,vol}]}` | shared keyword pools (fr/es/nl/sq) |
| `daily/semrush.json` | per site: AS, traffic, keywords, ref_domains, backlinks, ai_* — **owner-pasted, never fetched** | SEMRUSH panels, AI-search card |
| `daily/checkbox_state.json` | `{checked:[checkbox-ids]}` | pre-checked boxes on Backlinks (matrices + milestones) |
| `daily/history.json` | daily snapshots `{date, sites{...}}` | Trends sparklines, change deltas |
| `daily/goals.json` | `{set_on, goals:[{id,label,target,due}]}` — ids: `clicks`, `top10`, `prime_rd`, `earning` | **North Star card** on home (currents computed live; edit targets only when the owner asks) |
| `daily/prev_snapshot.json` | the diff BASELINE — read by generate, never written by it | **"What changed this update"** diff on home. Generate writes `cur_snapshot.json`; AFTER the deploy is verified live, promote it (`cp cur_snapshot.json prev_snapshot.json`) and commit. Never promote before a verified deploy — re-runs within one audit must not destroy the diff. |
| `briefs/<slug>/site-brief.md` | 9 site briefs (voice, lane, money pages, market) | read by the installed 5-skill SEO system (keyword-fanout-map → seo-content-writer → onpage-optimizer → internal-link-architect → ai-visibility-checker); each site's dashboard page shows its pipeline workflow card. ⚠️ fields await owner confirmation. Regenerate with `daily/build_briefs.py` only if the config changes — owner edits win over regeneration. |

**"Do this today"** is not data at all — `daily_plan()` in `generate_v3.py` computes the
queue from findings/content state; steps auto-clear when the next crawl verifies work done.
Trends/Backlinks/Plan pages: all generated from the same files.

## 5. Update procedure (the exact full-audit sequence)

```bash
cd seo-tools/daily
# 1. crawl all 9 (parallel)
for row in "esp iptvesp.com" "prime primeiptv-france.com" "ned iptvned.com" \
  "pix iptvpix.com" "slive www.smarters-live.com" "shqip iptvshqiptar.com" \
  "spf www.smartersprofrance.fr" "ifo iptvfranceofficiel.fr" \
  "aio abonnementiptvofficiel.com"; do python3 crawler.py $row & done; wait
# 2. credentials + data pulls
set -a && . ../dash/.env && set +a
python3 ../dash/fetch_dash_data.py        # GSC traffic + DataForSEO authority
python3 refresh_kt_positions.py           # live SERP position for every target
# RULE: any watched ranking that CHANGED must be re-probed twice before recording.
# 3. analysis
python3 build_findings.py
python3 build_content_kw.py && python3 build_content.py
python3 history.py
# 4. generate
DASH_STAMP="$(date -u '+%Y-%m-%d %H:%M UTC')" python3 generate_v3.py
# 5. deploy (see §3), then COMMIT THE UPDATED JSON STATE back to the working branch
```

A recent deploy commit to `dashboard` looks like: 14 files changed, all `*.html` —
e.g. `4337863 "GSC access restored — traffic live again; esp at all-time-high 333 clicks/7d"`.
When the owner pastes a data record instead (Semrush snapshot, "DASHBOARD PROGRESS v1"
checkbox code): merge it into `semrush.json` / `checkbox_state.json`, then run only
steps 4–5.

## 6. Config / secrets (NOT in the repo — recreate locally)

- `seo-tools/dash/.env` → `DFS_LOGIN` + `DFS_PASSWORD` (DataForSEO; owner has these —
  same credentials used since July). `chmod 600`.
- `seo-tools/gsc/sa.json` → Google service-account key
  `seo-monitor@seo-dashboard-505310.iam.gserviceaccount.com`, added as **Restricted**
  user on all 9 GSC properties. The owner downloaded this JSON on 12 Aug 2026
  (file like `seo-dashboard-505310-*.json` in Downloads). `chmod 600`.
- Semrush: no API — owner pastes Domain Overview values into chat; they go in `semrush.json`.
- Vercel: no token needed — deploys ride on git push to `dashboard`.
- Never commit either secret. `seo-tools/.gitignore` already excludes them.

## 7. Coordination between assistants (IMPORTANT)

Multiple assistants may run audits. To avoid divergent state:
1. **`git pull` the working branch before every audit** — the JSON state files are the
   shared memory (positions, history, checkbox ticks).
2. **Commit the updated JSONs back after every audit** (step 5 above).
3. Deploys: always `git pull origin dashboard` before pushing to it.
4. Chat-side rules still bind: model IDs never appear in commits; git author = owner
   identity; report what changed / what was verified / any alarm after each audit.
