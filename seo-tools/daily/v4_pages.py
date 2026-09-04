#!/usr/bin/env python3
"""v4 analytics pages: Overview, Performance, Rankings, Content, Technical,
Authority, Opportunities, Settings. Called from generate_v3.py at the end of a
build via build_all(globals()) so it shares the generator's loaded state.

Design contract (documented, no magic numbers on screen without a legend):
- All GSC comparisons are complete 28-day windows vs the previous 28 complete
  days (GSC lags ~2 days; ranges are printed in the UI).
- Ranking metrics are NEVER merged across indexes: strategic probes (DataForSEO
  SERP), DataForSEO top-100 and Semrush organic are labeled separately.
- Revenue is computed client-side from the sales app's localStorage on the same
  origin, labeled as TOTAL sales (not organic-attributed).
"""
import html as H
import json as J

# expected CTR by position — public-study heuristic, used only to rank
# opportunities, never displayed as a prediction. Documented in Settings.
def ectr(pos):
    curve = {1: .28, 2: .15, 3: .10, 4: .07, 5: .055, 6: .045, 7: .037, 8: .031, 9: .026, 10: .023}
    if pos is None: return 0
    p = round(pos)
    if p in curve: return curve[p]
    if p <= 20: return .015
    return .008

def pct(cur, prev):
    if not prev: return None
    return 100.0 * (cur - prev) / prev

def dfmt(delta, unit="%", inv=False):
    if delta is None: return '<span class="flat">new</span>'
    cls = "up" if (delta > 0) != inv else ("down" if delta != 0 else "flat")
    arrow = "▲" if delta > 0 else ("▼" if delta < 0 else "·")
    return f'<span class="{cls}">{arrow} {abs(delta):.0f}{unit}</span>'

def build_all(G):
    OUT, ALL, ABBR, SLUG = G["OUT"], G["ALL"], G["ABBR"], G["SLUG"]
    KT, SEM, D, F, CT, HIST = G["KT"], G["SEM"], G["D"], G["F"], G["CT"], G["HIST"]
    GSCD, INDEX, DFS_DOWN = G["GSCD"], G["INDEX"], G["DFS_DOWN"]
    STAMP_TXT, SEM_UPD, POS_SRC = G["STAMP_TXT"], G["SEM_UPD"], G["POS_SRC"]
    MONEY, CTRY, LANG, NSITES = G["MONEY"], G["CTRY"], G["LANG"], G["NSITES"]
    icon, shell, spark, COPY_JS = G["icon"], G["shell"], G["spark"], G["COPY_JS"]
    dfs_of, daily_of, nrank = G["dfs_of"], G["daily_of"], G["nrank"]
    alerts, PREV, _sc = G["alerts"], G.get("PREV") or {}, G["_sc"]
    reserved_for = G["reserved_for"]
    import os
    e = H.escape

    GS = GSCD.get("sites", {}) if GSCD else {}
    R28 = (GSCD.get("ranges", {}) or {}).get("cur28", ["", ""])
    P28 = (GSCD.get("ranges", {}) or {}).get("prev28", ["", ""])
    range_note = f"{R28[0]} → {R28[1]} vs {P28[0]} → {P28[1]}" if R28[0] else "28d windows unavailable"

    def tot(dom, days="28", which="cur"):
        return ((GS.get(dom, {}).get("totals", {}) or {}).get(days, {}) or {}).get(which) or {}

    def port_tot(days="28", which="cur"):
        c = i = 0; pw = 0.0
        for s in ALL:
            t = tot(s, days, which)
            c += t.get("clicks", 0); i += t.get("impressions", 0)
            if t.get("position") is not None and t.get("impressions"):
                pw += t["position"] * t["impressions"]
        pos = (pw / i) if i else None
        return {"clicks": c, "impressions": i, "ctr": (c / i if i else 0), "position": pos}

    cur = port_tot(); prev = port_tot(which="prev")

    # portfolio daily series (union of per-site GSC daily arrays already loaded in D)
    from collections import defaultdict
    daily_c = defaultdict(int); daily_i = defaultdict(int)
    for s in ALL:
        for x in daily_of(s):
            daily_c[x["date"]] += x["clicks"]; daily_i[x["date"]] += x["impressions"]
    days_sorted = sorted(daily_c)[-90:]
    series = [{"d": d, "c": daily_c[d], "i": daily_i[d]} for d in days_sorted]

    top10_now = sum(1 for s in ALL for r in KT.get(s, []) if r.get("pos") and r["pos"] <= 10)
    prev_pos = {(s, k): v for s in ALL
                for k, v in (PREV.get("sites", {}).get(s, {}).get("positions", {}) or {}).items()}
    top10_prev = sum(1 for (s, k), v in prev_pos.items() if v and v <= 10)

    def _earns_clicks(dom, path):
        pc = (GS.get(dom, {}).get("pages", {}) or {}).get("cur", {})
        for u, vv in pc.items():
            up = "/" + u.replace("https://", "").split("/", 1)[1] if "/" in u.replace("https://", "") else "/"
            if up.rstrip("/") == path.rstrip("/") and vv.get("clicks", 0) > 0:
                return True
        return False
    insp_all = []
    for s, rr in (INDEX.get("sites", {}) or {}).items():
        for p, v in rr.items():
            v = dict(v)
            if v.get("verdict") not in (None, "PASS") and _earns_clicks(s, p):
                # URL Inspection says not indexed, but GSC performance shows real clicks on
                # this URL — real users beat the anomalous verdict (verified-facts rule).
                v["verdict"] = "PASS"; v["state"] = "earning clicks (inspection verdict anomalous)"
            insp_all.append((s, p, v))
    insp_pass = [x for x in insp_all if x[2].get("verdict") == "PASS"]
    insp_fail = [x for x in insp_all if x[2].get("verdict") and x[2].get("verdict") != "PASS"]

    defects = sum(len(F.get(s, {}).get(k, []) or []) for s in ALL
                  for k in ("titles_over60", "redirect_links", "orphans", "canonical_mismatch")) \
        + sum(1 for s in ALL if F.get(s, {}).get("linked404"))

    # ---------- shared JS ----------
    CHART_JS = """<script>
(function(){
 document.querySelectorAll('.chart[data-series]').forEach(function(ch){
  var data=JSON.parse(ch.dataset.series), svg=ch.querySelector('svg'), tip=ch.querySelector('.htip'),
      line=ch.querySelector('.hoverline');
  if(!svg) return;
  ch.addEventListener('mousemove',function(ev){
    var r=svg.getBoundingClientRect(), x=(ev.clientX-r.left)/r.width;
    var i=Math.min(data.length-1,Math.max(0,Math.round(x*(data.length-1))));
    var d=data[i]; if(!d) return;
    line.style.display='block'; line.style.left=(x*100)+'%';
    tip.style.display='block';
    tip.style.left=Math.min(r.width-150,Math.max(0,ev.clientX-r.left+10))+'px'; tip.style.top='6px';
    tip.innerHTML='<b>'+d.d+'</b><br>'+d.c.toLocaleString()+' clicks · '+d.i.toLocaleString()+' impressions';
  });
  ch.addEventListener('mouseleave',function(){tip.style.display='none';line.style.display='none';});
 });
})();
</script>"""

    TABLE_JS = """<script>
(function(){
 // filter pills: buttons with data-filter toggle rows carrying data-f flags
 document.querySelectorAll('[data-filterbar]').forEach(function(bar){
  var table=document.getElementById(bar.dataset.filterbar); if(!table) return;
  bar.querySelectorAll('.fpill').forEach(function(b){
   b.addEventListener('click',function(){
    bar.querySelectorAll('.fpill').forEach(function(x){x.classList.remove('on');});
    b.classList.add('on');
    var f=b.dataset.filter;
    table.querySelectorAll('tbody tr').forEach(function(tr){
      tr.style.display=(f==='all'||(tr.dataset.f||'').split(' ').indexOf(f)>=0)?'':'none';
    });
   });
  });
 });
 // sortable headers
 document.querySelectorAll('th.sortable').forEach(function(th){
  th.addEventListener('click',function(){
   var table=th.closest('table'), tb=table.querySelector('tbody');
   var idx=Array.prototype.indexOf.call(th.parentNode.children,th);
   var dir=th.dataset.dir==='asc'?'desc':'asc'; th.dataset.dir=dir;
   var rows=Array.prototype.slice.call(tb.querySelectorAll('tr'));
   rows.sort(function(a,b){
    var av=a.children[idx].dataset.v!==undefined?parseFloat(a.children[idx].dataset.v):a.children[idx].textContent.trim();
    var bv=b.children[idx].dataset.v!==undefined?parseFloat(b.children[idx].dataset.v):b.children[idx].textContent.trim();
    if(typeof av==='number'&&!isNaN(av)&&typeof bv==='number'&&!isNaN(bv)) return dir==='asc'?av-bv:bv-av;
    return dir==='asc'?String(av).localeCompare(String(bv)):String(bv).localeCompare(String(av));
   });
   rows.forEach(function(r){tb.appendChild(r);});
  });
 });
})();
</script>"""

    SALES_JS = """<script>
(function(){
 var el=document.getElementById('kpi-revenue'), el2=document.getElementById('kpi-sales');
 if(!el) return;
 var raw=null; try{ raw=localStorage.getItem('iptv_sales_v1'); }catch(e){}
 if(!raw){ return; } // server-rendered 'no data on this device' state stays
 var sales=[]; try{ var j=JSON.parse(raw); sales=Array.isArray(j)?j:(j.sales||j.items||[]); }catch(e){ return; }
 if(!sales.length) return;
 var now=new Date(), cut=new Date(now-28*864e5), cut2=new Date(now-56*864e5);
 function dt(s){ return new Date(s.date||s.start||s.created||s.paid_date||0); }
 function eur(n){ return '\\u20ac'+Math.round(n).toLocaleString(); }
 var rev=0,revP=0,n28=0,nP=0;
 sales.forEach(function(s){
   var p=parseFloat(s.price)||0, d=dt(s);
   if(d>=cut){ rev+=p; n28++; } else if(d>=cut2){ revP+=p; nP++; }
 });
 var total=sales.reduce(function(a,s){return a+(parseFloat(s.price)||0);},0);
 el.querySelector('.kv').textContent=eur(rev);
 el.querySelector('.kd').innerHTML=(revP?((rev>=revP?'<span class=up>\\u25b2 ':'<span class=down>\\u25bc ')+Math.abs(Math.round(100*(rev-revP)/revP))+'%</span> vs prior 28d · '):'')+eur(total)+' all-time';
 if(el2){ el2.querySelector('.kv').textContent=n28;
   el2.querySelector('.kd').innerHTML=nP?((n28>=nP?'<span class=up>\\u25b2 ':'<span class=down>\\u25bc ')+Math.abs(n28-nP)+'</span> vs prior 28d'):'all channels'; }
})();
</script>"""

    PERIOD_JS = """<script>
(function(){
 var ch=document.querySelector('.chart[data-series]'); if(!ch) return;
 var all=JSON.parse(ch.dataset.series);
 document.querySelectorAll('.seg[data-period] button').forEach(function(b){
  b.addEventListener('click',function(){
   document.querySelectorAll('.seg[data-period] button').forEach(function(x){x.classList.remove('on');});
   b.classList.add('on');
   var n=parseInt(b.dataset.n,10), data=all.slice(-n);
   ch.dataset.series=JSON.stringify(data);
   redraw(ch,data);
  });
 });
 function redraw(ch,data){
  var svg=ch.querySelector('svg'); if(!svg||!data.length) return;
  var W=1000,Hh=200,pad=6;
  var mc=Math.max.apply(null,data.map(function(d){return d.c;}))||1;
  var mi=Math.max.apply(null,data.map(function(d){return d.i;}))||1;
  function pts(key,mx){ return data.map(function(d,i){
    var x=pad+i*(W-2*pad)/Math.max(1,data.length-1), y=Hh-pad-(d[key]/mx)*(Hh-2*pad);
    return x.toFixed(1)+','+y.toFixed(1); }).join(' ');
  }
  var pl=svg.querySelectorAll('polyline');
  if(pl[0]) pl[0].setAttribute('points',pts('i',mi));
  if(pl[1]) pl[1].setAttribute('points',pts('c',mc));
 }
})();
</script>"""

    # ---------- helpers ----------
    def kpi(label, value, delta_html, src, spark_html="", vid=""):
        idattr = f' id="{vid}"' if vid else ""
        sp_html = f'<div class="kspark">{spark_html}</div>' if spark_html else ""
        return (f'<div class="kpi"{idattr}><span class="kl">{label}</span>'
                f'<span class="kv">{value}</span><span class="kd">{delta_html}</span>'
                f'{sp_html}'
                f'<span class="src">i<span class="tip">{e(src)}</span></span></div>')

    def big_chart():
        if not series:
            return '<div class="empty"><b>No GSC daily data.</b> Traffic series appears after the first audit with Search Console connected.</div>'
        W, Hh, pad = 1000, 200, 6
        mc = max((d["c"] for d in series), default=1) or 1
        mi = max((d["i"] for d in series), default=1) or 1
        def pts(key, mx):
            n = max(1, len(series) - 1)
            return " ".join(f'{pad + i*(W-2*pad)/n:.1f},{Hh-pad-(d[key]/mx)*(Hh-2*pad):.1f}'
                            for i, d in enumerate(series))
        return (f'<div class="chart" data-series=\'{J.dumps(series)}\'>'
                f'<svg viewBox="0 0 {W} {Hh}" width="100%" height="200" preserveAspectRatio="none">'
                f'<polyline points="{pts("i", mi)}" fill="none" stroke="#c7d2fe" stroke-width="1.5"/>'
                f'<polyline points="{pts("c", mc)}" fill="none" stroke="#4f46e5" stroke-width="2"/>'
                f'</svg><div class="hoverline"></div><div class="htip"></div></div>'
                f'<div class="legend"><span><i style="background:#4f46e5"></i>Clicks (left-scaled)</span>'
                f'<span><i style="background:#c7d2fe"></i>Impressions (own scale)</span>'
                f'<span class="stmeta">Each series is scaled to its own max — read shape, not cross-height.</span></div>')

    # ---------- WHAT CHANGED ----------
    def what_changed():
        items = []
        for s in ALL:
            tc, tp = tot(s), tot(s, "28", "prev")
            c, p = tc.get("clicks", 0), tp.get("clicks", 0)
            if max(c, p) >= 15 and p and abs(pct(c, p)) >= 15:
                pg_cur = GS.get(s, {}).get("pages", {}).get("cur", {})
                pg_prev = GS.get(s, {}).get("pages", {}).get("prev", {})
                deltas = []
                for u in set(pg_cur) | set(pg_prev):
                    dd = pg_cur.get(u, {}).get("clicks", 0) - pg_prev.get(u, {}).get("clicks", 0)
                    if dd: deltas.append((dd, u))
                deltas.sort(key=lambda x: abs(x[0]), reverse=True)
                topu = deltas[0] if deltas else None
                d = pct(c, p)
                path = topu[1].split(CANON_HOST(s))[-1] if topu else ""
                mag_txt = f'{abs(d):.0f}%' if p >= 10 else f'{abs(c-p)} '
                items.append(dict(kind="good" if d > 0 else "bad",
                    text=f'{ABBR[s]} {"gained" if d>0 else "lost"} {mag_txt} organic clicks ({p} → {c}, 28d vs previous 28d).',
                    meta=(f'largest contributor: {path} ({topu[0]:+d} clicks)' if topu else ""),
                    hypo="", site=s, mag=abs(d)))
            # CTR shift with impressions up
            ic_, ip_ = tc.get("impressions", 0), tp.get("impressions", 0)
            ctr_c = (c / ic_) if ic_ else 0; ctr_p = (p / ip_) if ip_ else 0
            if ip_ >= 300 and ic_ > ip_ * 1.1 and ctr_p > 0 and ctr_c < ctr_p * 0.65:
                items.append(dict(kind="bad",
                    text=f'{ABBR[s]}: CTR fell {100*ctr_p:.1f}% → {100*ctr_c:.1f}% while impressions grew {ip_:,} → {ic_:,}.',
                    meta="", hypo="Hypothesis: new lower-position impressions dilute CTR — check the query table before editing titles.",
                    site=s, mag=25))
            # queries entering top 10
            qc = GS.get(s, {}).get("queries", {}).get("cur", {})
            qp = GS.get(s, {}).get("queries", {}).get("prev", {})
            entered = [q for q, v in qc.items() if v["position"] <= 10 and v["impressions"] >= 5
                       and (q not in qp or qp[q]["position"] > 10)]
            if len(entered) >= 2:
                ex = ", ".join(f'“{q}”' for q in entered[:3])
                items.append(dict(kind="good",
                    text=f'{ABBR[s]}: {len(entered)} queries entered positions 1–10 ({ex}{"…" if len(entered)>3 else ""}).',
                    meta="", hypo="", site=s, mag=10 + len(entered)))
        # strategic movers vs snapshot
        for s in ALL:
            for r in KT.get(s, []):
                op = prev_pos.get((s, r["kw"]))
                np_ = r.get("pos")
                if op and np_ and abs(op - np_) >= 3 and min(op, np_) <= 20:
                    good = np_ < op
                    items.append(dict(kind="good" if good else "bad",
                        text=f'{ABBR[s]}: strategic “{r["kw"]}” moved #{op} → #{np_} (live probe).',
                        meta=f'target page {r.get("page") or "—"}', hypo="", site=s, mag=abs(op-np_)+5))
        # authority velocity (DFS, our own history)
        if len(HIST) >= 2:
            for s in ALL:
                h = [x["sites"].get(s, {}).get("ref_domains") for x in HIST[-7:] if s in x.get("sites", {})]
                h = [x for x in h if x is not None]
                if len(h) >= 2 and abs(h[-1] - h[0]) >= 3:
                    d = h[-1] - h[0]
                    items.append(dict(kind="good" if d > 0 else "bad",
                        text=f'{ABBR[s]}: {abs(d)} referring domains {"gained" if d>0 else "lost"} over the last audits (DataForSEO {h[0]} → {h[-1]}).',
                        meta="", hypo="" if d > 0 else "Hypothesis: expired placements — review the lost links before replacing them.",
                        site=s, mag=abs(d)))
        # indexation problems
        for s, p, v in insp_fail:
            items.append(dict(kind="bad", text=f'{ABBR[s]}: priority page {p} is not indexed ({v.get("state") or v.get("detail")}).',
                              meta="GSC URL Inspection", hypo="", site=s, mag=30))
        items.sort(key=lambda x: -x["mag"])
        return items[:10]

    def CANON_HOST(s):
        return s

    changes = what_changed()

    # ---------- severity alerts ----------
    def sev_alerts():
        raw = alerts()
        out = []
        for lvl, txt in raw:
            if lvl == "good": continue
            sev = "critical" if lvl == "crit" else ("high" if any(
                w in txt.lower() for w in ("fell out", "not indexed", "lost", "dropped")) else "medium")
            out.append((sev, txt))
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        out.sort(key=lambda x: order[x[0]])
        return out[:7]

    SEVS = sev_alerts()

    # ---------- OPPORTUNITIES ----------
    INTENT_WORDS = ("abonnement", "abonament", "suscrip", "prix", "acheter", "comprar", "kopen",
                    "test", "essai", "premium", "iptv polska", "smarters", "boitier", "subscription")
    def vol_of(s, q):
        for r in KT.get(s, []):
            if r["kw"] == q: return r.get("vol")
        return None

    def opportunities():
        opps = []
        for s in ALL:
            qc = GS.get(s, {}).get("queries", {}).get("cur", {})
            pg_cur = GS.get(s, {}).get("pages", {}).get("cur", {})
            pg_prev = GS.get(s, {}).get("pages", {}).get("prev", {})
            phase_bonus = 10 if s in ("iptvesp.com", "primeiptv-france.com") else 5
            for q, v in qc.items():
                pos, imp, ctr = v["position"], v["impressions"], v["ctr"]
                intent = any(w in q for w in INTENT_WORDS)
                strat = any(r["kw"] == q for r in KT.get(s, []))
                if 4 <= pos <= 20 and imp >= 10:
                    upside = max(0, (ectr(3) - ctr)) * imp
                    score = min(30, imp // 10) + max(0, 25 - int(pos)) + (20 if intent else 8) \
                        + min(15, int(upside / 5)) + phase_bonus + (5 if strat else 0)
                    opps.append(dict(kind="Striking distance", score=score, site=s, query=q, page="",
                        what=f'“{q}” sits at position {pos:.0f} with {imp:,} impressions/28d.',
                        why="Positions 4–20 are the cheapest wins: the page already ranks, Google already tests it.",
                        upside=f'≈{upside:.0f} extra clicks/28d if it reaches the top 3 (expected-CTR heuristic).',
                        action="Strengthen internal links to the ranking page and refresh the content section matching this query.",
                        src="GSC query data, last 28 complete days"))
                if pos <= 10 and imp >= 50 and ectr(pos) > 0 and ctr < 0.6 * ectr(pos):
                    upside = (ectr(pos) - ctr) * imp
                    score = min(30, imp // 20) + 15 + (20 if intent else 8) + min(15, int(upside / 5)) + phase_bonus
                    opps.append(dict(kind="CTR gap", score=score, site=s, query=q, page="",
                        what=f'“{q}”: position {pos:.0f}, {imp:,} impressions, but CTR {100*ctr:.1f}% vs ≈{100*ectr(pos):.0f}% expected.',
                        why="The ranking is earned but the snippet does not win the click.",
                        upside=f'≈{upside:.0f} clicks/28d at expected CTR.',
                        action="Rewrite title/meta for this query (keep the keyword first, add the differentiator: price, test 24h, 4K).",
                        src="GSC query data + public CTR-by-position heuristic"))
            for r in CT.get(s, {}).get("recommend", []):
                if not r["covered"] and reserved_for(s, r["kw"]) and (r["vol"] or 0) >= 100:
                    score = min(30, (r["vol"] or 0) // 100) + 10 + 15 + phase_bonus
                    opps.append(dict(kind="Content gap", score=score, site=s, query=r["kw"], page="",
                        what=f'“{r["kw"]}” ({r["vol"]:,}/mo) has no page anywhere in this market.',
                        why="Uncontested demand inside this site's lane.",
                        upside="A new article can own the query without cannibalizing a sibling.",
                        action="Write it via the 5-skill pipeline (prompt ready on the Work page).",
                        src="DataForSEO volumes + portfolio coverage engine"))
            for u in set(pg_prev):
                pc = pg_cur.get(u, {}).get("clicks", 0); pp = pg_prev[u].get("clicks", 0)
                if pp >= 15 and pc <= pp * 0.6:
                    path = "/" + u.split("/", 3)[-1] if u.count("/") >= 3 else u
                    score = min(30, pp // 3) + 12 + phase_bonus
                    opps.append(dict(kind="Content decay", score=score, site=s, query="", page=path,
                        what=f'{path} lost {pp-pc} clicks ({pp} → {pc}, 28d vs previous).',
                        why="Decaying content keeps sliding unless refreshed; recovering an old ranking is cheaper than earning a new one.",
                        upside=f'Recovering to the prior period restores ≈{pp-pc} clicks/28d.',
                        action="Refresh the article: update facts/year, add a missing section for its top queries, re-run onpage-optimizer.",
                        src="GSC page data, 28d vs previous 28d"))
            sm = SEM.get(s) or {}
            for r in KT.get(s, []):
                if r.get("page") in (MONEY.get(s), "/") and (r.get("pos") is None or r["pos"] > 20) \
                        and (sm.get("ref_domains") or 0) < 20 and (r.get("vol") or 0) >= 200:
                    score = min(30, (r.get("vol") or 0) // 100) + 8 + 20 + phase_bonus
                    opps.append(dict(kind="Authority gap", score=score, site=s, query=r["kw"], page=r.get("page") or "",
                        what=f'Money target “{r["kw"]}” ({r.get("vol") or 0:,}/mo) is ' + ("unranked" if not r.get("pos") else "at #%d" % r["pos"]) + f' and the site has only {sm.get("ref_domains") or "0"} referring domains (Semrush).',
                        why="Commercial head terms follow authority; content alone will not close this gap.",
                        upside="Every quality referring domain moves the whole domain, not just this page.",
                        action="Point the next outreach/link batch at this site; internal links from every related article to the money page.",
                        src="Strategic targets + Semrush authority"))
        for s, p, v in insp_fail:
            opps.append(dict(kind="Indexation", score=70, site=s, query="", page=p,
                what=f'Priority page {p} is not indexed ({v.get("state") or v.get("detail")}).',
                why="An unindexed money/target page earns exactly zero organic clicks.",
                upside="Full recovery of the page's potential.",
                action="Request indexing in GSC, check canonical/robots, add 2–3 internal links from indexed pages.",
                src="GSC URL Inspection API"))
        best = {}
        for o in opps:
            k = (o["site"], o["kind"], o["query"] or o["page"])
            if k not in best or o["score"] > best[k]["score"]: best[k] = o
        return sorted(best.values(), key=lambda x: -x["score"])

    OPPS = opportunities()

    def opp_card(o):
        i = ALL.index(o["site"]) + 1
        qh = f'<span>query: {e(o["query"])}</span>' if o["query"] else ""
        ph = f'<span>page: {e(o["page"])}</span>' if o["page"] else ""
        return (f'<div class="opp"><div class="ohead"><span class="score num">{o["score"]}</span>'
                f'<span class="tag acc">{e(o["kind"])}</span>'
                f'<a href="{SLUG[o["site"]]}" style="font-weight:600">{e(ABBR[o["site"]])}</a>'
                f'<span class="dot s{i}"></span></div>'
                f'<div class="orow"><b>What:</b> {e(o["what"])}</div>'
                f'<div class="orow"><b>Why it matters:</b> {e(o["why"])}</div>'
                f'<div class="orow"><b>Expected upside:</b> {e(o["upside"])}</div>'
                f'<div class="orow"><b>Action:</b> {e(o["action"])}</div>'
                f'<div class="ofoot">{qh}{ph}'
                f'<span>source: {e(o["src"])}</span></div></div>')

    # ---------- OVERVIEW ----------
    def build_overview():
        dc = pct(cur["clicks"], prev["clicks"])
        di = pct(cur["impressions"], prev["impressions"])
        dctr = (cur["ctr"] - prev["ctr"]) * 100 if prev["impressions"] else None
        dpos = (prev["position"] - cur["position"]) if (cur["position"] and prev["position"]) else None
        clk_spark = spark([d["c"] for d in series[-45:]], w=130, h=26, color="var(--acc)") if series else ""
        kpis = (
            kpi("Revenue · 28d", "—",
                '<span class="flat">open /sales on this device to load</span>',
                "TOTAL sales revenue from the sales app (localStorage, this device). NOT organic-attributed — no analytics layer exists on the sites yet.", vid="kpi-revenue")
            + kpi("Sales · 28d", "—", '<span class="flat">sales app data</span>',
                  "Count of sales recorded in the sales app in the last 28 days. All channels, not organic-only.", vid="kpi-sales")
            + kpi("Organic clicks · 28d", f'{cur["clicks"]:,}', dfmt(dc) + ' <span class="stmeta">vs prev 28d</span>',
                  f"Google Search Console, all {NSITES} properties, complete days {range_note}.", clk_spark)
            + kpi("Impressions · 28d", f'{cur["impressions"]:,}', dfmt(di) + ' <span class="stmeta">vs prev 28d</span>',
                  "GSC impressions, same complete 28-day windows.")
            + kpi("CTR · 28d", f'{100*cur["ctr"]:.1f}%',
                  (dfmt(dctr, unit=" pts") if dctr is not None else '<span class="flat">—</span>') + ' <span class="stmeta">vs prev</span>',
                  "Portfolio clicks ÷ impressions (GSC). Compare trend, not absolute level — query mix differs per site.")
            + kpi("Avg position", f'{cur["position"]:.1f}' if cur["position"] else "—",
                  (dfmt(dpos, unit="") if dpos is not None else '<span class="flat">—</span>') + ' <span class="stmeta">impr-weighted</span>',
                  "GSC average position weighted by impressions across all sites. Lower is better; the delta arrow already accounts for that.")
            + kpi("Top-10 strategic", str(top10_now), dfmt(top10_now - top10_prev, unit="") + ' <span class="stmeta">vs last audit</span>',
                  f"Strategic tracked keywords (our {sum(len(v) for v in KT.values())}-target list) at position ≤10 in live DataForSEO probes. Not the same as Semrush/DFS totals — see Rankings.")
            + kpi("Indexation", f'{len(insp_pass)}/{len(insp_all)}' if insp_all else "—",
                  (f'<span class="{"up" if not insp_fail else "down"}">{len(insp_fail)} failing</span>' if insp_all else '<span class="flat">no inspection data</span>'),
                  "Priority URLs (money + strategic target pages) checked via the GSC URL Inspection API this audit.")
        )
        ch_parts = []
        for c in changes:
            ico = "▲" if c["kind"] == "good" else ("▼" if c["kind"] == "bad" else "·")
            meta_h = f'<div class="cmeta">{e(c["meta"])}</div>' if c["meta"] else ""
            hypo_h = f'<div class="hypo">{e(c["hypo"])}</div>' if c["hypo"] else ""
            ch_parts.append(f'<div class="chg {c["kind"]}"><span class="cico">{ico}</span>'
                            f'<div class="cbody">{e(c["text"])}{meta_h}{hypo_h}</div></div>')
        ch = "".join(ch_parts) or '<div class="empty">No meaningful changes detected between the last two 28-day windows.</div>'
        al = "".join(f'<div class="alertrow"><span class="sev {s_}">{s_.upper()}</span><span>{e(t)}</span></div>'
                     for s_, t in SEVS) or '<div class="empty"><b>No open alerts.</b> All monitored rules are quiet.</div>'
        opp_top = "".join(opp_card(o) for o in OPPS[:4])
        srows = ""
        for i, s in enumerate(ALL):
            t, tp = tot(s), tot(s, "28", "prev")
            d = pct(t.get("clicks", 0), tp.get("clicks", 0))
            sm = SEM.get(s) or {}
            n10 = sum(1 for r in KT.get(s, []) if r.get("pos") and r["pos"] <= 10)
            gsc_ok = GS.get(s, {}).get("in_gsc")
            srows += (f'<tr><td><a href="{SLUG[s]}"><span class="dot s{i+1}"></span> {ABBR[s]}</a></td>'
                      f'<td>{e(CTRY[s][1])}</td>'
                      + (f'<td data-v="{t.get("clicks",0)}">{t.get("clicks",0):,}</td><td>{dfmt(d)}</td>'
                         if gsc_ok else '<td colspan="2"><span class="tag warn">awaiting GSC</span></td>')
                      + f'<td data-v="{n10}">{n10}</td>'
                      f'<td data-v="{sm.get("ref_domains") or 0}">{sm.get("ref_domains") if sm.get("ref_domains") is not None else "—"}</td>'
                      f'<td><span class="badge b-{_sc.CONFIG[s]["tone"]}">{_sc.CONFIG[s]["status"]}</span></td></tr>')
        return (f'<div class="pagehead"><h1>Overview</h1><p class="sub">Executive view · complete 28-day GSC windows ({range_note}) · audit {e(STAMP_TXT)}</p></div>'
                f'<div class="kpirow">{kpis}</div>'
                f'<div class="grid g23"><div class="card"><div class="chead"><h2>Organic traffic — 90 days</h2>'
                f'<div class="seg" data-period><button data-n="7">7d</button><button data-n="28">28d</button>'
                f'<button class="on" data-n="90">90d</button></div></div>{big_chart()}</div>'
                f'<div class="card"><div class="chead"><h2>Alerts</h2><a class="btn sm" href="settings">rules</a></div>{al}</div></div>'
                f'<div class="grid g23"><div class="card"><div class="chead"><h2>What changed</h2>'
                f'<span class="stmeta">28d vs previous 28d · live probes · audit history</span></div>{ch}</div>'
                f'<div class="card"><div class="chead"><h2>Top opportunities</h2>'
                f'<a class="btn sm" href="opportunities">all {len(OPPS)}</a></div><div class="stack" style="gap:10px">{opp_top}</div></div></div>'
                f'<div class="card flush"><div class="chead"><h2>Websites</h2><span class="stmeta">clicks = GSC 28d complete</span></div>'
                f'<div class="overflow"><table><thead><tr><th>site</th><th>market</th><th class="sortable">clicks 28d</th>'
                f'<th>Δ</th><th class="sortable">top-10 strategic</th><th class="sortable">ref.dom (Semrush)</th><th>phase</th></tr></thead>'
                f'<tbody>{srows}</tbody></table></div></div>')

    # ---------- PERFORMANCE ----------
    def build_performance():
        qrows = []
        for s in ALL:
            qc = GS.get(s, {}).get("queries", {}).get("cur", {})
            qp = GS.get(s, {}).get("queries", {}).get("prev", {})
            for q, v in qc.items():
                pv = qp.get(q)
                dclk = v["clicks"] - (pv["clicks"] if pv else 0)
                dimp = v["impressions"] - (pv["impressions"] if pv else 0)
                dposq = (pv["position"] - v["position"]) if pv else None
                strat = any(r["kw"] == q for r in KT.get(s, []))
                flags = []
                if pv is None: flags.append("new")
                if dclk > 0: flags.append("win")
                if dclk < 0: flags.append("lose")
                p = v["position"]
                flags.append("p13" if p <= 3 else "p410" if p <= 10 else "p1120" if p <= 20 else "p2150" if p <= 50 else "p51")
                if v["impressions"] >= 50 and ectr(p) and v["ctr"] < 0.6 * ectr(p): flags.append("lowctr")
                if strat: flags.append("strat")
                qrows.append((v["clicks"], q, s, v, dclk, dimp, dposq, strat, " ".join(flags), pv))
            for q, pv in qp.items():
                if q not in qc and pv["clicks"] >= 3:
                    qrows.append((0, q, s, {"clicks": 0, "impressions": 0, "ctr": 0, "position": None},
                                  -pv["clicks"], -pv["impressions"], None, False, "lost lose", pv))
        qrows.sort(key=lambda x: -(abs(x[4]) * 2 + x[0]))
        qhtml = ""
        for clk, q, s, v, dclk, dimp, dposq, strat, flags, pv in qrows[:400]:
            vol = vol_of(s, q)
            voltx = ("{:,}".format(vol)) if vol else "—"
            st_tag = ' <span class="tag acc">target</span>' if strat else ""
            postxt = ("%.1f" % v["position"]) if v["position"] else "—"
            qhtml += (f'<tr data-f="all {flags}"><td>{e(q)}{st_tag}</td>'
                      f'<td><a href="{SLUG[s]}">{ABBR[s]}</a></td>'
                      f'<td data-v="{v["clicks"]}">{v["clicks"]:,}</td>'
                      f'<td data-v="{v["impressions"]}">{v["impressions"]:,}</td>'
                      f'<td data-v="{v["ctr"]}">{100*v["ctr"]:.1f}%</td>'
                      f'<td data-v="{v["position"] or 999}">{postxt}</td>'
                      f'<td data-v="{dclk}">{dfmt(dclk, unit="") if dclk else "·"}</td>'
                      f'<td data-v="{dimp}">{dfmt(dimp, unit="") if dimp else "·"}</td>'
                      f'<td data-v="{dposq if dposq is not None else 0}">{dfmt(dposq, unit="") if dposq is not None else "·"}</td>'
                      f'<td data-v="{vol or 0}">{voltx}</td></tr>')
        fbar = ('<div class="fbar" data-filterbar="qtable">'
                + "".join(f'<button class="fpill{" on" if f=="all" else ""}" data-filter="{f}">{l}</button>'
                          for f, l in [("all", "All"), ("win", "Winners"), ("lose", "Losers"), ("new", "New"),
                                       ("lost", "Lost"), ("p13", "Pos 1–3"), ("p410", "Pos 4–10"),
                                       ("p1120", "Pos 11–20"), ("p2150", "Pos 21–50"),
                                       ("lowctr", "High impr / low CTR"), ("strat", "Strategic")])
                + '</div>')
        prow = []
        for s in ALL:
            pc = GS.get(s, {}).get("pages", {}).get("cur", {})
            pp = GS.get(s, {}).get("pages", {}).get("prev", {})
            qc = GS.get(s, {}).get("queries", {}).get("cur", {})
            for u, v in pc.items():
                path = u.replace("https://", "").replace("http://", "")
                path = "/" + path.split("/", 1)[1] if "/" in path else "/"
                pv = pp.get(u)
                dclk = v["clicks"] - (pv["clicks"] if pv else 0)
                dposq = (pv["position"] - v["position"]) if pv else None
                prow.append((v["clicks"], path, s, v, dclk, dposq))
        prow.sort(key=lambda x: -x[0])
        phtml = ""
        for clk, path, s, v, dclk, dposq in prow[:200]:
            pposx = ("%.1f" % v["position"]) if v["position"] else "—"
            phtml += (f'<tr><td class="mono" style="font-size:11.5px">{e(path[:70])}</td><td><a href="{SLUG[s]}">{ABBR[s]}</a></td>'
                      f'<td data-v="{v["clicks"]}">{v["clicks"]:,}</td><td data-v="{v["impressions"]}">{v["impressions"]:,}</td>'
                      f'<td>{100*v["ctr"]:.1f}%</td><td data-v="{v["position"] or 999}">{pposx}</td>'
                      f'<td data-v="{dclk}">{dfmt(dclk, unit="") if dclk else "·"}</td>'
                      f'<td data-v="{dposq if dposq is not None else 0}">{dfmt(dposq, unit="") if dposq is not None else "·"}</td></tr>')
        # device + country
        dev = {}; ctr_ = {}
        for s in ALL:
            for k, v in (GS.get(s, {}).get("device") or {}).items():
                dev[k] = dev.get(k, 0) + v["clicks"]
            for k, v in (GS.get(s, {}).get("country") or {}).items():
                ctr_[k] = ctr_.get(k, 0) + v["clicks"]
        mx = max(dev.values(), default=1) or 1
        dhtml = "".join(f'<div class="hbar"><span class="hlab">{e(k.title())}</span>'
                        f'<span class="htrack"><i style="width:{100*v/mx:.0f}%"></i></span>'
                        f'<span class="hval">{v:,}</span></div>' for k, v in sorted(dev.items(), key=lambda x: -x[1]))
        top_c = sorted(ctr_.items(), key=lambda x: -x[1])[:10]
        mxc = max((v for _, v in top_c), default=1) or 1
        chtml = "".join(f'<div class="hbar"><span class="hlab">{e(k.upper())}</span>'
                        f'<span class="htrack"><i style="width:{100*v/mxc:.0f}%"></i></span>'
                        f'<span class="hval">{v:,}</span></div>' for k, v in top_c)
        return (f'<div class="pagehead"><h1>Performance</h1><p class="sub">Search Console analytics · complete windows {range_note} · top 250 queries/pages per site</p></div>'
                f'<div class="card" style="margin-bottom:16px"><div class="chead"><h2>Traffic — 90 days, all sites</h2>'
                f'<div class="seg" data-period><button data-n="7">7d</button><button data-n="28">28d</button>'
                f'<button class="on" data-n="90">90d</button></div></div>{big_chart()}</div>'
                f'<div class="card flush" style="margin-bottom:16px"><div class="chead"><h2>Queries</h2>'
                f'<span class="stmeta">Δ columns = vs previous 28d · click a column header to sort</span></div>'
                f'<div style="padding:0 18px">{fbar}</div>'
                f'<div class="twrap"><table id="qtable"><thead><tr><th>query</th><th>site</th>'
                f'<th class="sortable">clicks</th><th class="sortable">impr</th><th class="sortable">ctr</th>'
                f'<th class="sortable">pos</th><th class="sortable">Δ clicks</th><th class="sortable">Δ impr</th>'
                f'<th class="sortable">Δ pos</th><th class="sortable">vol/mo</th></tr></thead><tbody>{qhtml}</tbody></table></div></div>'
                f'<div class="card flush" style="margin-bottom:16px"><div class="chead"><h2>Pages</h2>'
                f'<span class="stmeta">top pages by clicks, 28d</span></div>'
                f'<div class="twrap"><table><thead><tr><th>page</th><th>site</th><th class="sortable">clicks</th>'
                f'<th class="sortable">impr</th><th>ctr</th><th class="sortable">pos</th><th class="sortable">Δ clicks</th>'
                f'<th class="sortable">Δ pos</th></tr></thead><tbody>{phtml}</tbody></table></div></div>'
                f'<div class="grid g2"><div class="card"><h2>Devices</h2><p class="sub" style="margin-bottom:8px">clicks, 28d</p>{dhtml or "<div class=empty>No device data.</div>"}</div>'
                f'<div class="card"><h2>Countries</h2><p class="sub" style="margin-bottom:8px">clicks, 28d — diaspora shows up here</p>{chtml or "<div class=empty>No country data.</div>"}</div></div>')

    # ---------- RANKINGS ----------
    def build_rankings():
        rows = ""
        for s in ALL:
            qc = GS.get(s, {}).get("queries", {}).get("cur", {})
            for r in sorted(KT.get(s, []), key=lambda r: (r.get("pos") or 999)):
                op = prev_pos.get((s, r["kw"]))
                g = qc.get(r["kw"])
                p = r.get("pos")
                pill = (f'<span class="krank {"good" if p<=10 else "ok" if p<=30 else "far"}">#{p}</span>'
                        if p else '<span class="krank miss">not in top 100</span>')
                gpos = ("%.1f" % g["position"]) if g else "—"
                voltxt = ("{:,}".format(r["vol"])) if r.get("vol") else "—"
                rows += (f'<tr><td>{e(r["kw"])}</td><td><a href="{SLUG[s]}">{ABBR[s]}</a></td>'
                         f'<td data-v="{r.get("vol") or 0}">{voltxt}</td>'
                         f'<td data-v="{p or 999}">{pill}</td>'
                         f'<td>{dfmt((op-p) if op and p else None, unit="") if (op and p and op!=p) else "·"}</td>'
                         f'<td data-v="{g["position"] if g else 999}">{gpos}</td>'
                         f'<td class="mono" style="font-size:11px">{e(r.get("page") or "—")}</td></tr>')
        dfs_rows = ""
        for i, s in enumerate(ALL):
            hh = [x["sites"].get(s, {}).get("ranked_top100") for x in HIST if s in x.get("sites", {})]
            hh = [x for x in hh if x is not None]
            t100 = dfs_of(s).get("ranked_top100")
            sm = SEM.get(s) or {}
            dfs_rows += (f'<tr><td><span class="dot s{i+1}"></span> {ABBR[s]}</td>'
                         f'<td data-v="{t100 or 0}">{t100 if t100 is not None else "—"}</td>'
                         f'<td>{spark(hh, w=90, h=20, color="var(--acc)") if len(hh)>1 else "·"}</td>'
                         f'<td data-v="{sm.get("organic_keywords") or 0}">{sm.get("organic_keywords") if sm.get("organic_keywords") is not None else "—"}</td>'
                         f'<td>{e(sm.get("ok_delta") or "")}</td><td class="stmeta">{e(sm.get("date",""))}</td></tr>')
        return (f'<div class="pagehead"><h1>Rankings</h1><p class="sub">Three independent datasets — never merged. '
                f'When they disagree, each is shown with its own trend.</p></div>'
                f'<div class="card flush" style="margin-bottom:16px"><div class="chead"><h2>Strategic tracked keywords — {sum(len(v) for v in KT.values())}</h2>'
                f'<span class="stmeta">probe = DataForSEO live SERP ({e(POS_SRC)}) · GSC = real-user avg position, 28d</span></div>'
                f'<div class="twrap"><table><thead><tr><th>keyword</th><th>site</th><th class="sortable">vol/mo</th>'
                f'<th class="sortable">probe pos</th><th>Δ vs last audit</th><th class="sortable">GSC pos</th><th>target page</th></tr></thead>'
                f'<tbody>{rows}</tbody></table></div></div>'
                f'<div class="card flush"><div class="chead"><h2>Index footprints per site</h2>'
                f'<span class="stmeta">DataForSEO top-100 (live each audit) vs Semrush organic keywords (owner-verified index) — different crawlers, different counts, both real</span></div>'
                f'<div class="overflow"><table><thead><tr><th>site</th><th class="sortable">DFS top-100 kw</th><th>trend</th>'
                f'<th class="sortable">Semrush organic kw</th><th>note</th><th>Semrush date</th></tr></thead><tbody>{dfs_rows}</tbody></table></div></div>')

    # ---------- CONTENT ----------
    def build_content():
        winners, losers, decay = [], [], []
        for s in ALL:
            pc = GS.get(s, {}).get("pages", {}).get("cur", {})
            pp = GS.get(s, {}).get("pages", {}).get("prev", {})
            for u in set(pc) | set(pp):
                c = pc.get(u, {}).get("clicks", 0); p = pp.get(u, {}).get("clicks", 0)
                path = u.replace("https://", "")
                path = "/" + path.split("/", 1)[1] if "/" in path else "/"
                d = c - p
                if d >= 3: winners.append((d, path, s, p, c))
                if d <= -3: losers.append((d, path, s, p, c))
                if p >= 10 and c <= p * 0.6: decay.append((d, path, s, p, c))
        winners.sort(key=lambda x: -x[0]); losers.sort(key=lambda x: x[0]); decay.sort(key=lambda x: x[0])
        def plist(rows, empty):
            if not rows: return f'<div class="empty">{empty}</div>'
            return "".join(f'<div class="hbar"><span class="hlab" style="width:190px" title="{e(pa)}">{e(pa[:38])}</span>'
                           f'<span style="font-size:11px;color:var(--faint)">{ABBR[s_]}</span>'
                           f'<span class="hval" style="width:110px">{p} → {c} · {dfmt(d, unit="")}</span></div>'
                           for d, pa, s_, p, c in rows[:12])
        states = ""
        for i, s in enumerate(ALL):
            arts = CT.get(s, {}).get("articles", []) or []
            pc = GS.get(s, {}).get("pages", {}).get("cur", {})
            by_path = {}
            for u, v in pc.items():
                pt = u.replace("https://", "")
                pt = "/" + pt.split("/", 1)[1] if "/" in pt else "/"
                by_path[pt.rstrip("/") or "/"] = v
            n = {"clicks": 0, "impr": 0, "silent": 0}
            for a in arts:
                v = by_path.get((a.get("path") or "").rstrip("/") or "/")
                if v and v["clicks"] > 0: n["clicks"] += 1
                elif v and v["impressions"] > 0: n["impr"] += 1
                else: n["silent"] += 1
            total = max(1, len(arts))
            states += (f'<tr><td><span class="dot s{i+1}"></span> {ABBR[s]}</td><td data-v="{len(arts)}">{len(arts)}</td>'
                       f'<td data-v="{n["clicks"]}"><span class="tag pos">{n["clicks"]}</span></td>'
                       f'<td data-v="{n["impr"]}"><span class="tag neu">{n["impr"]}</span></td>'
                       f'<td data-v="{n["silent"]}"><span class="tag warn">{n["silent"]}</span></td>'
                       f'<td><div class="bar"><i style="width:{100*(n["clicks"]+n["impr"])/total:.0f}%"></i></div></td></tr>')
        return (f'<div class="pagehead"><h1>Content</h1><p class="sub">Page-level movement, 28d vs previous 28d · '
                f'article states from crawl + GSC page data</p></div>'
                f'<div class="grid g3"><div class="card"><h2>Winners</h2><p class="sub" style="margin-bottom:6px">clicks gained</p>{plist(winners, "No page gained ≥3 clicks vs the previous window.")}</div>'
                f'<div class="card"><h2>Losers</h2><p class="sub" style="margin-bottom:6px">clicks lost</p>{plist(losers, "No page lost ≥3 clicks. Good.")}</div>'
                f'<div class="card"><h2>Decay</h2><p class="sub" style="margin-bottom:6px">−40%+ from a ≥10-click base — refresh candidates</p>{plist(decay, "No decaying pages detected.")}</div></div>'
                f'<div class="card flush"><div class="chead"><h2>Article visibility states</h2>'
                f'<span class="stmeta">receiving clicks / impressions only / silent (no GSC rows, 28d). Publication-date tracking starts for new pages going forward — historical dates were never recorded, so they are not shown rather than guessed.</span></div>'
                f'<div class="overflow"><table><thead><tr><th>site</th><th class="sortable">articles</th>'
                f'<th class="sortable">clicks</th><th class="sortable">impressions only</th><th class="sortable">silent</th><th style="min-width:120px">visible share</th></tr></thead>'
                f'<tbody>{states}</tbody></table></div></div>')

    # ---------- TECHNICAL ----------
    def build_technical():
        cats = [("titles_over60", "Titles >60 chars"), ("redirect_links", "Internal redirect links"),
                ("orphans", "Orphan pages"), ("canonical_mismatch", "Canonical mismatch")]
        trows = ""
        for i, s in enumerate(ALL):
            f = F.get(s, {})
            checks = _sc._health(s, F)
            ok = sum(1 for _, o in checks if o)
            cells = "".join(f'<td data-v="{len(f.get(k, []) or [])}">{len(f.get(k, []) or []) or "·"}</td>' for k, _ in cats)
            www = f.get("apex") or f.get("www_redirect") or "—"
            l404 = "·" if not f.get("linked404") else '<span class="tag neg">%d</span>' % len(f["linked404"])
            wtag = '<span class="tag pos">308</span>' if str(www).startswith("308") else f'<span class="tag warn">{e(str(www)[:12])}</span>'
            trows += (f'<tr><td><a href="{SLUG[s]}"><span class="dot s{i+1}"></span> {ABBR[s]}</a></td>'
                      f'<td data-v="{f.get("pages", 0)}">{f.get("pages", "—")}</td>{cells}'
                      f'<td>{l404}</td><td>{wtag}</td>'
                      f'<td data-v="{ok}"><b>{ok}/{len(checks)}</b></td></tr>')
        irows = ""
        for s, p, v in sorted(insp_all, key=lambda x: (x[2].get("verdict") == "PASS", x[0])):
            st = v.get("verdict") or "—"
            cls = "pos" if st == "PASS" else ("warn" if st == "NEUTRAL" else "neg")
            irows += (f'<tr><td>{ABBR.get(s, s)}</td><td class="mono" style="font-size:11px">{e(p)}</td>'
                      f'<td><span class="tag {cls}">{e(st)}</span></td>'
                      f'<td class="stmeta">{e(v.get("state") or v.get("detail") or "")}</td>'
                      f'<td class="stmeta">{e((v.get("last_crawl") or "")[:10])}</td></tr>')
        openissues = []
        for s in ALL:
            for it in (G["tech_items"](s) or []):
                openissues.append((s, it))
        oihtml = "".join(f'<div class="alertrow"><span class="sev medium">FIX</span><span><b>{ABBR[s]}</b> — {e(it if isinstance(it, str) else str(it))}</span></div>'
                         for s, it in openissues) or '<div class="empty"><b>Zero unresolved technical issues.</b> All crawl checks pass on every site.</div>'
        return (f'<div class="pagehead"><h1>Technical</h1><p class="sub">Fresh BFS crawl each audit ({sum(F.get(s, {}).get("pages", 0) or 0 for s in ALL)} pages today) · '
                f'health = crawl checks passed ÷ checks run, per site — the formula, nothing else</p></div>'
                f'<div class="card" style="margin-bottom:16px"><div class="chead"><h2>Open issues</h2></div>{oihtml}</div>'
                f'<div class="card flush" style="margin-bottom:16px"><div class="chead"><h2>Crawl results by category</h2></div>'
                f'<div class="overflow"><table><thead><tr><th>site</th><th class="sortable">pages</th>'
                + "".join(f'<th class="sortable">{l}</th>' for _, l in cats)
                + f'<th>broken links</th><th>www/apex</th><th class="sortable">health</th></tr></thead><tbody>{trows}</tbody></table></div></div>'
                f'<div class="card flush" style="margin-bottom:16px"><div class="chead"><h2>Indexation — priority URLs</h2>'
                f'<span class="stmeta">money + strategic target pages via GSC URL Inspection · {len(insp_pass)}/{len(insp_all)} PASS</span></div>'
                f'<div class="twrap"><table><thead><tr><th>site</th><th>url</th><th>verdict</th><th>coverage state</th><th>last crawl</th></tr></thead>'
                f'<tbody>{irows or "<tr><td colspan=5><div class=empty>No inspection data this audit.</div></td></tr>"}</tbody></table></div></div>'
                f'<div class="empty" style="text-align:left"><b>Core Web Vitals — not integrated yet.</b> '
                f'Field data needs the CrUX API (key required) or PageSpeed Insights runs per money page. '
                f'Owner-verified PSI spot-checks remain the source of truth until then; no synthetic score is shown here.</div>')

    # ---------- AUTHORITY ----------
    def build_authority():
        rows = ""
        for i, s in enumerate(ALL):
            sm = SEM.get(s) or {}; dd = dfs_of(s)
            rdh = [x["sites"].get(s, {}).get("ref_domains") for x in HIST if s in x.get("sites", {})]
            rdh = [x for x in rdh if x is not None]
            vel = (rdh[-1] - rdh[0]) if len(rdh) >= 2 else None
            sp = dd.get("spam_score")
            spcls = "neg" if (sp or 0) >= 60 else "neu"
            sptag = f'<span class="tag {spcls}">{sp}</span>' if sp is not None else "—"
            rows += (f'<tr><td><a href="{SLUG[s]}"><span class="dot s{i+1}"></span> {ABBR[s]}</a></td>'
                     f'<td data-v="{sm.get("authority_score") or 0}">{sm.get("authority_score") if sm.get("authority_score") is not None else "—"}</td>'
                     f'<td data-v="{sm.get("ref_domains") or 0}">{sm.get("ref_domains") if sm.get("ref_domains") is not None else "—"}</td>'
                     f'<td data-v="{sm.get("backlinks") or 0}">{sm.get("backlinks") if sm.get("backlinks") is not None else "—"}</td>'
                     f'<td data-v="{dd.get("ref_domains") or 0}">{dd.get("ref_domains") if dd.get("ref_domains") is not None else "—"}</td>'
                     f'<td>{spark(rdh, w=90, h=20, color="var(--acc)") if len(rdh)>1 else "·"}</td>'
                     f'<td>{dfmt(vel, unit="") if vel is not None else "·"}</td>'
                     f'<td data-v="{sp or 0}">{sptag}</td></tr>')
        risk = [t for s_, t in SEVS if "spam" in t.lower()]
        riskhtml = "".join(f'<div class="alertrow"><span class="sev high">RISK</span><span>{e(t)}</span></div>' for t in risk) \
            or '<div class="empty">No link-risk signals. Rule: a +4-point spam-score jump on any site pauses its tier-2 link work.</div>'
        return (f'<div class="pagehead"><h1>Authority</h1><p class="sub">Two independent indexes, always labeled — '
                f'Semrush (owner-verified, {e(SEM_UPD)}) and DataForSEO (probed live each audit). Velocity from our own audit history.</p></div>'
                f'<div class="card flush" style="margin-bottom:16px"><div class="chead"><h2>Authority by site</h2></div>'
                f'<div class="overflow"><table><thead><tr><th>site</th><th class="sortable">Semrush AS</th>'
                f'<th class="sortable">SR ref.dom</th><th class="sortable">SR backlinks</th>'
                f'<th class="sortable">DFS ref.dom</th><th>DFS trend</th><th>velocity</th><th class="sortable">DFS spam</th></tr></thead>'
                f'<tbody>{rows}</tbody></table></div></div>'
                f'<div class="grid g2"><div class="card"><h2>Link risk</h2>{riskhtml}</div>'
                f'<div class="card"><h2>Quality over quantity</h2><p class="narr">Placement counts are an execution log, '
                f'not an SEO KPI — what moves rankings is referring domains that Google trusts, pointed at strategic pages. '
                f'The operational checklist (platform-by-platform) lives in the '
                f'<a href="links">link execution workflow</a>; anchor distribution and new/lost domain detail can be pulled '
                f'from DataForSEO on demand.</p></div></div>')

    # ---------- OPPORTUNITIES PAGE ----------
    def build_opportunities():
        cards = "".join(opp_card(o) for o in OPPS[:18])
        return (f'<div class="pagehead"><h1>Opportunities</h1><p class="sub">{len(OPPS)} detected · '
                f'ranked by a transparent additive score — impressions/volume band + ranking proximity + commercial intent '
                f'+ CTR upside + site phase. The score prioritises, it does not predict; the formula is documented in '
                f'<a href="settings">Integrations &amp; rules</a>.</p></div>'
                f'<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr))">{cards}</div>'
                + ('' if len(OPPS) else '<div class="empty">No opportunities detected — that usually means GSC query data is missing, not that nothing can be improved.</div>'))

    # ---------- SETTINGS ----------
    def build_settings_v4():
        integ = [
            ("Google Search Console", f"service account · {sum(1 for s in ALL if GS.get(s, {}).get('in_gsc'))}/{NSITES} properties · query/page/device/country pulled {e(GSCD.get('generated','—'))}",
             "pos" if GSCD else "warn", "Connected" if GSCD else "No deep pull yet"),
            ("DataForSEO", "backlinks, spam, live SERP probes, volumes",
             "warn" if DFS_DOWN else "pos", "OUT OF CREDIT — top up" if DFS_DOWN else "Connected"),
            ("Semrush", f"authority index · last pull {e(SEM_UPD)}", "neu", "Via Claude MCP"),
            ("Sales app", "same-origin localStorage + Firestore sync (owned by the sales session)", "neu", "Browser-local"),
            ("GA4 / analytics", "not installed on any site — organic revenue attribution unavailable", "warn", "Not connected"),
            ("CrUX / PSI", "field Core Web Vitals", "warn", "Not integrated"),
        ]
        irows = "".join(f'<div class="alertrow"><span class="tag {c}">{lab}</span><span><b>{n}</b> — {d}</span></div>'
                        for n, d, c, lab in integ)
        sr = ""
        for i, s in enumerate(ALL):
            st = _sc.CONFIG[s]
            gsctag = '<span class="tag pos">yes</span>' if GS.get(s, {}).get("in_gsc") else '<span class="tag warn">no</span>'
            sr += (f'<tr><td><span class="dot s{i+1}"></span> {s}</td><td>{e(CTRY[s][1])}</td>'
                   f'<td>{e(LANG[s][0])}</td><td class="mono" style="font-size:11px">{e(MONEY.get(s,"—"))}</td>'
                   f'<td><span class="badge b-{st["tone"]}">{st["status"]}</span></td>'
                   f'<td>{gsctag}</td></tr>')
        docs = """
<details class="panel"><summary>Severity levels</summary><div class="pbody">
CRITICAL — revenue or indexation is threatened right now (money page deindexed, site missing from GSC, confirmed top-10 loss).<br>
HIGH — high-impact ranking/traffic problem (large click loss, priority page not indexed, link-risk trigger).<br>
MEDIUM — meaningful improvement opportunity or watch item.<br>
LOW — maintenance. The Overview shows at most 7 alerts; everything else lives on its section page.</div></details>
<details class="panel"><summary>Opportunity score — exact formula</summary><div class="pbody">
score = impressions/volume band (0–30) + ranking proximity (25 − position, min 0) + commercial intent (20 if the query
contains buy/subscribe/test/brand-app terms, else 8) + CTR upside (expected−actual CTR × impressions, capped 15)
+ site phase bonus (10 growth sites, 5 others) + 5 if it is a tracked strategic keyword.
Indexation failures are pinned at 70. The score prioritises work; it is not a traffic forecast.</div></details>
<details class="panel"><summary>Expected-CTR curve</summary><div class="pbody">
Public-study heuristic by position: #1 28%, #2 15%, #3 10%, #4 7%, #5 5.5%, #6 4.5%, #7 3.7%, #8 3.1%, #9 2.6%,
#10 2.3%, 11–20 1.5%, 21+ 0.8%. Used only to flag under-performing snippets and rank opportunities.</div></details>
<details class="panel"><summary>Technical health</summary><div class="pbody">
Health = crawl checks passed ÷ checks run per site (titles ≤60, no redirect links, no orphans, canonicals OK,
no broken links, www/apex 308, favicon). No weighting, no hidden score.</div></details>
<details class="panel"><summary>Data windows</summary><div class="pbody">
GSC lags ~2 days, so every "28d" window ends 3 days ago and always compares complete periods: """ + e(range_note) + """.
Strategic positions come from live DataForSEO probes at audit time; Semrush numbers carry their own pull date.</div></details>"""
        return (f'<div class="pagehead"><h1>Integrations &amp; rules</h1><p class="sub">One site registry, one audit stamp ({e(STAMP_TXT)}), '
                f'per-source freshness — and every formula the dashboard uses, documented.</p></div>'
                f'<div class="card" style="margin-bottom:16px"><div class="chead"><h2>Data sources</h2></div>{irows}</div>'
                f'<div class="card flush" style="margin-bottom:16px"><div class="chead"><h2>Site registry</h2>'
                f'<span class="stmeta">single source of truth: seo-tools/daily/_sites.py</span></div>'
                f'<div class="overflow"><table><thead><tr><th>domain</th><th>market</th><th>language</th><th>money page</th>'
                f'<th>phase</th><th>GSC</th></tr></thead><tbody>{sr}</tbody></table></div></div>'
                f'<div class="stack" style="gap:10px">{docs}</div>')

    # ---------- write ----------
    JS = CHART_JS + TABLE_JS + PERIOD_JS
    pages = [
        ("index.html", "IPTV Portfolio — SEO Command Center", build_overview(), None, JS + SALES_JS),
        ("performance.html", "Performance — IPTV Portfolio", build_performance(), "performance", JS),
        ("rankings.html", "Rankings — IPTV Portfolio", build_rankings(), "rankings", TABLE_JS),
        ("content.html", "Content — IPTV Portfolio", build_content(), "content", TABLE_JS),
        ("technical.html", "Technical — IPTV Portfolio", build_technical(), "technical", TABLE_JS),
        ("authority.html", "Authority — IPTV Portfolio", build_authority(), "authority", TABLE_JS),
        ("opportunities.html", "Opportunities — IPTV Portfolio", build_opportunities(), "opportunities", ""),
        ("settings.html", "Integrations — IPTV Portfolio", build_settings_v4(), "settings", ""),
    ]
    for fn, title, body, cur_, js in pages:
        open(os.path.join(OUT, fn), "w").write(shell(title, body, cur=cur_, extra_js=js))
    # legacy route: trends -> performance
    open(os.path.join(OUT, "trends.html"), "w").write(
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Trends → Performance</title>'
        '<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/performance">'
        '<script>location.replace("/performance");</script></head>'
        '<body style="font:14px system-ui;padding:40px">Trends moved to <a href="/performance">Performance</a>.</body></html>')
    print(f"v4 pages written: {len(pages)} + trends redirect · opportunities={len(OPPS)} · changes={len(changes)}")
