"""Do next — ONE ranked queue merging Today + Work (Backlinks stays its own page).

Lanes: Do now (ranked 1..N, contiguous) · Needs Jamal (owner-only / blocked) · Monitor · Excluded (scope config).
A task clears only when it is LIVE-VERIFIED: deploy READY (Vercel API when a token exists, else inferred
from the live fetch) AND the change confirmed on the live URL (live_verify.py). Task state is the same
localStorage/Firestore document Today used (seo_tasks_v2 / seo_state/{uid}.tasks) — nothing changes for sync.
"""
import json, os, re, csv, html as _H, datetime as _dt, hashlib
import live_verify as LV

e = _H.escape
BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = _dt.date.today().isoformat()

# ───────────── SCOPE CONFIG (owner rule 8 Sep: European markets only) ─────────────
SCOPE = {
    "in": ["ES", "FR", "NL", "AL", "PL", "BE/CH"],
    "out_label": "Arab / MENA + rest of Africa",
    "out_words": ("alger", "algérie", "algerie", "algeria", "tunis", "tunisie", "tunisia", "maroc", "morocco", "marocain",
                  "afrique", "africa", "sénégal", "senegal", "côte d'ivoire", "cote d'ivoire", "cameroun", "cameroon",
                  "egypt", "égypte", "egypte", "libye", "libya", "mauritan", "maghreb", "arabe", "arabic", " arab",
                  "liban", "lebanon", "syrie", "syria", "emirat", "dubai", "dubaï", "qatar", "saoud", "saudi", "koweit", "kuwait",
                  "bahrein", "oman", "jordan", "jordanie", "irak", "iraq", "yemen", "yémen", "soudan", "sudan", "dz ", " dz"),
}
def out_of_scope(q):
    ql = " " + (q or "").lower() + " "
    return any(w in ql for w in SCOPE["out_words"])

TYPE_OF = {"Content gap": "Content", "Content decay": "Content", "Striking distance": "Striking distance",
           "CTR gap": "Striking distance", "Rank recovery": "Striking distance", "Technical fix": "Technical",
           "Indexation": "Technical", "Authority gap": "Backlink", "Backlink": "Backlink",
           "Compliance": "Compliance", "Cannibalisation": "Cannibalisation", "Footprint": "Footprint"}
ACTION_OF = {"Content gap": "CREATE", "Content decay": "ENHANCE", "Striking distance": "ENHANCE", "CTR gap": "ENHANCE",
             "Rank recovery": "ENHANCE", "Technical fix": "FIX", "Indexation": "FIX", "Authority gap": "PLACE", "Backlink": "PLACE",
             "Compliance": "FIX", "Cannibalisation": "FIX", "Footprint": "FIX"}
BADGE = {"Content": "b-content", "Striking distance": "b-striking", "Technical": "b-tech", "Backlink": "b-links", "Owner": "b-tech", "Blocked": "b-bad",
         "Compliance": "b-bad", "Cannibalisation": "b-warn", "Footprint": "b-tech"}


def slugify(s):
    s = LV.norm(s)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def build_donext(G, C):
    """G = generate_v3 globals · C = v4_pages context (TASKS, buckets, THIST, CLOUD, GS, KT, CT, SEM, SPOST, ...)."""
    ALL, ABBR, MONEY, CANON = G["ALL"], G["ABBR"], G["MONEY"], G["CANON"]
    KT, CT, GS, SEM = C["KT"], C["CT"], C["GS"], C["SEM"]
    TASKS, T_TODAY, T_NEXT, T_MONITOR = C["TASKS"], C["T_TODAY"], C["T_NEXT"], C["T_MONITOR"]
    THIST, CLOUD, STEPS = C["THIST"], C["CLOUD"], C["STEPS"]
    reserved_for, vol_of, insp_all = G["reserved_for"], C["vol_of"], C["insp_all"]
    REPOS = json.load(open(os.path.join(BASE, "site_repos.json")))
    cloud_tasks = CLOUD.get("tasks") or {}
    cache = LV.load_cache()
    vercel, vnote = LV.vercel_states(ALL)
    cache["vercel"] = vercel; cache["vercel_note"] = vnote
    crawl_by_site = {}
    for s in ALL:
        p = os.path.join(BASE, f"d_{ABBR[s]}", "crawl.json")
        try: crawl_by_site[s] = json.load(open(p)).get("pages", [])
        except Exception: crawl_by_site[s] = []
    hist_by_id = {c["id"]: c for c in THIST.get("completed", [])}
    try: G["_ledger_rows_pre"] = list(csv.DictReader(open(G["LEDGER_PATH"], encoding="utf-8")))
    except Exception: G["_ledger_rows_pre"] = []
    # ─── backlink ledger: decay check on every logged URL + promote pending rows ───
    LEDGER = G["LEDGER_PATH"]
    rows = list(csv.DictReader(open(LEDGER, encoding="utf-8"))) if os.path.exists(LEDGER) else []
    fields = ["site", "platform", "slug", "detail", "follow", "status", "verified", "url", "checked", "http"]
    KEY2DOM = {v: k for k, v in ABBR.items()}
    changed = False
    for r in rows:
        for f in fields: r.setdefault(f, "")
        if r["url"] and r["status"] in ("live", "pending", "decayed", "logged"):
            res = LV.check_backlink({"target_url": r["url"], "site": KEY2DOM.get(r["site"], r["site"])})
            r["checked"] = TODAY; r["http"] = str(res.get("http") or 0)
            new = ("live" if res.get("live") else "logged" if res.get("logged") else
                   "decayed" if (res.get("http") in (404, 410) or (r["status"] == "live" and res.get("http") == 200)) else r["status"])
            if new == "live":
                r["follow"] = "dofollow" if res.get("dofollow") else "nofollow"; r["verified"] = TODAY
            elif new == "logged" and not r.get("verified"):
                r["verified"] = TODAY   # owner-logged date; the platform refuses automated checks
            if new != r["status"]: r["status"] = new; changed = True
            cache.setdefault("links", {})[f'lp-{r["slug"]}-{r["site"]}'] = {**res, "checked": TODAY, "url": r["url"]}
    with open(LEDGER, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
    G["_ledger_rows"] = rows; G["_ledger_rows_pre"] = rows
    for c in THIST.get("completed", []):
        if out_of_scope(c.get("query") or "") and c.get("outcome") != "OUT OF SCOPE":
            c["outcome"] = "OUT OF SCOPE"; c["how"] = (c.get("how") or "").split(" · ")[0] + " · Arab/MENA market — filed under Excluded (owner rule 8 Sep)"
    open_ids = {t["id"] for t in TASKS}
    insp_open = {(s, p) for (s, p, v) in insp_all if v.get("verdict") not in (None, "PASS")}

    # ─── helpers ───
    def gsc_q(s, q):
        return GS.get(s, {}).get("queries", {}).get("cur", {}).get(q)
    def metric(s, q, page=""):
        g = gsc_q(s, q) if q else None
        v = vol_of(s, q) if q else None
        if g:
            return f'GSC pos {g["position"]:.1f} · {g["clicks"]} clicks · {g["impressions"]:,} impr / 28d'
        if v: return f"{v:,}/mo"
        if page: return page
        return "no volume data"
    STOP = ("iptv", "2026", "les", "des", "para", "por", "the", "een", "voor", "con", "com", "abonnement", "abonament")
    def sig_words(kw): return [w for w in LV.norm(kw).split() if len(w) > 2 and w not in STOP]
    def ranking_page(s, q):
        """GSC's own answer: the page that earns this query's impressions (query+page dimension)."""
        u = GS.get(s, {}).get("qpage", {}).get(q)
        if not u: return None
        return "/" + u.split("/", 3)[-1] if u.count("/") >= 3 else "/"
    def existing_page(s, kw):
        """A same-intent page already on this site → ENHANCE it, never a new URL.
        Order: strategic target page hint → GSC ranking page → article path/title → crawled URL slug."""
        r = next((r for r in KT.get(s, []) if r["kw"] == kw and r.get("page")), None)
        if r: return r["page"]
        rp_ = ranking_page(s, kw)
        if rp_ and rp_ != "/": return rp_
        words = sig_words(kw)
        if not words: return None
        for a in CT.get(s, {}).get("articles", []):
            hay = LV.norm(a.get("path", "") + " " + a.get("title", ""))
            if all(w in hay for w in words): return a.get("path")
        for pg in crawl_by_site.get(s, []):
            slug = LV.norm(pg.get("url", "").split("/")[-1].replace("-", " "))
            if slug and all(w in slug for w in words): return "/" + pg["url"].split("/", 3)[-1]
        return None
    def paths_in(txt): return re.findall(r"(/[A-Za-z0-9_\-/\.]+)", txt or "")
    def new_links_since(s, since):
        return sum(1 for r in G.get("_ledger_rows_pre", []) if r.get("site") == ABBR[s] and r.get("status") in ("live", "logged") and (r.get("verified") or r.get("checked") or TODAY) >= (since or "9999"))
    def done_when(kind, url, kw):
        if kind == "Content gap":
            return [f"article live at {url}, ≥ 900 words, real hero image", "internal links from 2 related pages + money-page CTA", "deploy READY + live fetch finds the keyword on the page"]
        if kind == "Content decay":
            return ["facts/year refreshed + the missing section added", "dateModified bumped on the page", "deploy READY + live fetch sees the new modified date"]
        if kind == "CTR gap":
            return ["title rewritten keyword-first, ≤ 60 chars", "meta description rewritten with the differentiator", "deploy READY + live title confirmed"]
        if kind in ("Striking distance", "Rank recovery"):
            return ["3+ internal links point at the ranking page with varied anchors", "on-query section refreshed + dateModified bumped", "deploy READY + live fetch finds the keyword on the page"]
        if kind == "Technical fix":
            return ["defect fixed in the repo (all flagged pages)", "deploy READY", "live re-check passes (thin pages ≥ 300 words / redirect 308 / zero broken links)"]
        if kind == "Indexation":
            return ["indexing requested in GSC", "canonical + robots checked", "URL Inspection = PASS"]
        if kind == "Compliance":
            return ["every flagged term removed or rewritten (title, meta, H1, body, alt)", "deploy READY", "next audit's compliance scan finds zero hits on this site"]
        if kind == "Cannibalisation":
            return ["the term is out of the non-owner page's title and H1", "one contextual link to the owner's page for that intent", "next audit: the non-owner site no longer appears in the top 50 for the term (GSC, may lag 2–4 weeks)"]
        if kind == "Footprint":
            return ["reciprocal links removed or nofollowed in one direction / duplicated pages rewritten", "deploy READY", "next audit's footprint scan no longer lists the pair"]
        return ["post published with a brand or naked-URL anchor", "live URL logged on the Backlinks page (that list is the ledger)", "live fetch: link present + dofollow"]

    # ─── task model ───
    def model(t, cs=None):
        cs = cs or cloud_tasks.get(t["id"]) or {}
        s, q, kind = t["site"], t.get("query") or "", t["kind"]
        if s not in CANON: return None   # owner/legacy records without a site cannot be live-checked
        rp = REPOS.get(s, {})
        typ, action = TYPE_OF.get(kind, "Content"), ACTION_OF.get(kind, "ENHANCE")
        note = ""
        url = ""
        ex = existing_page(s, q) if q else None
        if kind == "Content gap":
            if ex:
                action = "ENHANCE"; url = f"https://{CANON[s]}{ex}"
                note = f"page already targets this term ({ex}) — no new URL, enhance it"
            else:
                url = f"https://{CANON[s]}{rp.get('content_path', '/blog/')}{slugify(q)}"
                note = "check no same-intent page exists on this site or a same-market sibling before creating"
        elif kind in ("Striking distance", "CTR gap", "Rank recovery"):
            if ex: url = f"https://{CANON[s]}{ex}"; note = "page already ranks this term — enhance it, never a new URL"
            else: url = ""; note = "ranking page not resolved — set the live URL on the card (GSC → Pages for this query)"
            if ex == "/": note = "the homepage ranks this term — enhance the homepage section, never a new URL"
        elif kind == "Content decay":
            url = f"https://{CANON[s]}{t.get('page') or ''}"; note = "refresh in place — same URL keeps its history"
        elif kind == "Technical fix":
            url = f"https://{CANON[s]}/"; note = ""
        elif kind == "Indexation":
            url = f"https://{CANON[s]}{t.get('page') or ''}"
        elif kind == "Authority gap":
            url = f"https://{CANON[s]}{t.get('page') or MONEY.get(s, '/')}"; note = "links, not content — content alone will not close this gap"
        elif kind == "Compliance":
            url = f"https://{CANON[s]}{t.get('page') or '/'}"; note = "legal floor — same day; the scan lists every page"
        elif kind == "Cannibalisation":
            url = f"https://{CANON[s]}{t.get('page') or '/'}"; note = f"owner of the term: {t.get('owner', '')} — link to it, never a new URL"
        elif kind == "Footprint":
            url = f"https://{CANON[s]}/"; note = "reduce the network pattern; never add cross-links between owned sites"
        if cs.get("url"): url = cs["url"]  # owner-set live URL wins
        cat = C["tech_cat"](str(t.get("what") or "")) if kind == "Technical fix" else ""
        m = dict(id=t["id"], type=typ, kind=kind, site=s, repo_path=rp.get("repo", "—"), repo_content=rp.get("content", ""),
                 keyword=q, page=t.get("page") or "", metric=metric(s, q, t.get("page") or ""),
                 search_volume=vol_of(s, q) if q else None, gsc=gsc_q(s, q) if q else None,
                 target_url=url, action=action, cannibalization_note=note, deploy_as=REPOS.get("deploy_as", ""),
                 guards=REPOS.get("guards", []), done_when=done_when(kind, url or "(URL to set)", q),
                 priority_score=t.get("score", 0), effort=t.get("effort", "Medium"), effort_min=t.get("effort_min", 40),
                 what=t.get("what", ""), why=t.get("why", ""), why_action=t.get("action", ""), drivers=t.get("drivers", []),
                 category=cat, bucket=t.get("bucket", ""), completed=cs.get("completed"),
                 defect_gone=((kind in ("Technical fix", "Compliance", "Footprint", "Cannibalisation")) and t["id"] not in open_ids),
                 indexed=(kind == "Indexation" and all((s, p_) not in insp_open for p_ in (paths_in(t.get("what")) or [t.get("page") or ""]))),
                 new_links=(new_links_since(s, cs.get("completed")) if kind == "Authority gap" else 0))
        return m

    # ─── which tasks did the owner mark built? verify them LIVE now ───
    built = {}
    for tid, cs in cloud_tasks.items():
        if isinstance(cs, dict) and cs.get("state") == "completed" and not tid.startswith(("lp-", "owner_")):
            src = next((t for t in TASKS if t["id"] == tid), None)
            h = hist_by_id.get(tid)
            if out_of_scope((src or h or {}).get("query") or ""): continue
            m = model(src, cs) if src else (model({**h, "score": 0, "effort": "—", "effort_min": 0, "drivers": [], "action": "", "why": ""}, cs) if h else None)
            if m: built[tid] = m   # (a task no longer produced by the engine is verified from its history record)
    # auto-verified records (indexation / technical) count as built too
    for c in THIST.get("completed", []):
        if c["id"] not in built and c.get("kind") in ("Technical fix", "Indexation"):
            m = model({**c, "score": 0, "effort": "—", "effort_min": 0, "drivers": [], "action": "", "why": ""}, {"completed": c.get("completed")})
            if m: built[c["id"]] = m
    to_check = [m for m in built.values()]
    results = LV.verify_tasks(to_check, crawl_by_site, CANON, vercel) if to_check else {}
    for tid, r in results.items():
        prev = (cache.get("tasks") or {}).get(tid) or {}
        if prev.get("live") and r.get("http") == 0:
            r = {**prev, "detail": prev.get("detail", "") + f" · re-fetch unreachable on {TODAY}, keeping the earlier verified result"}
        if r.get("live") and not prev.get("verified_at"):
            h = hist_by_id.get(tid)
            r["verified_at"] = (h.get("completed") if (h and h.get("outcome") == "VERIFIED") else TODAY)
        elif prev.get("verified_at") and r.get("live"):
            r["verified_at"] = prev["verified_at"]
        cache.setdefault("tasks", {})[tid] = r
        # keep task_history honest: live-verified → VERIFIED, else AWAITING with the live detail
        h = hist_by_id.get(tid)
        if h:
            if r.get("live"):
                if h.get("outcome") in ("AWAITING VERIFICATION", None): h["outcome"] = "VERIFIED"
                h["live_check"] = r.get("detail")
            else:
                if h.get("outcome") == "VERIFIED" and h.get("kind") not in ("Indexation",): h["outcome"] = "AWAITING VERIFICATION"
                h["live_check"] = r.get("detail")
    LV.save_cache(cache)

    # ─── lanes ───
    def st_of(tid): return (cloud_tasks.get(tid) or {}) if isinstance(cloud_tasks.get(tid), dict) else {}
    live_ids = {tid for tid, r in (cache.get("tasks") or {}).items() if r.get("live")}
    # Do now = today + next engine tasks that are Claude-actionable and not dismissed/deferred/completed
    do_src = [t for t in T_TODAY if st_of(t["id"]).get("state") not in ("completed", "dismissed", "deferred")]
    do_models = [m for m in (model(t) for t in do_src) if m]
    next_src = [t for t in T_NEXT if st_of(t["id"]).get("state") not in ("completed", "dismissed", "deferred")]
    next_models = [m for m in (model(t) for t in next_src) if m]
    # backlinks: the ledger's Do-next placements (P1) become ranked cards too
    G["ledger_checklist"]()
    for key, pid, label, pr, own in getattr(G["ledger_checklist"], "donext", []):
        dom = KEY2DOM[key]; lid = f"lp-{pid}-{key}"
        if (CLOUD.get("links") or {}).get(lid): continue
        sc = 55 if key == "rodak" else 45
        do_models.append(dict(id=lid, type="Backlink", kind="Backlink", site=dom, repo_path="—", repo_content="",
                              keyword=label, page="", metric=f"{pr} placement · brand / naked anchor", search_volume=None, gsc=None,
                              target_url=f"https://{CANON[dom]}/", action="PLACE",
                              cannibalization_note="anchor = brand or naked URL only — never money keywords",
                              deploy_as="owner publishes (signup + CAPTCHA + publish)", guards=["no rights-holder / channel / league names", "no fake reviews / address"],
                              done_when=done_when("Backlink", "", ""), priority_score=sc, effort="Quick", effort_min=25,
                              what=f"{label} for {dom}.", why="Authority is the ceiling on this site — one quality link moves the whole domain.",
                              why_action="Publish the post, then paste the live URL when you tick it: that write IS the ledger.",
                              drivers=["authority gap"], category="", bucket="links", completed=None, defect_gone=False, indexed=False))
    # guest posts + expert quotes (outreach_targets.json): the links that actually move authority.
    # One card per priority site (paused sites skipped); ticking it = placement logged in the ledger (lp-gp-… id).
    try: OUT = json.load(open(os.path.join(BASE, "outreach_targets.json")))
    except Exception: OUT = {"platforms": [], "prospects": {}, "ideas": {}}
    LANG_OF = {"iptvesp.com": "es", "iptvsegura.com": "es", "iptvned.com": "nl", "rodaktv.com": "pl", "iptvshqiptar.com": "sq"}
    for s_ in ALL:
        if s_ not in LANG_OF: LANG_OF[s_] = "fr"
    PRIO = ["iptvesp.com", "iptvned.com", "rodaktv.com", "iptvsegura.com", "smartersprofrance.fr", "primeiptv-france.com", "iptvshqiptar.com"]
    cloud_links = CLOUD.get("links") or {}
    outreach = []
    for s_ in PRIO:
        key = ABBR[s_]
        if key in (G["PAUSED_LINKS"] or {}): continue
        for pr_ in sorted(OUT["prospects"].get(LANG_OF[s_], []), key=lambda x: -x["as"]):
            if s_ not in pr_["sites"]: continue
            lid = f'lp-gp-{pr_["slug"]}-{key}'
            if cloud_links.get(lid): continue
            outreach.append(dict(id=lid, type="Backlink", kind="Backlink", site=s_, repo_path="—", repo_content="",
                                 keyword=f'{pr_["domain"]} — {pr_["type"]}', page="", metric=f'authority {pr_["as"]} · {pr_["type"]}', search_volume=None, gsc=None,
                                 target_url=f'https://{pr_["domain"]}/', action="PITCH",
                                 cannibalization_note="one contextual link, brand or naked-URL anchor, to a guide page (not the pricing page)",
                                 deploy_as="owner sends the pitch and handles the editor; Claude writes pitch + article + quote",
                                 guards=["no rights-holder / channel / league names", "no '100% legal' claims", "real screenshots we own", "author alghostrader"],
                                 done_when=["pitch sent from the owner's mailbox (draft in seo-tools/links/PITCHES-*.md)", "editor accepted · article or quote delivered",
                                            "live URL pasted here → the audit checks it is live + dofollow"],
                                 priority_score=50 + (pr_["as"] >= 40) * 2, effort="Deep work", effort_min=90,
                                 what=f'{pr_["type"].capitalize()} on {pr_["domain"]} (authority {pr_["as"]}) for {s_}. Angle: {OUT["ideas"].get(s_, "")}',
                                 why="One in-content dofollow link from an indexed, relevant domain is worth more than the whole directory set.",
                                 why_action=pr_["how"], drivers=["authority is the ceiling on this site", f'target authority {pr_["as"]}'],
                                 category="", bucket="links", completed=None, defect_gone=False, indexed=False))
            break   # one outreach card per site in the queue; the rest are on the Backlinks page
    bl = [m for m in do_models if m["type"] == "Backlink"]
    for m in bl[2:]: do_models.remove(m)   # the rest stay on the Backlinks page
    do_models += outreach[:2]
    if sum(1 for m in do_models if m["type"] not in ("Backlink", "Compliance")) < 3:
        seen = {m["id"] for m in do_models}
        for t in sorted(T_NEXT + T_MONITOR, key=lambda t: -t["score"]):
            if sum(1 for m in do_models if m["type"] not in ("Backlink", "Compliance")) >= 3: break
            if t["id"] in seen or t.get("improving") or st_of(t["id"]).get("state") in ("completed", "dismissed", "deferred"): continue
            m = model(t)
            if m: m["why_action"] = (m.get("why_action") or "") + " (backfilled from Monitor: the queue was short)"; do_models.append(m); seen.add(t["id"])
    do_models.sort(key=lambda m: -m["priority_score"])
    # verifying = built by the owner, not live yet · shipped = live-verified
    verifying, shipped = [], []
    for tid, m in built.items():
        r = (cache.get("tasks") or {}).get(tid) or {}
        m["verify"] = r
        (shipped if r.get("live") else verifying).append(m)
    shipped.sort(key=lambda m: (m["verify"].get("verified_at") or ""), reverse=True)
    shipped_today = [m for m in shipped if m["verify"].get("verified_at") == TODAY]
    shipped_earlier = [m for m in shipped if m["verify"].get("verified_at") != TODAY]
    # promoted-from-monitor candidates rendered hidden (state decides visibility, like Today did)
    _in_do = {x["id"] for x in do_models}
    next_models = [m for m in next_models if m["id"] not in _in_do]
    promo_models = next_models + [m for m in (model(t) for t in T_MONITOR[:12] if t["id"] not in _in_do) if m]

    # ─── Needs Jamal ───
    needs = []
    for dom, v in vercel.items():
        if v.get("state") in ("BLOCKED", "ERROR", "CANCELED"):
            needs.append(dict(id=f'owner_deploy_{ABBR[dom]}_{(v.get("at") or 0)}', badge="Blocked", title=f"Vercel deploy {v['state']} on {dom} — authorize / redeploy",
                              meta=f"auto-detected from the Vercel API · project {v.get('project')}", link=v.get("inspector"),
                              lines=[("cause", "commit author not a recognised Vercel member, or the build failed"), ("fix", "open the inspector, Redeploy / authorize; every task on this site waits until READY")],
                              cta="Mark authorized", blocked=True))
    if not vercel:
        needs.append(dict(id="owner_vercel_token", badge="Owner", title="Add VERCEL_TOKEN to dash/.env so BLOCKED deploys are detected automatically",
                          meta=vnote, link="https://vercel.com/account/tokens",
                          lines=[("why", "without it the board infers “deployed” from the live fetch and cannot see a BLOCKED build"),
                                 ("how", "Vercel → Account → Tokens → create (read scope) → paste as VERCEL_TOKEN=… (+ VERCEL_TEAM_ID if the projects live in a team)")],
                          cta="Done — token added"))
    try: _pl = json.load(open(os.path.join(BASE, "outreach_targets.json"))).get("platforms", [])
    except Exception: _pl = []
    if _pl and not (cloud_tasks.get("owner_quote_accounts_v1") or {}).get("state") == "completed":
        needs.append(dict(id="owner_quote_accounts_v1", badge="Owner", title="Create the expert-quote accounts (signup + CAPTCHA are owner-only)",
                          meta=" · ".join(p_["name"].split(" (")[0] for p_ in _pl[:6]),
                          lines=[(p_["name"].split(" (")[0], f'{p_["url"]} — {p_["cost"]} · {p_["how"]}') for p_ in _pl],
                          cta="Accounts created"))
    _stale = [ABBR[d_] for d_ in ALL if (SEM.get(d_) or {}).get("date") and (SEM.get(d_) or {}).get("date") < TODAY and "exhausted" in ((SEM.get(d_) or {}).get("ok_delta") or "")]
    if _stale:
        needs.append(dict(id=f"owner_semrush_units_{TODAY}", badge="Owner", title=f"Semrush API units are at zero — top up so authority readings refresh ({len(_stale)} sites on yesterday's data)",
                          meta="sites on the last reading: " + ", ".join(_stale), link="https://www.semrush.com/kb/1235-api-units",
                          lines=[("why", "the Authority page and the referring-domain deltas stay frozen for these sites until the API has units again"),
                                 ("how", "Semrush → Subscription info → API units → add units; the next audit refreshes all 11 sites")], cta="Units added"))
    wk = _dt.date.today().isocalendar()[1]
    needs.append(dict(id=f"owner_sales_w{wk}", badge="Owner", title="Send this week's sales numbers per site", meta="feeds revenue-weighted prioritisation",
                      lines=[("why", "so the queue ranks by € earned, not only search volume"), ("format", "site · new subs · renewals · revenue — a WhatsApp line per site is enough")], cta="Mark sent"))
    briefs_dir = next((p for p in (os.path.join(BASE, "..", "..", "..", "..", "home", "user", "jamal", "seo-tools", "briefs"), "/home/user/jamal/seo-tools/briefs", os.path.join(BASE, "briefs")) if os.path.isdir(p)), None)
    warn = {}
    if briefs_dir:
        for d in sorted(os.listdir(briefs_dir)):
            f = os.path.join(briefs_dir, d, "site-brief.md")
            if os.path.exists(f):
                n = sum(1 for line in open(f, encoding="utf-8") if "⚠" in line and "Anything marked" not in line)
                if n: warn[d] = n
    if warn:
        needs.append(dict(id="owner_briefs_v1", badge="Owner", title=f"Fill the ⚠ placeholder fields in seo-tools/briefs/ ({sum(warn.values())} fields, {len(warn)} sites)",
                          meta=" · ".join(f"{k} {v}" for k, v in warn.items()),
                          lines=[("why", "prices, customer value, author identity and competitor confirmations feed the content prompts — placeholders block index-ready pages"),
                                 ("where", "seo-tools/briefs/<site>/site-brief.md — every line marked ⚠")], cta="Mark reviewed"))
    for key, why in (G["PAUSED_LINKS"] or {}).items():
        needs.append(dict(id=f"owner_links_review_{key}", badge="Owner", title=f"Review the newest links on {KEY2DOM[key]} ({why}) and decide: resume or disavow",
                          meta="link building is paused on this site until you decide", lines=[("rule", "+4-pt spam-score jump = pause; review the newest referring domains in Semrush → Backlinks → new")], cta="Reviewed — resume"))
    for m in verifying:
        if m.get("verify", {}).get("blocked"):
            needs.append(dict(id=f'owner_blocked_{m["id"]}', badge="Blocked", title=f'{m["type"]}: {m["keyword"] or m["page"] or m["site"]} — deploy blocked on {m["site"]}',
                              meta=m["verify"].get("detail", ""), link=(vercel.get(m["site"]) or {}).get("inspector"), lines=[("fix", "authorize the deploy, then the next audit live-verifies this task")], cta="Mark authorized", blocked=True))

    # ─── Excluded (scope filter) ───
    excl = {}
    for s in ALL:
        for q, v in GS.get(s, {}).get("queries", {}).get("cur", {}).items():
            if out_of_scope(q) and v["impressions"] >= 10 and v["position"] <= 30:
                sc = min(30, v["impressions"] // 10) + max(0, 25 - int(v["position"])) + 20
                excl[(s, q)] = dict(site=s, q=q, score=sc, why=f'GSC pos {v["position"]:.0f} · {v["impressions"]:,} impr / 28d')
        for r in CT.get(s, {}).get("recommend", []):
            if out_of_scope(r["kw"]) and (s, r["kw"]) not in excl:
                excl[(s, r["kw"])] = dict(site=s, q=r["kw"], score=min(30, (r["vol"] or 0) // 100) + 25, why=f'{r["vol"] or 0:,}/mo keyword idea')
        for r in KT.get(s, []):
            if out_of_scope(r["kw"]) and (s, r["kw"]) not in excl:
                excl[(s, r["kw"])] = dict(site=s, q=r["kw"], score=53, why="strategic target list — out of scope")
    for c in THIST.get("completed", []):
        if c.get("outcome") == "OUT OF SCOPE" and (c.get("site"), c.get("query")) not in excl and c.get("site") in ALL:
            excl[(c["site"], c["query"])] = dict(site=c["site"], q=c["query"], score=0, why="completed before the scope rule — no follow-up")
    excluded = sorted(excl.values(), key=lambda x: -x["score"])

    # ─── export the data model (audit trail + next audit) ───
    json.dump({"date": TODAY, "scope": SCOPE, "vercel_note": vnote,
               "do_now": do_models, "verifying": [{k: v for k, v in m.items()} for m in verifying],
               "shipped": [{k: v for k, v in m.items()} for m in shipped], "needs": needs, "monitor": [m for m in (model(t) for t in T_MONITOR) if m],
               "excluded": excluded}, open(os.path.join(BASE, "donext.json"), "w"), indent=1, default=str)

    est = sum(m["effort_min"] for m in do_models)
    G["DONEXT_N"] = len(do_models)

    # ═════════════ DO-NEXT.md — the same queue for Claude Code sessions without a browser ═════════════
    def md_task(m, i=None, verify=None):
        verify = verify or {}
        title = m["keyword"] or m["page"] or (m["category"].title() if m["category"] else m["site"])
        head = (f"### {'#' + str(i) if i else '…'} {m['type']} — {title} · {m['site']}")
        lines = [head, f"- id: `{m['id']}` · score {m['priority_score']} · {m['effort']} ≈{m['effort_min']} min · {m['metric']}",
                 f"- repo: `{m['repo_path']}`" + (f" ({m['repo_content']})" if m['repo_content'] else ""),
                 f"- action: **{m['action']}** → {m['target_url'] or '(URL not resolved — set it in the update line)'}"]
        if m["cannibalization_note"]: lines.append(f"- ⚠ {m['cannibalization_note']}")
        lines.append(f"- what: {m['what']}" + (f" {m['why_action']}" if m.get("why_action") else ""))
        lines.append(f"- deploy-as: {m['deploy_as']} · guards: " + " · ".join(m["guards"]))
        lines.append("- done when: " + " / ".join(m["done_when"]))
        if verify.get("detail"): lines.append(f"- live check ({verify.get('checked', '')}): {verify['detail']}")
        return "\n".join(lines) + "\n"
    md = [f"# DO NEXT — IPTV portfolio · generated {TODAY} by the dashboard audit",
          "",
          "This file IS the task board (same data as iptv.alghostrader.com/today, lane **Do now**). Work top-down: #1 is the next task.",
          "A task is DONE only when it is live-verified by the next audit (deploy READY + change confirmed on the live URL).",
          "",
          "## How to mark a task done (no browser needed)",
          "Append ONE line per task to `seo-tools/daily/task_updates.jsonl`, then commit + push this repo (branch `claude/iptvpix-seo-audit-l68bmx`):",
          "```",
          '{"id": "<id from the task>", "state": "completed", "url": "https://<exact live URL you changed or published>", "date": "YYYY-MM-DD", "by": "iptv-session", "note": "what was changed (1 line)"}',
          "```",
          "States: `completed` (built + deployed) · `deferred` · `dismissed` (with a note why) · `active` (started). Always give the live URL for content/enhance tasks:",
          "the audit fetches it and checks keyword + modified date (add `dateModified` / `og:updated_time` to the page). For a backlink id (`lp-…`) the url is the placement URL.",
          "The next audit merges these lines with the owner's browser ticks (Firestore) and moves the task to Shipped only after the live check passes.",
          "",
          f"## Do now — {len(do_models)} tasks, ≈{est//60}h {est%60:02d}m", ""]
    md += [md_task(m, i + 1) for i, m in enumerate(do_models)]
    md += ["", f"## Verifying — {len(verifying)} built, not live yet (what is still missing)", ""]
    md += [md_task(m, None, m["verify"]) for m in verifying]
    md += ["", f"## Shipped (live-verified) — {len(shipped)}", ""]
    md += [f"- ✓ {m['type']} — {m['keyword'] or m['page'] or m['category']} · {m['site']} · verified {m['verify'].get('verified_at')} · {m['verify'].get('detail', '')}" for m in shipped]
    md += ["", f"## Needs Jamal (owner-only / blocked) — {len(needs)}", ""]
    md += [f"- {n['badge']}: {n['title']} — {n['meta']}" for n in needs]
    md += ["", f"## Monitor — {len(T_MONITOR)} watch items (do not work on these)", ""]
    md += [f"- {t['kind']}: {t.get('query') or t.get('page')} · {ABBR[t['site']]} · score {t['score']}" for t in T_MONITOR[:25]]
    md += ["", f"## Excluded — {len(excluded)} out-of-scope ({SCOPE['out_label']}) — never work on these", ""]
    md += [f"- {x['q']} · {ABBR.get(x['site'], x['site'])}" for x in excluded]
    md += ["", "## Rules", "- One keyword, one page, one site per market — ENHANCE the ranking page, never create a competing URL.",
           "- Commits authored by alghostrader (other authors land BLOCKED on Vercel).",
           "- No rights-holder / channel / league / broadcaster names. Title ≤ 60 chars. Real hero image.",
           "- Backlinks: brand or naked-URL anchors only; signup + CAPTCHA + publish = owner only.", ""]
    open(os.path.join(BASE, "DO-NEXT.md"), "w", encoding="utf-8").write("\n".join(md))

    # ═════════════ HTML ═════════════
    def track(m, state="", verify=None):
        verify = verify or {}
        if m["type"] == "Backlink": labels = ("Placed", "Logged", "Live")
        else: labels = ("Built", "Deployed", "Live")
        built_ = state == "completed" or bool(verify)
        dep = bool(verify.get("deployed")); liv = bool(verify.get("live")); blk = bool(verify.get("blocked"))
        steps = [("done" if built_ else ("now" if state == "active" else ""), labels[0]),
                 ("blocked" if blk else ("done" if dep else ""), labels[1]),
                 ("done" if liv else "", labels[2])]
        h = ""
        for i, (cls, lab) in enumerate(steps):
            if i: h += f'<span class="conn {"done" if steps[i-1][0] == "done" else ""}"></span>'
            h += f'<span class="step {cls}" data-step="{i}"><span class="pip"></span><span class="lbl-txt">{lab}</span></span>'
        return f'<span class="track">{h}</span>'

    def card(m, rank=None, state="", verify=None, shipped_=False, promo=False):
        verify = verify or {}
        b = BADGE.get(m["type"], "b-tech")
        title = m["keyword"] or m["page"] or (m["category"].title() if m["category"] else m["site"])
        if m["type"] == "Technical" and m["category"]: title = m["category"].title() + (f" · {m['page']}" if m["page"] else "")
        rank_html = ('<span class="rank">✓</span>' if shipped_ else f'<span class="rank num">{rank if rank else "…"}</span>')
        lines = [("repo", e(m["repo_path"]) + (f' <span class="dim">{e(m["repo_content"])}</span>' if m["repo_content"] else "")),
                 ("action", f'<b>{e(m["action"])}</b> → {e(m["target_url"] or "(set the live URL below)")}' + (f' <span class="warnflag">⚠ {e(m["cannibalization_note"])}</span>' if m["cannibalization_note"] else "")),
                 ("deploy-as", e(m["deploy_as"])),
                 ("guards", " · ".join(e(g) for g in m["guards"]))]
        if m.get("why_action"): lines.insert(1, ("what", e(m["why_action"])))
        if verify.get("detail"): lines.append(("live check", e(verify["detail"]) + (f' · Vercel {e(verify["vercel"])}' if verify.get("vercel") else "") + f' · {e(verify.get("checked", ""))}'))
        ws = "".join(f'<div class="line"><span class="key">{k}</span><span class="val">{v}</span></div>' for k, v in lines)
        dw = "".join(f'<li class="{"ok" if (shipped_ or (verify.get("live"))) else "pending"}"><span class="mk">{"✓" if (shipped_ or verify.get("live")) else "○"}</span> {e(x)}</li>' for x in m["done_when"])
        is_lp = m["id"].startswith("lp-")
        url_in = ((f'<input class="lpx" type="checkbox" id="{e(m["id"])}" hidden>' if is_lp else "") +
                  f'<div class="urlrow"><label>{"Placement URL" if is_lp else "Live URL"}</label><input type="url" class="t-url" placeholder="{"https://… the published post (the audit checks it is live + dofollow)" if is_lp else "https://" + e(CANON[m["site"]]) + "/… (paste the exact live URL — the next audit fetches it)"}" value="{e((st_of(m["id"]).get("url") or ""))}"><button class="act t-urlsave">Save</button></div>')
        steps_json = e(json.dumps(STEPS.get(m["kind"], ["Do the recommended action", "Re-check next audit"])))
        drivers = "".join(f"<li>{e(x)}</li>" for x in m.get("drivers", []))
        why = (f'<details class="why"><summary>Why this priority? (score {m["priority_score"]})</summary><ul>{drivers}</ul><div class="dim">{e(m.get("why", ""))}</div></details>' if drivers else "")
        actions = (f'<div class="actions" data-lane="{"ship" if shipped_ else "do"}">'
                   f'<button class="act primary t-start">Start</button><button class="act t-done">Mark complete</button>'
                   f'<button class="act t-defer">Defer</button><button class="act t-dismiss">Dismiss</button>'
                   f'<button class="act t-undo">Undo</button>'
                   + (f'<a class="act" href="{e(m["target_url"])}" target="_blank" rel="noopener">Open live page ↗</a>' if m["target_url"] else "") + '</div>')
        cls = "card task" + (" ship" if shipped_ else "") + (" blocked" if verify.get("blocked") else "")
        tail = (f'live-verified {e(verify.get("verified_at") or "")}' if shipped_ else
                (f'built {e(m.get("completed") or "")} · awaiting live check' if (state == "completed" and not m["effort_min"]) else f'{e(m["effort"])} ≈{m["effort_min"]}m'))
        promo_attr = ' data-promo="1" hidden' if promo else ""
        return (f'<article class="{cls}" data-tid="{m["id"]}" data-type="{e(m["type"])}" data-site="{e(m["site"])}" data-min="{m["effort_min"]}" '
                f'data-score="{m["priority_score"]}" data-title="{e(m["kind"])}: {e(title[:80])}" data-steps="{steps_json}" data-live="{1 if verify.get("live") else 0}" data-built="{1 if state == "completed" else 0}"{promo_attr}>'
                f'<button class="chead" aria-expanded="false">{rank_html}<span class="ctitle"><span class="row1"><span class="badge {b}">{e(m["type"])}</span>'
                f'<h3>{"“" + e(title) + "”" if m["keyword"] and m["type"] != "Backlink" else e(title)}</h3></span>'
                f'<span class="meta"><span class="site">{e(m["site"])}</span><span class="sep"></span>{e(m["metric"])}<span class="sep"></span>{tail}</span></span>'
                f'<span class="cright">{track(m, state, verify)}<span class="chev">›</span></span></button>'
                f'<div class="spec"><p class="what">{e(m["what"])}</p><div class="worksheet">{ws}</div>{url_in}'
                f'<div class="dw"><span class="dwt">Done when{" — all checks passed" if shipped_ else ""}</span><ul>{dw}</ul></div>{why}{actions}</div></article>')

    def needs_card(n):
        lines = "".join(f'<div class="line"><span class="key">{e(k)}</span><span class="val">{e(v)}</span></div>' for k, v in n["lines"])
        link = f'<a class="act primary" href="{e(n["link"])}" target="_blank" rel="noopener">Open ↗</a>' if n.get("link") else ""
        return (f'<article class="card task{" blocked" if n.get("blocked") else ""}" data-tid="{e(n["id"])}" data-owner="1" data-title="{e(n["title"][:80])}" data-min="0">'
                f'<button class="chead" aria-expanded="false"><span class="rank">{"!" if n.get("blocked") else "J"}</span><span class="ctitle"><span class="row1">'
                f'<span class="badge {BADGE.get(n["badge"], "b-tech")}">{e(n["badge"])}</span><h3>{e(n["title"])}</h3></span><span class="meta">{e(n["meta"])}</span></span>'
                f'<span class="cright"><span class="chev">›</span></span></button>'
                f'<div class="spec"><div class="worksheet">{lines}</div><div class="actions">{link}<button class="act primary t-done">{e(n["cta"])}</button><button class="act t-undo">Undo</button></div></div></article>')

    def rrow(m, kind="monitor"):
        if kind == "monitor":
            btn = f'<button class="ghost t-promote" data-tid="{m["id"]}">Add to Do now</button>'
            sub = m["what"]
        else:
            btn = '<span class="badge b-bad">Out of scope</span>'; sub = f'{SCOPE["out_label"]} — {m["why"]}'
        title = m.get("keyword") or m.get("q") or m.get("page") or m["site"]
        return (f'<div class="rrow" data-tid="{e(m.get("id", ""))}"><span class="score">{m.get("priority_score", m.get("score", ""))}</span>'
                f'<span class="rt"><b>{e(title)}</b><div class="m"><span class="site">{e(ABBR.get(m["site"], m["site"]))}</span> · {e(sub)}</div></span>{btn}</div>')

    do_html = "".join(card(m, i + 1) for i, m in enumerate(do_models)) or '<div class="empty">Nothing to do — the engine found no open task. Links and content cadence continue as standing work.</div>'
    promo_html = "".join(card(m, None, promo=True) for m in promo_models)
    ver_html = "".join(card(m, None, "completed", m["verify"]) for m in verifying)
    ship_html = "".join(card(m, None, "completed", m["verify"], shipped_=True) for m in shipped_today)
    earlier_html = "".join(card(m, None, "completed", m["verify"], shipped_=True) for m in shipped_earlier)
    needs_html = "".join(needs_card(n) for n in needs)
    next_html = "".join(rrow(m) for m in next_models) or '<div class="rrow"><span class="rt">Nothing deferred.</span></div>'
    mon_html = "".join(rrow(m) for m in (model(t) for t in T_MONITOR) if m) or '<div class="rrow"><span class="rt">Nothing on watch.</span></div>'
    exc_html = "".join(rrow(x, "excluded") for x in excluded) or '<div class="rrow"><span class="rt">Nothing excluded.</span></div>'
    gsc_when = (C.get("GSCD") or {}).get("generated", "") or TODAY
    sites_opt = "".join(f'<option value="{e(s)}">{e(s)}</option>' for s in ALL)
    scope_in = " · ".join(SCOPE["in"])
    vercel_line = ("Vercel API on — deploy state read per site." if vercel else e(vnote))

    body = f'''
<div class="dn">
<p class="lead">One ranked queue — <b>Today</b> and <b>Work</b> merged. Item <b>#1</b> is the next thing to do. A task clears only when it is <b>live-verified</b> (deploy READY + change confirmed on the live URL), never when it is merely committed. <span class="dim">{vercel_line}</span></p>
<section class="summary" aria-label="Queue summary">
  <div class="tile do"><span class="stripe"></span><div class="k">To do now</div><div class="v num" id="c-do">{len(do_models)}</div><div class="s">≈ <span id="c-est">{est//60}h {est%60:02d}m</span> of work</div></div>
  <div class="tile ship"><span class="stripe"></span><div class="k">Shipped today</div><div class="v num" id="c-ship">{len(shipped_today)}</div><div class="s">all live-verified · <span id="c-ver">{len(verifying)}</span> awaiting live check</div></div>
  <div class="tile hiba"><span class="stripe"></span><div class="k">Needs Jamal</div><div class="v num" id="c-needs">{len(needs)}</div><div class="s">owner-only / blocked</div></div>
  <div class="tile watch"><span class="stripe"></span><div class="k">Monitoring</div><div class="v num" id="c-mon">{len(T_MONITOR)}</div><div class="s">don't touch yet</div></div>
  <div class="tile excl"><span class="stripe"></span><div class="k">Excluded</div><div class="v num" id="c-exc">{len(excluded)}</div><div class="s">out of scope</div></div>
</section>
<div class="dngrid">
<div>
  <div class="lanes" role="tablist" aria-label="Lanes">
    <button class="lane-btn" role="tab" aria-selected="true" data-panel="do">Do now <span class="c num" id="l-do">{len(do_models)}</span></button>
    <button class="lane-btn warn" role="tab" aria-selected="false" data-panel="needs">Needs Jamal <span class="c num" id="l-needs">{len(needs)}</span></button>
    <button class="lane-btn slate" role="tab" aria-selected="false" data-panel="monitor">Monitor <span class="c num" id="l-mon">{len(T_MONITOR)}</span></button>
    <button class="lane-btn slate" role="tab" aria-selected="false" data-panel="excluded">Excluded <span class="c num" id="l-exc">{len(excluded)}</span></button>
  </div>
  <section class="panel active" id="p-do" role="tabpanel">
    <div class="toolbar"><label>Site</label><select class="sel" id="sitefilter"><option value="">All websites</option>{sites_opt}</select>
      <span class="dim" style="margin-left:auto">Sorted by priority score · highest first · ranks renumber as you work</span></div>
    <div id="focusbar" hidden></div>
    <div class="stack" id="shipped">{ship_html}</div>
    <div class="stack" id="queue">{do_html}{promo_html}</div>
    <div class="subhead" id="ver-head" {"" if verifying else "hidden"}><h2>Verifying — built, not live yet</h2><span class="note">the next audit fetches the live URL; until it passes these do not count as done</span></div>
    <div class="stack" id="verifying">{ver_html}</div>
    <div class="subhead" id="park-head" hidden><h2>Parked — deferred / dismissed</h2><span class="note">nothing is terminal: restore any of them</span></div>
    <div class="stack" id="parked"></div>
    <details class="earlier" {"" if next_models else "hidden"} style="margin-top:14px"><summary>Next — {len(next_models)} deferred, not forgotten (score ≥ 52) · promote one to Do now if it out-scores the queue</summary><div class="rows" id="nextlist" style="margin-top:10px">{next_html}</div></details>
    <details class="earlier" {"" if shipped_earlier else "hidden"}><summary>Shipped earlier — {len(shipped_earlier)} live-verified</summary><div class="stack" style="margin-top:10px">{earlier_html}</div></details>
  </section>
  <section class="panel needs" id="p-needs" role="tabpanel" hidden>
    <div class="panelhead"><h2>Needs Jamal</h2><span class="note">Owner-only or blocked — parked here so the queue stays purely actionable.</span></div>
    <div class="stack" id="needs">{needs_html}</div>
  </section>
  <section class="panel" id="p-monitor" role="tabpanel" hidden>
    <div class="panelhead"><h2>Monitor — don't touch yet</h2><span class="note">The engine is protecting your attention. Promote one only if it out-scores the queue.</span></div>
    <div class="rows" id="monitor">{mon_html}</div>
  </section>
  <section class="panel excl" id="p-excluded" role="tabpanel" hidden>
    <div class="panelhead"><h2>Excluded — out of scope</h2><span class="note">Auto-filed by the scope filter. Never enters the queue.</span></div>
    <div class="rows">{exc_html}</div>
  </section>
</div>

</div>
</div>'''
    return body


DONEXT_JS = r"""<script>
(function(){
 var K='seo_tasks_v2', TODAY=new Date().toISOString().slice(0,10);
 function load(){ try{return JSON.parse(localStorage.getItem(K)||'{}');}catch(e){return{};} }
 function save(st){ try{localStorage.setItem(K,JSON.stringify(st));}catch(e){} if(window.seoCloudSave) window.seoCloudSave(st); }
 var st=load();
 var Q=document.getElementById('queue'), V=document.getElementById('verifying'), P=document.getElementById('parked'), S=document.getElementById('shipped');
 function fmt(m){ return Math.floor(m/60)+'h '+('0'+(m%60)).slice(-2)+'m'; }
 function setStep(card,i,cls){ var s=card.querySelector('.step[data-step="'+i+'"]'); if(!s) return; s.className='step'+(cls?' '+cls:''); var c=s.previousElementSibling; if(c&&c.classList.contains('conn')) c.classList.toggle('done', cls==='done'); }
 function place(card, where){ if(card.parentElement!==where) where.appendChild(card); }
 function apply(){
  var site=(document.getElementById('sitefilter')||{}).value||'';
  var open=[], ver=0, park=0, done=0, mins=0;
  document.querySelectorAll('article.task[data-tid]').forEach(function(c){
    var id=c.dataset.tid, s=st[id]||{}, state=s.state||'', live=c.dataset.live==='1', owner=c.dataset.owner==='1', promo=c.dataset.promo==='1';
    if(!s.state && c.dataset.built==='1') state='completed';
    if(owner){ c.classList.toggle('done', state==='completed'); var cta=c.querySelector('.t-done'); if(cta) cta.hidden=(state==='completed'); var u=c.querySelector('.t-undo'); if(u) u.hidden=(state!=='completed'); return; }
    if(id.indexOf('lp-')===0){ var cb=document.getElementById(id); var on=cb?cb.checked:false; state=on?'completed':(state==='completed'?'':state); }
    // shipped (live-verified) cards never move; everything else is placed by state
    if(live){ c.hidden=false; c.classList.add('ship'); setStep(c,0,'done'); setStep(c,1,'done'); setStep(c,2,'done'); done++; return; }
    if(promo && !(state==='promoted'||state==='active'||state==='completed'||state==='deferred'||state==='dismissed')){ c.hidden=true; return; }
    c.hidden=false;
    if(state==='completed'){ place(c,V); ver++; setStep(c,0,'done'); c.classList.remove('active'); }
    else if(state==='deferred'||state==='dismissed'){ place(c,P); park++; c.classList.remove('active'); c.querySelector('.rank').textContent=state==='deferred'?'⏸':'✕'; }
    else { place(c,Q); c.classList.toggle('active', state==='active'); setStep(c,0,state==='active'?'now':''); open.push(c); }
    if(site && c.dataset.site!==site && !live){ c.hidden=true; }
    // buttons reflect state
    var b;
    if(b=c.querySelector('.t-start')) b.hidden=(state==='active'||state==='completed');
    if(b=c.querySelector('.t-done')) b.hidden=(state==='completed');
    if(b=c.querySelector('.t-defer')) b.hidden=(state==='deferred'||state==='completed');
    if(b=c.querySelector('.t-dismiss')) b.hidden=(state==='dismissed'||state==='completed');
    if(b=c.querySelector('.t-undo')) b.hidden=!(state==='completed'||state==='deferred'||state==='dismissed'||state==='active'||(promo&&state==='promoted'));
    if(b=c.querySelector('.t-undo')) b.textContent=state==='completed'?'Undo complete':state==='active'?'Pause':(promo&&state==='promoted')?'Back to Monitor':'Restore to queue';
  });
  // contiguous ranks 1..N in DOM order (= priority order), only for visible open cards
  open.sort(function(a,b){ return (+b.dataset.score)-(+a.dataset.score); });
  open.forEach(function(c){ Q.appendChild(c); });
  var n=0; open.forEach(function(c){ if(c.hidden) return; n++; c.querySelector('.rank').textContent=n; mins+=parseInt(c.dataset.min,10)||0; });
  var vh=document.getElementById('ver-head'); if(vh) vh.hidden=!ver;
  var ph=document.getElementById('park-head'); if(ph) ph.hidden=!park;
  var shipToday=0; S.querySelectorAll('article.task').forEach(function(c){ if(!c.hidden) shipToday++; });
  var needsN=0; document.querySelectorAll('#needs article.task').forEach(function(c){ if(!c.classList.contains('done')) needsN++; });
  document.querySelectorAll('#nextlist .rrow[data-tid]').forEach(function(r){ var s=st[r.dataset.tid]||{}; var gone=(s.state==='promoted'||s.state==='active'||s.state==='completed'); r.hidden=gone; var b=r.querySelector('.t-promote'); if(b){ b.disabled=gone; b.textContent=gone?'On your list':'Add to Do now'; } });
  var monN=0; document.querySelectorAll('#monitor .rrow[data-tid]').forEach(function(r){ var s=st[r.dataset.tid]||{}; var gone=(s.state==='promoted'||s.state==='active'||s.state==='completed'); r.hidden=gone; if(!gone) monN++;
    var b=r.querySelector('.t-promote'); if(b){ b.disabled=gone; b.textContent=gone?'On your list':'Add to Do now'; } });
  function txt(id,v){ var el=document.getElementById(id); if(el) el.textContent=v; }
  txt('c-do',n); txt('l-do',n); txt('c-est',fmt(mins)); txt('c-ship',shipToday); txt('c-ver',ver); txt('c-needs',needsN); txt('l-needs',needsN); txt('c-mon',monN); txt('l-mon',monN);
  var tag=document.querySelector('.side nav a.on .navtag'); if(tag) tag.textContent=n;
  renderFocus();
 }
 function renderFocus(){
  var bar=document.getElementById('focusbar'); if(!bar) return;
  var fid=null; Object.keys(st).forEach(function(k){ if(st[k].state==='active') fid=k; });
  if(!fid){ bar.hidden=true; return; }
  var s=st[fid], steps=s.steps||[], done=(s.checked||[]).length;
  var mins=Math.max(0, Math.round((s.min||30)*(1-done/Math.max(1,steps.length))));
  var h='<div class="focus"><div class="fh"><b>Current focus:</b> '+s.title+'<span class="dim">'+done+' / '+steps.length+' steps · ≈'+mins+' min left</span></div>';
  steps.forEach(function(sp,i){ var ck=(s.checked||[]).indexOf(i)>=0; h+='<label><input type="checkbox" data-i="'+i+'" '+(ck?'checked':'')+'> <span'+(ck?' class="strike"':'')+'>'+sp+'</span></label>'; });
  h+='<div class="actions"><button class="act primary" id="focusdone">Mark complete</button><button class="act" id="focusstop">Pause</button></div></div>';
  bar.innerHTML=h; bar.hidden=false;
  bar.querySelectorAll('input[type=checkbox]').forEach(function(cb){ cb.addEventListener('change',function(){ var i=parseInt(cb.dataset.i,10); s.checked=s.checked||[]; var at=s.checked.indexOf(i); if(cb.checked&&at<0)s.checked.push(i); if(!cb.checked&&at>=0)s.checked.splice(at,1); st[fid]=s; save(st); renderFocus(); }); });
  var fd=document.getElementById('focusdone'); if(fd) fd.addEventListener('click',function(){ set(fid,'completed'); });
  var fs=document.getElementById('focusstop'); if(fs) fs.addEventListener('click',function(){ set(fid,'queued'); });
 }
 function set(id,state){
  var c=document.querySelector('article.task[data-tid="'+id+'"]'), cur=st[id]||{};
  if(c){ cur.title=c.dataset.title; cur.min=parseInt(c.dataset.min,10)||30; try{cur.steps=JSON.parse(c.dataset.steps||'[]');}catch(e){cur.steps=[];} }
  cur.prev=cur.state||'queued'; cur.state=state;
  if(state==='completed') cur.completed=TODAY; else delete cur.completed;
  if(state==='active'){ Object.keys(st).forEach(function(k){ if(st[k].state==='active'&&k!==id) st[k].state='queued'; }); }
  st[id]=cur; save(st);
  // ledger-driven ids: the checkbox is the truth, flip it first so apply() sees the new state
  if(id.indexOf('lp-')===0){ var cb=document.getElementById(id); if(cb&&cb.checked!==(state==='completed')){ cb.checked=(state==='completed'); cb.dispatchEvent(new Event('change')); } }
  apply();
 }
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('button'); if(!b) return;
  var card=b.closest('article.task'); var id=card?card.dataset.tid:null;
  if(b.classList.contains('chead')){ var o=card.classList.toggle('open'); b.setAttribute('aria-expanded',o?'true':'false'); return; }
  if(b.classList.contains('lane-btn')){ document.querySelectorAll('.lane-btn').forEach(function(x){x.setAttribute('aria-selected','false');}); b.setAttribute('aria-selected','true');
    ['do','needs','monitor','excluded'].forEach(function(k){ var p=document.getElementById('p-'+k); var on=k===b.dataset.panel; p.classList.toggle('active',on); p.hidden=!on; }); return; }
  if(b.classList.contains('t-promote')){ var tid=b.dataset.tid; var cur=st[tid]||{}; var pc=document.querySelector('article.task[data-tid="'+tid+'"]'); if(pc){ cur.title=pc.dataset.title; cur.min=parseInt(pc.dataset.min,10)||30; try{cur.steps=JSON.parse(pc.dataset.steps||'[]');}catch(e){} } cur.state='promoted'; st[tid]=cur; save(st); apply();
    document.querySelector('.lane-btn[data-panel="do"]').click(); if(pc){ pc.scrollIntoView({behavior:'smooth',block:'center'}); } return; }
  if(!id) return;
  if(b.classList.contains('t-start')){ set(id,'active'); window.scrollTo({top:0,behavior:'smooth'}); }
  else if(b.classList.contains('t-done')){ var inp=card.querySelector('.t-url'); if(inp&&inp.value.trim()){ var cu=st[id]||{}; cu.url=inp.value.trim(); st[id]=cu; try{localStorage.setItem('lpu:'+id,cu.url);}catch(e){} } set(id,'completed'); }
  else if(b.classList.contains('t-defer')) set(id,'deferred');
  else if(b.classList.contains('t-dismiss')) set(id,'dismissed');
  else if(b.classList.contains('t-undo')){ var s=st[id]||{}; var promo=card.dataset.promo==='1'; var back=promo?((s.state==='promoted')?'queued':'promoted'):'queued'; set(id,back); }
  else if(b.classList.contains('t-urlsave')){ var inp=card.querySelector('.t-url'); var cur=st[id]||{}; cur.url=(inp.value||'').trim(); cur.title=card.dataset.title; st[id]=cur; save(st);
    if(id.indexOf('lp-')===0){ try{localStorage.setItem('lpu:'+id,cur.url);}catch(e){} var cb=document.getElementById(id); if(cb&&cb.checked&&window.seoLinksPush) window.seoLinksPush(); }
    b.textContent='Saved ✓'; setTimeout(function(){b.textContent='Save';},1500); }
 });
 var sf=document.getElementById('sitefilter'); if(sf) sf.addEventListener('change',apply);
 document.addEventListener('change',function(ev){ if(ev.target&&ev.target.classList&&ev.target.classList.contains('lpx')) apply(); });
 function fillUrls(){ document.querySelectorAll('article.task .t-url').forEach(function(inp){ var id=inp.closest('article.task').dataset.tid; var u=(st[id]||{}).url||''; if(!u&&id.indexOf('lp-')===0){ try{u=localStorage.getItem('lpu:'+id)||'';}catch(e){} } if(u&&!inp.value) inp.value=u; }); }
 window.addEventListener('seo-state-sync',function(){ st=load(); apply(); fillUrls(); });
 window.addEventListener('seo-links-sync',function(){ apply(); fillUrls(); });
 fillUrls();
 apply();
})();
</script>"""
