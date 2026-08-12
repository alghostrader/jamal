# Standing instructions — IPTV portfolio SEO (iptv.alghostrader.com)

## THE RULE: "update the dashboard" = FULL AUDIT, always

Whenever the owner says **"update the dashboard"** (or "good morning", or any request to
refresh it), that ALWAYS means a **complete, from-scratch audit of everything** — never a
partial refresh, never reusing yesterday's data. Then update **every** piece of information
on the dashboard that the fresh data touches. No stale claim may survive an update.

### Where the toolchain lives (read this first)

All audit scripts are committed at **`seo-tools/`** (see its README for the exact run
sequence). The working copy goes in the session scratchpad, but the repo is the source of
truth — the ephemeral workspace was recycled once (12 Aug 2026) and destroyed an
uncommitted toolchain. **After changing any script, commit it back to `seo-tools/`.**
Credentials are never committed: `dash/.env` (DataForSEO) and `gsc/sa.json` (Search
Console service account) must be re-supplied by the owner after a recycle.

### The full-audit checklist (all of it, every time)

1. **Crawl all 9 sites** — fresh BFS crawl (refresh sitemaps first). Never reuse an old crawl.
2. **GSC** — verified property list (sites.list — fact, not inference) + 90d traffic per site.
3. **DataForSEO** — backlinks/summary (rank, ref domains, spam) per site; volumes where needed.
4. **Live SERP probes** — re-probe every keyword target's position (refresh_kt_positions.py);
   re-probe any watched rankings (e.g. frozen-page re-evaluations) twice if a change is found.
5. **Fix verification** — diff fresh crawl against previous findings; mark every fixed item ✓
   and every claim from the owner's fix reports verified or not (verify independently, live).
6. **Content intel** — rebuild coverage/gaps with the cannibalization guards (sibling
   ownership, page hints, lane reservation). Recompute next-article prompts.
7. **Regenerate EVERY page** — home, Today queue, Trends, Links, Plan, all 9 site pages:
   prompts, opportunity cards, narratives, statuses, plan table, alerts, owner tasks.
   Anything conditional must be recomputed (steps auto-clear when work is verified done).
8. **History** — append authority + keyword-position history points.
9. **Deploy** — dashboard branch, pipeline marker, verify the marker live on
   iptv.alghostrader.com before reporting done.
10. **Report** — lead with what changed / what was verified / any alarm, then next tasks.

### Non-negotiables carried between sessions

- **Verified facts only** — never infer ("0 rows" ≠ "not in GSC"; call the API). If a tool
  reading disagrees with owner-verified data (e.g. PSI), the owner's live verification wins.
- **Anti-cannibalization is law** — one keyword, one page, one site per market. Lanes:
  prime = FR head terms · smarters-live = application/Smarters-Pro FR · pix = FR content ·
  spf = Smarters install/config · ifo = premium/HDR · aio = trial/deals + boitier.
- **Frozen pages stay frozen** until re-probes clear them (aio /test-iptv & /boitier-iptv,
  frozen 1 Aug, ~2-3 weeks) — support via internal links only.
- Dashboard generator lives in the session scratchpad (`scratchpad/daily/generate_v3.py`);
  deploys go to the `dashboard` branch as static HTML with a pipeline marker comment.
- Model ID never appears in commits/PRs. Git author is the owner's identity.
