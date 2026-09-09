# iptvpix deep-dive + portfolio root cause (2026-09-09)

**The question:** iptvpix has the portfolio's best backlink metric (DFS domain rank 8, 40 ref domains) yet 0 visible rankings in France *or* Belgium. Why?

**Short answer:** the "best link profile" is an illusion — those 40 links are toxic junk Google ignores. iptvpix is fully indexed and technically healthy; it doesn't rank because (a) it has zero legitimate authority, (b) its brand name collides with the established "IPTVX" app so Google won't even rank it for its own name, and (c) it targets crowded head terms owned by exact-match domains and big media. The deep-dive also exposed a **portfolio-wide root cause** that explains why authority never rises.

---

## What I tested and found

### 1. Indexation — HEALTHY (scariest hypotheses ruled out)
- `site:iptvpix.com` returns ~10+ pages (home, /abonnements, /meilleur-abonnement-iptv, /installation, /blog, …). **Indexed.**
- Homepage: HTTP 200, `server: Vercel`, **no** `x-robots-tag`. /abonnements: `<meta robots="index, follow">` + self-canonical.
- Googlebot user-agent also gets 200 (no cloaking, no bot block).
- → Not deindexed, not penalized-to-removal, no noindex leak, no DMCA delist. The site is crawlable and indexed.

### 2. Brand-entity collision — the specific iptvpix problem
- Search **"iptvpix"** (FR and BE): iptvpix.com does **not appear at all** — Google returns generic IPTV results.
- Search **"iptvpix avis"**: Google returns results for the **"IPTVX"** iOS app (3,548 App-Store ratings, established ~3 yrs).
- → Google treats "iptvpix" as a variant of the well-known **IPTVX** entity and won't rank iptvpix.com even for its own brand. No brand entity = no brand-search traffic and a weak trust signal. This is unique to pix (the name collision).

### 3. Backlinks — TOXIC, not "good" (and the real story)
The 38 referring domains, top-ranked, are almost entirely junk:
- **SEO-scraper "site value" pages** that auto-list every domain: getwebsiteworth.com, vsitestatus.com, screenshots.wiki, global-ranks.pages.dev, global-websites.pages.dev, pagesearch.net — zero editorial value.
- **Gambling / porn spam:** m98ufa.com (spam 75), betwinnermirror.com (70).
- **Fake-news spam:** theforbestimes.com, fashionclothingnews.com (70).
- **Junk directories:** australianwebdirectory.pro/.shop (70), "rankvanceseo.info" (70), "rankvanceauthority.info".
- **URL shorteners:** urls-shortener.eu, shortenurls.eu, buzzshrink.website, anchorurl.cloud, bye.fyi.
- **DataForSEO spam score: iptvpix = 50** (and the whole portfolio sits at 50–62 — high; >30 is a concern).
- → DFS's "domain rank 8" counts link *quantity*. Google counts *quality* and sees ~nothing. That's why the metric is high but rankings are zero.

### 4. Competition — money SERPs are locked
- "abonnement iptv belgique" (BE) top results: **exact-match domains** iptvbelgique24.com, iptv-be.com, smartiptvbelgique.com + **authority media** selectra, frandroid, amazon.be + AI Overview + YouTube.
- iptvpix has neither an EMD advantage nor the authority to displace them.

---

## The portfolio-wide root cause (the big finding)

**Every site shares the same ~38 toxic referring domains.** iptvesp's referring-domain list is the *identical* junk set as iptvpix's — fashionclothingnews.com, uncledspizza.com, quotesblom.com, theforbestimes.com, betwinnermirror.com, betulcrime.com, homesforsaleoldgreenwichct.com, m98ufa.com, plumeriamarketing.com, ggmap.us.com, screenshots.wiki, the url-shorteners, "rankvance*.info", etc. all appear on both.

This is the fingerprint of the **free-backlink / directory-submission / scraper campaigns** (FREE-BACKLINK-WORKFLOW, DIRECTORY-LISTING-KIT, SCALE-BACKLINK-SYSTEM). The output is a shared footprint of worthless-to-toxic links, spam-scored 50–75, that Google discounts to ~0.

**The decisive comparison:**

| | iptvesp (WINNER) | iptvpix (INVISIBLE) |
|---|---|---|
| Ranking result | 4 top-3, ETV ~423 | 0 visible rankings |
| Referring domains | same ~38 junk set | same ~38 junk set |
| Spam score | 55 | 50 |
| Brand collision | none ("iptvesp" is clean) | severe (→ "IPTVX") |
| Distinct low-comp niche | **yes** — Telegram/M3U | no — chases head terms |

The winner and the loser have **identical, worthless link profiles.** Therefore **links are not what makes iptvesp win.** iptvesp wins on two things pix lacks: a **clean brand entity** and a **distinct low-competition niche** (Telegram/listas/M3U) where topical content — not authority — decides ranking.

---

## What this means for the whole portfolio

1. **The link-building program has been building a dead (and slightly risky) asset.** The daily free-directory/bookmark/scraper links produce a shared toxic footprint that does nothing for authority and, at spam 50–75, carries mild SpamBrain risk. **Stop it.**
2. **Authority still matters — but only *real editorial* links move it.** The guest-post program (10 drafts ready, brand bylines on AS 22–62 sites) is the correct and only lever. Nothing in the current backlink footprint counts.
3. **The fastest wins come from the iptvesp playbook, not from links:** pick a *low-competition* niche and out-content it. That's why iptvesp ranks with the same zero authority everyone else has.

## Fix list — iptvpix specifically
1. **Stop pointing junk links at it.** Optionally disavow the worst offenders (m98ufa.com, betwinnermirror.com, theforbestimes.com, fashionclothingnews.com, australianwebdirectory.*) — defensible given the gambling/fake-news profile.
2. **Repair the brand entity** so Google separates IPTVPIX from IPTVX: Organization schema with `sameAs` (real social/Wikidata), consistent "IPTVPIX" brand mentions via the guest posts (byline already set to IPTVPIX), a press/about page, and brand+qualifier content. Goal: rank #1 for "iptvpix" first.
3. **Stop chasing head terms** ("abonnement iptv belgique/france") owned by EMDs + media. **Plant a distinct low-competition niche** (device/M3U/Telegram-style long-tail for the BE/CH French market) and own it the way iptvesp owns Telegram.
4. Send the pix guest draft (presse-citron → /blog/iptv-4k-france-qualite-debit) as one of the first real links.

## Fix list — portfolio
1. Retire the free-backlink/directory/scraper workflow.
2. Route all authority effort through the editorial guest-post + expert-quote program.
3. Run the "find a low-comp niche and plant it" play on every site that's invisible (pix, iptvfranceofficiel, iptvshqiptar, the FR pack) — that's the proven mechanism, independent of authority.

---

*Method: DataForSEO backlinks (referring domains, spam score, bulk ranks) + live Google SERPs (brand, money terms, site:) + live header/robots checks. 2026-09-09.*
