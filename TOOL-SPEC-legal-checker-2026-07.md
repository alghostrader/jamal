# Build Spec — "Is IPTV Legal in [Country]?" Checker

**Type:** Tier-2 linkable asset (from the Backlink & Authority plan)
**Primary home:** primeiptv-france.com (flagship — the earned authority should land here)
**Phase 2:** localized NL clone on iptvned.com (`/iptv-legaal`) — different language, not duplicate content
**Date:** 29 July 2026

---

## 1. Why this tool (the 3 jobs it does)

1. **Earns links** — a clean, sourced, dated "IPTV legality by country" reference is the kind of page bloggers, forums and Reddit threads cite naturally. That's free authority pointed at the flagship.
2. **Ranks long-tail** — each country becomes its own indexable page ("iptv légal en france", "iptv légal en belgique", "iptv legal suisse"), capturing a whole cluster of legality queries that currently go unanswered.
3. **Builds trust (E-E-A-T)** — a grey-niche sales site publishing a careful, sourced, non-alarmist legal explainer signals legitimacy to both users and Google. This directly supports the "we are a legitimate, licensed service" positioning.

---

## 2. The core framing (accurate, safe, on-brand)

**Do not** publish "IPTV is illegal/legal" as a blunt verdict. The honest and defensible message — which also happens to support the business — is:

> **IPTV is a technology, and the technology is legal everywhere. What determines legality is whether the *content* is properly licensed.** Streaming *licensed* channels through an IPTV app is legal. Accessing *pirated* streams of copyrighted content is not. The per-country differences are mostly about **how strictly this is enforced** and whether **personal use** is treated differently from **reselling/redistribution**.

Every country page reinforces this. It's true, it de-risks the content, and it frames the customer's choice around choosing a legitimate provider.

> ⚠️ **YMYL guardrail:** this is legal-information content. It is **informational, not legal advice**, must carry a visible disclaimer, must be **dated / "last reviewed"**, and every country's specifics must be **sourced and owner-verified before publish**. The dev builds the framework; the owner supplies/confirms the legal facts and sources per country. Do **not** let the model invent statutes, case law, or penalty figures.

---

## 3. Information architecture / URLs

- **Hub:** `/iptv-legal` — intro + the interactive country selector + a grid/list of all covered countries.
- **Per-country:** `/iptv-legal/[pays]` — e.g. `/iptv-legal/france`, `/iptv-legal/belgique`, `/iptv-legal/suisse`, `/iptv-legal/espagne`, `/iptv-legal/pays-bas`, `/iptv-legal/canada`, `/iptv-legal/luxembourg`.
- Static-generate (SSG) every country page at build time so the content is **fully server-rendered and indexable** — the selector is a client convenience on top, never the only way to reach the content.
- Canonical: each country page self-canonical. Hub self-canonical.
- Add all pages to `sitemap.xml`.

---

## 4. UX / behavior

**Hub page (`/iptv-legal`):**
- H1: "IPTV est-il légal ? Le guide par pays"
- One-paragraph core framing (section 2).
- **Selector:** a searchable `<select>` / combobox of countries. On choose → client-side route to `/iptv-legal/[pays]` (progressive enhancement: it's a real link, works without JS).
- Below the selector: a country grid, each card = flag + name + status badge, linking to its page.
- FAQ block (3–5 Q&As) with FAQPage schema.

**Country page (`/iptv-legal/[pays]`):**
- H1: "IPTV est-il légal en {Pays} ?"
- **Status badge** (see taxonomy below) — big, colour-coded, immediately scannable.
- Sections: *Le principe* (core framing) · *Usage personnel* · *Revente / redistribution* · *Application de la loi / sanctions* · *Comment rester du bon côté* (→ soft CTA to the licensed service).
- **"Dernière vérification : {date}"** + **Sources** list (outbound links to authorities/official texts).
- Visible disclaimer: "Ces informations sont fournies à titre indicatif et ne constituent pas un conseil juridique."
- Internal links: back to hub, to 2–3 sibling countries, and one contextual link to the money page (`/abonnement`).

---

## 5. Status taxonomy (3 tiers, colour-coded)

| Status | Badge | Meaning |
|---|---|---|
| `legal` | 🟢 Légal (avec sources sous licence) | Licensed IPTV clearly legal; piracy illegal; little/no personal-use enforcement noise |
| `conditional` | 🟡 Légal sous conditions | Licensed = legal, but piracy actively illegal; personal use tolerated, **reselling prosecuted** |
| `restricted` | 🔴 Strictement encadré | Active enforcement / ISP blocking / notable prosecutions |

The badge reflects **enforcement climate**, never "IPTV = illegal". Even `restricted` pages open with "the technology is legal; licensed streams are legal."

---

## 6. Data model

One reviewed JSON file drives all pages — `data/legal-by-country.json`:

```json
[
  {
    "code": "FR",
    "slug": "france",
    "name": "France",
    "flag": "🇫🇷",
    "status": "conditional",
    "headline": "Légal avec des sources sous licence ; le piratage est poursuivi.",
    "personal_use": "…owner-verified text…",
    "reselling": "…owner-verified text…",
    "enforcement": "…owner-verified text…",
    "sources": [
      { "label": "…official source…", "url": "https://…" }
    ],
    "last_reviewed": "2026-07-29"
  }
]
```

- **Every prose field and every source is owner-supplied/verified.** Ship with FR, BE, CH, ES, NL, CA, LU (primeiptv's francophone + neighbour markets) and expand later.
- The build fails loudly if a country is missing `sources` or `last_reviewed` (forces the guardrail).

---

## 7. SEO / structured data

- Per-country page: `Article` (or `FAQPage` for the hub) JSON-LD with `datePublished` / `dateModified` = `last_reviewed`, `author`/`publisher` = the brand.
- `<title>` keyword-first, ≤60 chars: "IPTV légal en France ? Ce que dit la loi (2026)".
- Meta description ≤160, unique per country.
- Breadcrumb schema: Accueil › IPTV légal › {Pays}.
- All country pages in the sitemap; internal-link them from the existing legal/blog content and the footer's resources area (one link to the hub, not sitewide per-country).

---

## 8. Design & accessibility

- Reuse the site's existing components, tokens, spacing — must look native, not bolted-on.
- Status badges: colour **plus** text/icon (never colour alone) for colourblind users; AA contrast.
- Fully responsive; the selector is keyboard-navigable with proper labels/ARIA.
- No layout shift on the badge (reserve space) — keep CLS at 0 like the rest of the site.
- No heavy client JS — this is a content/perf-sensitive template; keep the country pages static and fast (Perf ≥ 90).

---

## 9. Internal linking & conversion

- Hub linked once from: the footer "Ressources" area and the existing legal blog posts.
- Each country page: soft CTA — "Choisir un service avec des flux sous licence →" to `/abonnement`. Helpful, not pushy.
- **Do not** create a per-country link in a sitewide footer (footprint risk). One hub link is enough.

---

## 10. Acceptance criteria (verification)

1. `/iptv-legal` and each `/iptv-legal/[pays]` return 200 and are **server-rendered** (view-source shows the legal text, not an empty JS shell).
2. Every country page has: status badge, all content sections, `last_reviewed` date, ≥1 source link, disclaimer.
3. Valid `Article`/`FAQPage` + `BreadcrumbList` JSON-LD (test in Rich Results).
4. All pages in `sitemap.xml`; each self-canonical; titles ≤60, descriptions ≤160.
5. Lighthouse mobile ≥ 90, CLS ≈ 0 on the hub and one country page.
6. Build fails if any country lacks sources / last_reviewed.
7. Keyboard + screen-reader pass on the selector; badges legible without colour.

---

## 11. Out of scope / phase 2

- **NL clone on iptvned** (`/iptv-legaal`, `/iptv-legaal/[land]`) — translated, NL-verified data; strengthens iptvned's existing legal cluster and captures the high-volume NL legality queries. Different language on a different domain = not duplicate content. Optionally connect FR↔NL equivalents with `hreflang`.
- Later: embeddable badge widget ("IPTV legality: {country}") others can paste — turns the asset into a passive link magnet.

---

## 12. Copy-paste dev prompt

> Paste into a Claude Code session in the **primeiptv-france.com** repo. Keep the data file owner-verified — do not invent legal facts.

```
>>> TARGET WEBSITE: primeiptv-france.com <<<
Before writing any code, switch to the primeiptv-france.com project/repo in this workspace. Every
path and route below is relative to THAT project. Do NOT modify any other site (smarters-live,
iptvesp, iptvned, iptvpix, iptvshqiptar) — only primeiptv-france.com.

You are a senior Next.js engineer building a linkable SEO asset on primeiptv-france.com
(Next.js App Router on Vercel). Build an "Is IPTV legal in [country]?" checker. Follow this spec exactly.

FRAMING (use verbatim as the core message on every page): IPTV is a technology and is legal
everywhere; legality depends on whether the CONTENT is licensed. Licensed streams = legal;
pirated streams = illegal. Per-country differences are about enforcement and personal-use vs
reselling. This is informational, NOT legal advice.

BUILD:
1. Data: create data/legal-by-country.json with entries {code,slug,name,flag,status,headline,
   personal_use,reselling,enforcement,sources[],last_reviewed}. Seed FR, BE, CH, ES, NL, CA, LU.
   Leave prose/sources as clearly-marked TODO placeholders for the owner to fill/verify — do NOT
   fabricate statutes, penalties, or case law. The build must throw if any country lacks a
   non-empty sources[] or last_reviewed.
2. Routes (App Router, statically generated via generateStaticParams):
   - /iptv-legal  → intro + core framing + searchable country selector (a real <select>/links,
     works without JS) + a card grid (flag + name + colour+text status badge) + a 4-item FAQ.
   - /iptv-legal/[pays] → H1 "IPTV est-il légal en {Pays} ?", big colour+text status badge,
     sections (Le principe / Usage personnel / Revente / Application de la loi / Comment rester
     du bon côté), "Dernière vérification : {last_reviewed}", Sources list, disclaimer, links to
     hub + 2-3 sibling countries + one contextual link to /abonnement.
3. Status taxonomy: legal=🟢 "Légal (sources sous licence)", conditional=🟡 "Légal sous
   conditions", restricted=🔴 "Strictement encadré". Badge shows colour AND text/icon.
4. SEO: each page self-canonical; title keyword-first ≤60 ("IPTV légal en {Pays} ? (2026)");
   unique meta ≤160; Article JSON-LD (dateModified=last_reviewed) on country pages, FAQPage on
   the hub, BreadcrumbList on both; add all URLs to sitemap.xml.
5. Design: reuse existing components/tokens so it looks native; fully responsive; badges AA
   contrast and legible without colour; selector keyboard/ARIA accessible; reserve badge space
   so CLS stays ~0; keep pages static — Lighthouse mobile ≥90.
6. Internal links: add ONE link to /iptv-legal from the footer "Ressources" area and from the
   existing legal blog posts. Do NOT add per-country links to a sitewide footer.

VERIFY before done: both routes 200 and server-rendered (view-source shows the legal text);
JSON-LD valid in Rich Results; titles ≤60, descriptions ≤160; sitemap includes all pages;
Lighthouse mobile ≥90 and CLS ~0 on the hub + one country page; build fails on missing
sources/last_reviewed. One commit per numbered item: feat(legal-checker): <item>.
```
