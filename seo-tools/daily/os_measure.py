"""Measurements for the OS-transformation audit: cross-site duplication, footprint, cannibalisation. Evidence, not assumption."""
import json, re, socket, itertools, collections
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from _sites import SITES
UA={"User-Agent":"Mozilla/5.0 (compatible; iptv-portfolio-audit/1.0)"}
KEY2DOM={k:d for k,d,_ in SITES}; OWNED=[d for _,d,_ in SITES]
def fetch(u):
    try:
        r=requests.get(u,headers=UA,timeout=15); return u,r.status_code,r.text if "html" in (r.headers.get("content-type") or "") else ""
    except Exception: return u,0,""
pages={}
for k,d,c in SITES:
    try: cr=json.load(open(f"d_{k}/crawl.json"))
    except Exception: continue
    urls=[p["url"] for p in cr["pages"] if str(p.get("status"))=="200" and "?" not in p["url"]][:120]
    with ThreadPoolExecutor(10) as ex:
        for u,st,html in ex.map(fetch,urls):
            if st==200 and html: pages[u]=(d,html)
print("fetched",len(pages),"pages")
def text_of(html):
    s=BeautifulSoup(html,"lxml")
    for t in s(["script","style","noscript","nav","footer","header"]): t.decompose()
    return re.sub(r"\s+"," ",s.get_text(" ",strip=True)).lower()
def shingles(t,n=6):
    w=t.split(); return {" ".join(w[i:i+n]) for i in range(max(0,len(w)-n+1))}
sh={}; ana=collections.defaultdict(set); xlinks=collections.Counter(); tmpl={}; ids_by_site=collections.defaultdict(set)
for u,(d,html) in pages.items():
    t=text_of(html); sh[u]=(d,shingles(t),len(t.split()))
    for m in re.findall(r"(G-[A-Z0-9]{6,12}|GTM-[A-Z0-9]{5,9}|UA-\d{4,10}-\d|AW-\d{6,12})",html): ids_by_site[d].add(m)
    for m in re.findall(r"fbq\('init',\s*'(\d+)'",html): ids_by_site[d].add("FB-"+m)
    for m in re.findall(r"hjid:\s*(\d+)",html): ids_by_site[d].add("HJ-"+m)
    for href in re.findall(r'href=["\'](https?://[^"\']+)',html):
        for o in OWNED:
            if o!=d and (o in href): xlinks[(d,o)]+=1
    if u.rstrip("/")=="https://"+d or u.rstrip("/")=="https://www."+d or u.count("/")==3:
        s=BeautifulSoup(html,"lxml"); cls=set()
        for el in s.find_all(True)[:400]:
            for c in (el.get("class") or []): cls.add(c)
        tmpl[d]=cls
# near-duplicate pages across DIFFERENT sites (Jaccard on 6-word shingles)
dups=[]; bysite=collections.defaultdict(list)
for u,(d,S,n) in sh.items():
    if n>=150: bysite[d].append((u,S))
for a,b in itertools.combinations(OWNED,2):
    best=None
    for ua,Sa in bysite.get(a,[]):
        for ub,Sb in bysite.get(b,[]):
            if not Sa or not Sb: continue
            j=len(Sa&Sb)/len(Sa|Sb)
            if j>=0.25 and (best is None or j>best[0]): best=(round(j,2),ua,ub)
    if best: dups.append({"sites":[a,b],"jaccard":best[0],"page_a":best[1],"page_b":best[2]})
dups.sort(key=lambda x:-x["jaccard"])
# also count near-duplicate page PAIRS >=0.5 per site pair
pair_counts=collections.Counter()
for a,b in itertools.combinations(OWNED,2):
    for ua,Sa in bysite.get(a,[]):
        for ub,Sb in bysite.get(b,[]):
            if Sa and Sb and len(Sa&Sb)/len(Sa|Sb)>=0.5: pair_counts[(a,b)]+=1
# templates: class-name Jaccard between homepages
tpairs=[]
for a,b in itertools.combinations(list(tmpl),2):
    A,B=tmpl[a],tmpl[b]
    if A and B: tpairs.append((round(len(A&B)/len(A|B),2),a,b))
tpairs.sort(reverse=True)
# DNS
ips={}
for d in OWNED:
    try: ips[d]=sorted({ai[4][0] for ai in socket.getaddrinfo(d,443)})
    except Exception as e: ips[d]=["unresolved"]
# shared analytics ids
id_sites=collections.defaultdict(set)
for d,ids in ids_by_site.items():
    for i in ids: id_sites[i].add(d)
shared_ids={i:sorted(s) for i,s in id_sites.items() if len(s)>1}
# cannibalisation from GSC: same query, >=2 owned sites, position <=50
g=json.load(open("gsc_details.json"))["sites"]; q_sites=collections.defaultdict(list)
for d,x in g.items():
    for q,v in x.get("queries",{}).get("cur",{}).items():
        if v["position"]<=50: q_sites[q].append((d,round(v["position"],1),v["impressions"],x.get("qpage",{}).get(q,"")))
cann=[{"query":q,"sites":sorted(v,key=lambda t:t[1])} for q,v in q_sites.items() if len({d for d,*_ in v})>=2]
cann.sort(key=lambda c:-sum(t[2] for t in c["sites"]))
out={"pages_fetched":len(pages),"ips":ips,"analytics_ids":{d:sorted(v) for d,v in ids_by_site.items()},"shared_analytics_ids":shared_ids,
     "cross_links":[{"from":a,"to":b,"count":n} for (a,b),n in sorted(xlinks.items(),key=lambda x:-x[1])],
     "template_similarity":[{"sites":[a,b],"class_jaccard":j} for j,a,b in tpairs],
     "near_duplicate_best_pair":dups,"near_duplicate_pairs_ge_0_5":[{"sites":[a,b],"pairs":n} for (a,b),n in pair_counts.most_common()],
     "cannibalisation":cann}
json.dump(out,open("os_audit_measurements.json","w"),indent=1,ensure_ascii=False)
print("ips",ips); print("shared ids",shared_ids); print("xlinks",out["cross_links"][:12]); print("templates",tpairs[:8]); print("dups",dups[:8]); print("dup pairs>=.5",out["near_duplicate_pairs_ge_0_5"][:8]); print("cannibalised queries",len(cann)); [print(" ",c["query"],c["sites"]) for c in cann[:15]]
