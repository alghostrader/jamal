#!/usr/bin/env python3
"""Real search volumes for curated article-angle keyword pools -> content_keywords.json"""
import json, os, time, requests
AUTH = (os.environ["DFS_LOGIN"], os.environ["DFS_PASSWORD"])
BASE = os.path.dirname(os.path.abspath(__file__))
POOLS = {
 "fr": ("France","fr",["comment installer iptv","application iptv","meilleure application iptv","iptv firestick",
   "iptv samsung smart tv","iptv box android","iptv apple tv","iptv smarters pro","test iptv gratuit","iptv m3u",
   "iptv ne fonctionne plus","vpn iptv","iptv 4k","iptv sport","configuration iptv smarters","iptv sur pc",
   "iptv freebox","iptv orange","iptv erreur de lecture","meilleur iptv france","iptv chromecast","iptv vlc",
   "meilleur iptv","iptv legal","fournisseur iptv","serveur iptv","iptv android","telecharger iptv","iptv mac",
   "iptv belgique","iptv suisse"]),
 "es": ("Spain","es",["como instalar iptv","aplicacion iptv","mejor aplicacion iptv","iptv firestick",
   "iptv samsung smart tv","iptv smarters pro","listas iptv","iptv android","iptv no funciona","iptv 4k",
   "iptv en pc","iptv legal españa","iptv vlc","iptv chromecast","mejor iptv españa","proveedor iptv",
   "mejor lista iptv","iptv smart tv","iptv de pago","iptv barato"]),
 "nl": ("Netherlands","nl",["iptv installeren","iptv app","beste iptv app","iptv firestick","iptv samsung tv",
   "iptv smarters pro","iptv kopen","iptv aanbieders","iptv box","iptv 4k","iptv legaal","iptv werkt niet",
   "iptv chromecast","beste iptv nederland","iptv provider","goedkope iptv"]),
 "sq": ("Albania","sq",["si te instaloj iptv","aplikacion iptv","iptv smart tv","iptv smarters pro","iptv shqip",
   "iptv 4k","tv shqip live"]),
}
def fetch(loc, lang, kws):
    for a in range(4):
        try:
            r = requests.post("https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live",
                auth=AUTH, json=[{"location_name": loc, "language_code": lang, "keywords": kws}], timeout=120).json()
            if r.get("status_code") == 20000:
                t = r["tasks"][0]
                if t.get("status_code") == 20000 and t.get("result"):
                    return {it["keyword"]: (it.get("search_volume") or 0) for it in t["result"]}
        except Exception: pass
        time.sleep(2*(a+1))
    return {}
out = {}
for mk,(loc,lang,kws) in POOLS.items():
    vols = fetch(loc, lang, kws)
    out[mk] = sorted([{"kw":k,"vol":vols.get(k,0)} for k in kws], key=lambda x:-x["vol"])
    print(f"{mk}: " + ", ".join(f"{r['kw']}={r['vol']}" for r in out[mk][:5]))
    time.sleep(0.5)
json.dump(out, open(os.path.join(BASE,"content_keywords.json"),"w"), indent=1, ensure_ascii=False)
print("saved content_keywords.json")
