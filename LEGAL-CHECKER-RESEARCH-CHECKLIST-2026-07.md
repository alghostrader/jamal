# Research Checklist — Legal Checker Data (7 seed countries)

**Companion to:** TOOL-SPEC-legal-checker-2026-07.md
**Purpose:** turn `data/legal-by-country.json` into a fill-in-the-blanks task.
**Date:** 29 July 2026

> ⚠️ **These are research *leads*, not legal conclusions.** The regulators, laws, and cases below are starting points to make your research fast — every actual claim (personal-use treatment, penalties, current enforcement, the final status badge) must be **confirmed from the primary source and dated** before publish. This is informational, not legal advice. When unsure, mark the field `TODO-VERIFY` and leave it out rather than guess. Prefer **primary/official sources** (government, regulator, EUR-Lex, court rulings) over blogs or competitor sites.

---

## A. The question set (answer these 8 for every country)

Fill one JSON entry per country. Each prose field = 2–4 plain-sentence answers to these:

1. **The principle** — Is IPTV-the-technology legal, and does legality hinge on content licensing? (Should be yes/yes everywhere — this is the core framing. Confirm no country outright bans IPTV apps themselves.)
2. **Personal use** — Is *watching* streams from an unlicensed source treated as an offence for the end user, or is enforcement aimed at operators/resellers? Any known end-user prosecutions?
3. **Reselling / redistribution** — What's the legal position on selling or redistributing unlicensed streams? (Almost always clearly illegal — confirm the instrument.)
4. **Enforcement climate** — Is there active ISP/site blocking? A prominent anti-piracy body? Notable recent cases? This sets the badge tier.
5. **Penalties** — What are the stated penalties for infringement/distribution? (Cite the statute — do **not** approximate.)
6. **The safe takeaway** — One sentence: how a user stays on the right side (choose licensed sources). Feeds the CTA.
7. **Sources** — ≥1 authoritative link (regulator, law text, official ruling). More = more link-worthy.
8. **Last reviewed** — Today's date on verification. Re-review every 6–12 months.

**Badge decision rule:**
`legal` = licensed clearly legal, negligible end-user enforcement · `conditional` = licensed legal but piracy actively illegal, reselling prosecuted, personal use tolerated · `restricted` = active blocking / prominent prosecutions / aggressive enforcer.

---

## B. Per-country research leads

Each block: the bodies and laws to start from, the landmark case if any, and a **suggested** starting badge to confirm (not to copy blindly).

### 🇫🇷 France — `slug: france`
- **Regulator/enforcer:** ARCOM (since Jan 2022, merged CSA + HADOPI).
- **Governing law:** Code de la propriété intellectuelle (droit d'auteur).
- **Notable:** 2021 anti-piracy law enabling court-ordered blocking of pirate **sports** streams (LaLiga/Canal+/beIN cases); ARCOM maintains a blocklist.
- **Angles to confirm:** end-user vs distributor treatment; sports-stream blocking; penalties under the CPI.
- **Suggested starting badge:** `conditional` → verify.

### 🇧🇪 Belgium — `slug: belgique`
- **Regulator/enforcer:** BAF (Belgian Anti-piracy Federation); FPS Economy.
- **Governing law:** Code de droit économique, Livre XI (droit d'auteur).
- **Notable:** courts have ordered ISP blocking of pirate services.
- **Angles to confirm:** current blocking orders; reseller prosecutions; end-user position.
- **Suggested starting badge:** `conditional` → verify (possibly `restricted` if blocking is prominent).

### 🇨🇭 Switzerland — `slug: suisse`
- **Regulator:** IPI/IGE (Swiss Federal Institute of Intellectual Property).
- **Governing law:** Copyright Act (LDA/URG), **revised 2020**.
- **Notable:** the 2020 revision targets piracy **operators/platforms**; Switzerland has historically been lenient on downloading **for personal use** — confirm exactly how the revised law treats end users now.
- **Angles to confirm:** personal-use carve-out post-2020; operator liability.
- **Suggested starting badge:** `conditional` (lenient on personal use) → verify.

### 🇪🇸 Spain — `slug: espana`
- **Regulator/enforcer:** CNMC; Comisión de Propiedad Intelectual (Ministerio de Cultura); LaLiga is a very active private enforcer.
- **Governing law:** Ley de Propiedad Intelectual (LPI).
- **Notable:** aggressive court-ordered blocking of pirate sports IPTV (LaLiga-driven), including IP-range blocks.
- **Angles to confirm:** breadth of blocking; reseller penalties; end-user treatment.
- **Suggested starting badge:** `conditional`/`restricted` → verify (enforcement is notably aggressive).

### 🇳🇱 Netherlands — `slug: pays-bas`
- **Regulator/enforcer:** BREIN (Stichting Brein) — highly active anti-piracy foundation.
- **Governing law:** Auteurswet (Copyright Act).
- **Notable:** CJEU **"Filmspeler" (2017)** ruling — selling pre-loaded IPTV boxes and **streaming from an obviously illegal source** is unlawful (removed the "temporary copy" defence for end users). This is a big one and very citable.
- **Angles to confirm:** Filmspeler's practical effect on end users; BREIN settlements/blocking.
- **Suggested starting badge:** `restricted` → verify (active enforcer + adverse end-user precedent).

### 🇨🇦 Canada — `slug: canada`
- **Regulator:** CRTC (broadcast); courts for copyright.
- **Governing law:** Copyright Act.
- **Notable:** **GoldTV (2019)** — Federal Court issued Canada's first site-blocking order; Bell/Rogers/Quebecor active; earlier FairPlay Canada blocking proposal.
- **Angles to confirm:** scope of site-blocking orders; end-user vs operator; statutory damages.
- **Suggested starting badge:** `conditional`/`restricted` → verify.

### 🇱🇺 Luxembourg — `slug: luxembourg`
- **Regulator:** ALIA (Autorité luxembourgeoise indépendante de l'audiovisuel).
- **Governing law:** Loi du 18 avril 2001 sur les droits d'auteur; EU copyright directives apply.
- **Notable:** small jurisdiction, limited public IPTV case law — lean on the EU-level framework (InfoSoc Directive, CJEU rulings incl. Filmspeler apply EU-wide).
- **Angles to confirm:** local enforcement reality; reliance on EU precedent.
- **Suggested starting badge:** `conditional` → verify (limited local case law).

---

## C. Source-quality standard (what counts as a citable source)

Rank, best first — aim for at least one from the top two tiers per country:
1. **Primary law / official body** — the statute text, the regulator's own site (ARCOM, BREIN, CNMC, IPI, ALIA, CRTC), EUR-Lex, a published court ruling.
2. **Government / EU institutional** — ministry pages, EUR-Lex case law, official press releases.
3. **Reputable press / legal analysis** — established news or law-firm commentary **only to supplement**, never as the sole source.
4. ❌ **Never cite:** competitor IPTV sites, piracy blogs, undated forum posts, or AI summaries.

Each source in JSON: `{ "label": "ARCOM — <page title>", "url": "https://…" }`. Use the real page title so the citation looks credible.

---

## D. Fill-in template (copy per country)

```json
{
  "code": "FR",
  "slug": "france",
  "name": "France",
  "flag": "🇫🇷",
  "status": "conditional",                                  // confirm via Section A badge rule
  "headline": "TODO — one line, e.g. 'Légal avec des sources sous licence ; le piratage et la revente sont poursuivis.'",
  "personal_use": "TODO-VERIFY — Q2 answer, sourced.",
  "reselling": "TODO-VERIFY — Q3 answer, sourced.",
  "enforcement": "TODO-VERIFY — Q4 answer (blocking, enforcer, recent case).",
  "penalties": "TODO-VERIFY — Q5, cite the statute; no approximations.",
  "safe_takeaway": "TODO — Q6, one sentence, feeds the CTA.",
  "sources": [
    { "label": "TODO — official source title", "url": "https://TODO" }
  ],
  "last_reviewed": "2026-07-29"
}
```

---

## E. Workflow (fast path)

1. Open the country block in Section B → visit the named regulator + law.
2. Answer the 8 questions (Section A) in plain sentences; keep each field 2–4 sentences.
3. Grab 1–2 top-tier sources (Section C).
4. Set the badge via the decision rule; date it.
5. Paste into the template (Section D). Anything unconfirmed stays `TODO-VERIFY` — the build blocks publish until sources + date exist, so half-done entries can't leak live.
6. Start with **France, Belgium, Netherlands** (highest search demand + richest case law), then CH/ES/CA/LU.

> Re-review cadence: every 6–12 months, or when a major ruling/law change lands. Bump `last_reviewed` each time — the freshness date is part of why the page earns trust and links.
