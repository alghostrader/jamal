# SEO dashboard toolchain

Everything needed to run a full portfolio audit and rebuild **iptv.alghostrader.com**.
Committed to git on 12 Aug 2026 after the ephemeral workspace was recycled and the
original scripts were lost — **never keep this toolchain only in a scratch directory again.**

## Layout

```
seo-tools/
  daily/
    _sites.py               the 9 sites + canonical hosts (single source of truth)
    crawler.py              BFS technical crawler   → d_<slug>/crawl.json
    build_findings.py       crawl → audit_findings.json (technical defects)
    build_content_kw.py     DataForSEO volumes → content_keywords.json
    build_content.py        crawl + keywords → content.json (gaps, cannibalization guards)
    refresh_kt_positions.py live SERP positions → keyword_targets.json
    history.py              daily authority/ranking snapshot → history.json
    generate_v3.py          builds every dashboard page → out/*.html
    sitecards.py            per-site status cards
    recover_state.py        rebuilds JSON state from deployed HTML (disaster recovery)
    _styles.html            the design system (inlined into every page)
  dash/
    fetch_dash_data.py      GSC traffic + DataForSEO authority → dash_data.json
    .env.example            credential template
```

## Credentials (never committed)

- `dash/.env` — `DFS_LOGIN` / `DFS_PASSWORD` for DataForSEO.
- `gsc/sa.json` — Google service-account key with **read** access to all 9 Search Console
  properties. Without it the pipeline still runs; traffic metrics show as paused.

## Full audit (the standing rule: "update the dashboard" = all of this)

```bash
cd seo-tools/daily
python3 -c "from _sites import SITES; [print(s,c) for s,_,c in SITES]" | \
  while read slug host; do python3 crawler.py $slug $host & done; wait
set -a && . ../dash/.env && set +a
python3 ../dash/fetch_dash_data.py     # GSC (if key present) + DataForSEO
python3 refresh_kt_positions.py        # live SERP position for every target
python3 build_findings.py
python3 build_content_kw.py && python3 build_content.py
python3 history.py
DASH_STAMP="$(date -u '+%Y-%m-%d %H:%M UTC')" python3 generate_v3.py
```

Then deploy `out/*.html` to the `dashboard` branch (Vercel serves it), adding a
`<!-- pipeline:<marker> -->` comment to `index.html` and verifying the marker is live.

**After the deploy is verified live:** promote the change-diff baseline —
`cp daily/cur_snapshot.json daily/prev_snapshot.json` — and commit both. The
generator reads `prev_snapshot.json` for the home page's "What changed" card and
writes `cur_snapshot.json`; promoting only after a verified deploy means re-runs
within one audit never destroy the diff.

## Site briefs (the 5-skill content system)

`briefs/<slug>/site-brief.md` — one per site, drafted by `daily/build_briefs.py`
from crawl + audit data. The installed SEO skills (keyword-fanout-map,
seo-content-writer, onpage-optimizer, internal-link-architect,
ai-visibility-checker) read these files for voice, lane rules, money pages and
market settings. Fields marked ⚠️ are inferred — the owner confirms them.
Article production runs through the skill pipeline shown on each site's
dashboard page; the classic one-shot prompt remains as a no-skills fallback.

## Rules baked into the pipeline

- **Verified facts only.** Position drops are re-probed twice before being recorded.
- **One keyword → one page → one site.** `build_content.py` enforces market-level
  reservation: money-page hints, sibling coverage, and satellite lane isolation.
- **Frozen pages stay frozen** until live probes clear them.
- Checkbox progress is baked server-side from `checkbox_state.json` (owner pastes a
  "DASHBOARD PROGRESS" code from the Backlinks page).
