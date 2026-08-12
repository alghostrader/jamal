#!/usr/bin/env python3
"""Recover dashboard state from the last deployed HTML (container recycle recovery).
Rebuilds keyword_targets.json, semrush.json, checkbox_state.json, links_progress.json."""
import json, os, re, sys, html as H
from bs4 import BeautifulSoup

REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/user/jamal"
BASE = os.path.dirname(os.path.abspath(__file__))
PAGES = {"iptvesp.com": "iptvesp", "primeiptv-france.com": "primeiptv-france", "iptvned.com": "iptvned",
         "iptvpix.com": "iptvpix", "smarters-live.com": "smarters-live", "iptvshqiptar.com": "iptvshqiptar",
         "smartersprofrance.fr": "smartersprofrance-fr", "iptvfranceofficiel.fr": "iptvfranceofficiel-fr",
         "abonnementiptvofficiel.com": "abonnementiptvofficiel"}

def soup_of(name):
    p = os.path.join(REPO, name + ".html")
    return BeautifulSoup(open(p, encoding="utf-8").read(), "lxml") if os.path.exists(p) else None

# ---------- keyword targets (from each site page's "Keyword targets" card) ----------
kt = {}
for dom, page in PAGES.items():
    s = soup_of(page)
    rows = []
    if s:
        for card in s.select("div.card"):
            h2 = card.find("h2")
            if not h2 or "Keyword targets" not in h2.get_text(): continue
            for tr in card.select("tbody tr"):
                td = tr.find_all("td")
                if len(td) < 3: continue
                kw = td[0].get_text(strip=True)
                try: vol = int(td[1].get_text(strip=True).replace(",", "").replace(" ", ""))
                except Exception: vol = 0
                rk = td[2].get_text(strip=True)
                m = re.match(r"#(\d+)", rk)
                row = {"kw": kw, "vol": vol, "pos": int(m.group(1)) if m else None}
                rows.append(row)
            break
    kt[dom] = rows

# money-page ownership hints (re-applied; they drive the cannibalization guard)
OWN = {"abonnementiptvofficiel.com": {"test iptv gratuit": "/test-iptv", "essai iptv 7 jours": "/test-iptv",
                                      "meilleur boitier iptv": "/boitier-iptv"},
       "iptvfranceofficiel.fr": {"iptv premium": "/iptv-premium"},
       "smartersprofrance.fr": {"iptv smarters": "/ (homepage + install hub)"}}
for dom, m in OWN.items():
    for r in kt.get(dom, []):
        if r["kw"] in m: r["page"] = m[r["kw"]]
json.dump(kt, open(os.path.join(BASE, "keyword_targets.json"), "w"), indent=1, ensure_ascii=False)
print("keyword_targets.json:", {d: len(v) for d, v in kt.items()})

# ---------- semrush (from each site page's SEMRUSH overview panel) ----------
sem = {"_note": "Owner-supplied Semrush Domain Overview values. Recovered from deployed HTML 12 Aug 2026.",
       "_updated": "2026-08-03"}
def num(txt):
    txt = (txt or "").replace(",", "").replace(" ", "").strip()
    if txt in ("", "—", "-"): return None
    try: return int(txt)
    except Exception:
        return txt if txt else None
for dom, page in PAGES.items():
    s = soup_of(page)
    if not s: continue
    panel = None
    for pn in s.select("div.ovpanel"):
        chip = pn.select_one(".ovchip")
        if chip and "SEMRUSH" in chip.get_text(): panel = pn; break
    if not panel: continue
    e = {"date": "2026-08-02"}
    for tile in panel.select(".ovtile"):
        lab = tile.select_one(".ovlabel").get_text(strip=True)
        valel = tile.select_one(".ovval")
        badge = valel.select_one(".ovbadge")
        if badge: e["as_label"] = badge.get_text(strip=True); badge.extract()
        val = valel.get_text(strip=True)
        sub = tile.select_one(".ovsub")
        subt = sub.get_text(strip=True) if sub else ""
        if lab == "Authority Score": e["authority_score"] = num(val)
        elif lab == "Organic Traffic": e["organic_traffic"] = num(val)
        elif lab == "Organic Keywords": e["organic_keywords"] = num(val); e["ok_delta"] = subt
        elif lab == "Ref. Domains": e["ref_domains"] = num(val)
        elif lab == "Backlinks": e["backlinks"] = num(val)
        elif lab == "AI Search":
            e["ai_visibility"] = num(val) or 0
            m = re.match(r"(\d+) cited(?: · (.*))?", subt)
            if m:
                e["ai_cited_pages"] = int(m.group(1)); e["ai_note"] = m.group(2) or ""
    foot = panel.select_one(".ovfoot")
    if foot and "no data" in foot.get_text().lower() and "paste" in foot.get_text().lower():
        continue
    sem[dom] = e
json.dump(sem, open(os.path.join(BASE, "semrush.json"), "w"), indent=1, ensure_ascii=False)
print("semrush.json:", len([k for k in sem if not k.startswith("_")]), "sites")

# ---------- checkbox state + links progress (from links.html) ----------
s = soup_of("links")
checked = []
if s:
    for cb in s.select("input.lpx"):
        if cb.has_attr("checked") and cb.get("id"): checked.append(cb["id"])
json.dump({"checked": sorted(checked), "_synced": "2026-08-03"},
          open(os.path.join(BASE, "checkbox_state.json"), "w"), indent=1)
print("checkbox_state.json:", len(checked), "checked")

# links_progress kept empty — the baked checkbox ids already carry the same information
if not os.path.exists(os.path.join(BASE, "links_progress.json")):
    json.dump({}, open(os.path.join(BASE, "links_progress.json"), "w"))
