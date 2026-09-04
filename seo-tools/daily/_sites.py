# canonical host per site (spf + slive are www-canonical)
SITES = [
 ("esp","iptvesp.com","iptvesp.com"),
 ("prime","primeiptv-france.com","primeiptv-france.com"),
 ("ned","iptvned.com","iptvned.com"),
 ("pix","iptvpix.com","iptvpix.com"),
 ("slive","smarters-live.com","www.smarters-live.com"),
 ("shqip","iptvshqiptar.com","iptvshqiptar.com"),
 ("spf","smartersprofrance.fr","www.smartersprofrance.fr"),
 ("ifo","iptvfranceofficiel.fr","iptvfranceofficiel.fr"),
 ("aio","abonnementiptvofficiel.com","abonnementiptvofficiel.com"),
 ("segura","iptvsegura.com","iptvsegura.com"),
 ("rodak","rodaktv.com","rodaktv.com"),
]
ALL = [d for _,d,_ in SITES]
SLUG2DOM = {s:d for s,d,_ in SITES}
DOM2SLUG = {d:s for s,d,_ in SITES}
