#!/usr/bin/env python3
"""Draft site-brief.md for each portfolio site from crawl + audit data.

The 5-skill SEO system (keyword-fanout-map, seo-content-writer, onpage-optimizer,
internal-link-architect, ai-visibility-checker) reads these briefs. Fields that are
inferred rather than owner-confirmed carry the standard "⚠️ verify" marker.
Output: <out>/briefs/<slug>/site-brief.md
"""
import json, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "briefs")
TODAY = "2026-08-14"

# slug, domain, brand, market, lang_name, lang_code, money pages, lane summary,
# never-touch (anti-cannibalization), competitors seen in live SERPs this month
S = [
 dict(slug="esp", dom="iptvesp.com", brand="IPTVEsp", country="Spain", lang="Spanish", lc="es",
      money=["/suscripciones"], sells="IPTV subscription plans for Spanish viewers (Spanish + international channels, VOD).",
      lane="ES market head terms + Telegram/lists content angle. The only ES site — owns the whole Spanish lane.",
      never="Nothing portfolio-internal — sole ES site. Never free-list piracy bait beyond the existing Telegram-angle articles.",
      comp=["iptvspain.es", "suscripcion-iptv.com", "tdtchannels.com (free alternative)"],
      tone="direct, práctico, benefit-first", reader="Spanish cord-cutter comparing IPTV providers; price-sensitive, afraid of scams and cut-offs"),
 dict(slug="prime", dom="primeiptv-france.com", brand="Prime IPTV France", country="France", lang="French", lc="fr",
      money=["/abonnement"], sells="Premium IPTV subscriptions for France — the portfolio flagship.",
      lane="FR head terms: abonnement iptv, iptv france, meilleur iptv. The ONLY site allowed on FR head terms.",
      never="Smarters/app tutorials (smarters-live & smartersprofrance own those), trial/deal terms (abonnementiptvofficiel), premium/HDR angle (iptvfranceofficiel).",
      comp=["iptv-france.tv", "abonnement-iptvfrance.fr", "king365tv.com"],
      tone="premium, confiant, précis", reader="French viewer ready to buy a subscription; wants reliability, EPG quality, fast activation"),
 dict(slug="ned", dom="iptvned.com", brand="IPTVNed", country="Netherlands", lang="Dutch", lc="nl",
      money=["/abonnementen"], sells="IPTV subscriptions for the Dutch market (NL + international channels).",
      lane="NL market — sole Dutch site, owns the whole lane.",
      never="Nothing portfolio-internal — sole NL site.",
      comp=["iptv-nederland.nl", "beste-iptv.nl"],
      tone="nuchter, helder, behulpzaam", reader="Dutch viewer replacing cable; wants simple setup on Smart TV and honest pricing"),
 dict(slug="pix", dom="iptvpix.com", brand="IPTVPix", country="France", lang="French", lc="fr",
      money=["/abonnements"], sells="IPTV subscriptions, positioned through helpful FR content (guides, tutorials).",
      lane="FR content lane: informational articles, app comparisons, how-tos that funnel to /abonnements. Recovering from a deindexation — content quality is the recovery lever.",
      never="FR head terms (prime), Smarters install/config (spf), trial/deals (aio), premium/HDR (ifo).",
      comp=["iptvsmarterspros.fr", "neotv.fr"],
      tone="pédagogique, précis, sans jargon", reader="French user researching how IPTV works before buying; comparison-shopper"),
 dict(slug="slive", dom="smarters-live.com", brand="Smarters Live", country="France", lang="French", lc="fr",
      money=["https://primeiptv-france.com/abonnement (funnel to the flagship)"],
      sells="Nothing directly — the application/device hub: IPTV Smarters Pro & player guides, device checker tool. Funnels buyers to the flagship.",
      lane="'application iptv' / IPTV Smarters Pro FR lane + the device-checker tool.",
      never="Head terms (prime), install long-tail on smartersprofrance's targets, any money page of its own.",
      comp=["iptvsmarters.app", "smarterspro.fr"],
      tone="technique, fiable, tutoriel", reader="French user who already has (or wants) the Smarters app and needs setup help"),
 dict(slug="shqip", dom="iptvshqiptar.com", brand="IPTV Shqiptar", country="Albania", lang="Albanian", lc="sq",
      money=["the subscription/contact page ⚠️ verify exact URL"],
      sells="IPTV subscriptions for Albanian-speaking viewers (Albania, Kosovo, diaspora).",
      lane="Albanian market — sole sq site, owns the whole lane. Ranks via mixed-language SERPs.",
      never="Nothing portfolio-internal — sole Albanian site.",
      comp=["iptvshqip.com", "tvalb.com"],
      tone="i drejtpërdrejtë, miqësor", reader="Albanian-speaking viewer (often diaspora) wanting home channels abroad"),
 dict(slug="spf", dom="smartersprofrance.fr", brand="Smarters Pro France", country="France", lang="French", lc="fr",
      money=["/abonnement-iptv"], sells="IPTV subscriptions sold through Smarters-Pro install/config expertise.",
      lane="'iptv smarters' install/config long-tail (8,100/mo cluster): device-by-device install guides are the asset.",
      never="'application iptv' head term (smarters-live), 'abonnement iptv' head term (prime).",
      comp=["iptvsmarterspro.fr", "smarters-iptv.fr"],
      tone="tutoriel, étape par étape", reader="French user installing IPTV Smarters Pro on a specific device (Firestick, Smart TV, box)"),
 dict(slug="ifo", dom="iptvfranceofficiel.fr", brand="IPTV France Officiel", country="France", lang="French", lc="fr",
      money=["/iptv-premium"], sells="Premium/HDR-angle IPTV subscriptions (quality positioning: 4K, HDR, 22,000+ channels).",
      lane="'iptv premium' / 'iptv hdr' / 'iptv 4k' quality angle ONLY.",
      never="FR head terms (prime), free-code/gratuit bait queries (they attract non-buyers), 'application iptv' (smarters-live).",
      comp=["king365tv.com", "premium-iptv.fr"],
      tone="haut de gamme, technique, rassurant", reader="French viewer who cares about picture quality and channel breadth; less price-sensitive"),
 dict(slug="aio", dom="abonnementiptvofficiel.com", brand="Abonnement IPTV Officiel", country="France", lang="French", lc="fr",
      money=["/test-iptv (frozen — no edits)", "/iptv-premium"],
      sells="Trial-intent and deal-intent IPTV: free tests, cheap plans, plus the boitier (box) hardware angle.",
      lane="Trial/deals: 'test iptv gratuit', 'essai iptv', 'iptv pas cher' + ALL hardware/boitier terms (it ranks for them).",
      never="FR head terms (prime). NOTE: /test-iptv and /boitier-iptv are FROZEN (Google re-evaluation) — support via internal links only, zero on-page edits until probes clear them.",
      comp=["test-iptv.fr", "abonnement-iptvfrance.fr"],
      tone="direct, orienté essai, sans risque", reader="French user who wants to try before buying; deal-hunter; also boitier/hardware buyers"),
]

TPL = """# Site Brief — {brand}

> Read by: keyword-fanout-map · seo-content-writer · onpage-optimizer ·
> internal-link-architect · ai-visibility-checker
>
> Drafted automatically from the {today} portfolio audit (crawl + GSC + SERP data).
> Anything marked ⚠️ verify was inferred and needs the owner to confirm it.
>
> Last updated: {today}

---

## Part 1 — Business

- **Business name:** {brand}
- **Domain:** {dom}
- **Industry / niche:** IPTV subscription service ({country} market)
- **What they actually sell (one sentence):** {sells}
- **Price positioning:** budget-to-mid ⚠️ verify

### Services or products

1. IPTV subscription plans (1/3/6/12 months)
2. Multi-device setup support (Smart TV, Firestick, Android box, mobile)
3. Free content: setup guides, tutorials, tools

**Money pages** (internal links get prioritised towards these):
{money_lines}

### Service area

- **Primary location(s):** {country} (digital service, no physical location)
- **Country for search data:** {country}
- **Language for search data:** {lang} ({lc})

### Portfolio lane (HARD anti-cannibalization contract)

- **This site owns:** {lane}
- **This site NEVER touches:** {never}
- Portfolio rule: one keyword → one page → one site per market. Check the
  dashboard's reserved-keyword queue before targeting anything new.

### Competitors

{comp_lines}

### Goals

- **Primary goal:** subscription sales via the money page(s)
- **What a customer is worth, roughly:** ⚠️ NEEDS INPUT (monthly plan price × avg retention)
- **What this business will NOT do:** paid ads, fake reviews, money-anchor link building

### Proof and assets

- **Real numbers the business can claim:** ⚠️ NEEDS INPUT — do NOT invent channel
  counts or customer counts; use only what the money page already states.
- **Case studies / results:** none published — never fabricate.
- **Certifications / awards:** none — never fabricate.

### Author identity (E-E-A-T)

- **Who is credited as author:** ⚠️ NEEDS INPUT (no named author published today)
- Until provided: publish without a fake persona. Never invent credentials.

### The call to action

- **Primary CTA:** order (or start the trial of) the subscription on the money page ⚠️ verify wording
- **Where it points:** {money0}
- **Phone / address:** none — digital only (contact via site form/WhatsApp/Telegram ⚠️ verify)

---

## Part 2 — Voice

### Tone in three words

{tone}

### The reader

- **Who is reading:** {reader}
- **Reading level:** simple, non-technical ({lang}); short sentences
- **What they are afraid of:** scams, service cut-offs mid-subscription, buffering,
  payment safety
- **What would make them trust this site:** precise setup knowledge, honest limits,
  fast answers, visible refund/trial terms

### Say / don't say

| Always | Never |
|--------|-------|
| concrete setup steps with device names | "100% legal" or any legality claim |
| honest about what needs a stable connection | broadcaster logos / channel-brand promises |
| "test before you commit" (where trials exist) | invented user counts or reviews |
| plain {lang}, short sentences | machine-translated phrasing |

### Sentence style

- **Person:** second person ({lang} formal "you"); first person plural for the service
- **Contractions:** natural {lang} usage
- **Humour:** minimal — clarity over personality
- **Sentence length:** short; one idea per sentence; front-load the answer

---

## Hard content rules

- Respect the lane contract above — it overrides any keyword opportunity.
- Frozen pages stay frozen until the dashboard clears them.
- Brand or naked-URL anchors only in any off-site content.
- Never invent statistics, results, reviews or credentials.
- Never cite a source that was not fetched and confirmed in that run.
"""

for c in S:
    money_lines = "\n".join(f"- {m}" for m in c["money"])
    comp_lines = "\n".join(f"{i+1}. {x} ⚠️ verify (seen in live SERPs, not owner-confirmed)" for i, x in enumerate(c["comp"]))
    txt = TPL.format(today=TODAY, money0=c["money"][0], money_lines=money_lines, comp_lines=comp_lines, **c)
    d = os.path.join(OUT, c["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "site-brief.md"), "w").write(txt)
    print("brief:", c["slug"])
print("done ->", OUT)
