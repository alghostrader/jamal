# Build Spec — IPTV Player / Device Compatibility Checker

**Type:** Tier-2 linkable asset (from the Backlink & Authority plan)
**Primary home:** smarters-live.com (the Smarters Pro / app hub — this is its first linkable asset)
**Funnels the sale to:** primeiptv-france.com `/abonnement`
**Date:** 29 July 2026

---

## 1. Why this tool (the 3 jobs it does)

1. **Earns free links** — "which IPTV app works on my device?" is a question forums, Reddit, and setup blogs answer constantly. A clean device→app checker is the thing they link to instead of re-explaining. Free authority pointed at smarters-live.
2. **Ranks a big under-targeted keyword + a device long-tail** — the hub targets **"application iptv" (6,600/mo)** and **"meilleure application iptv"**, both flagged as under-targeted in the keyword audit; each device page captures its own query ("iptv firestick", "application iptv samsung smart tv", "iptv apple tv", "iptv mag"…). This is a whole cluster smarters-live currently gets nothing from.
3. **Builds the Smarters Pro hub** — the recommended app is almost always **IPTV Smarters Pro** (49,500/mo term). Every device page is a natural, non-spammy place to feature it, moving smarters-live toward owning that intent — then funnelling the actual subscription to primeiptv.

---

## 2. Core concept (what it does)

User picks their device → gets: **does it work**, the **recommended app(s)** for that device, a **short install path**, and a **CTA to a subscription that works on it**. Plus an at-a-glance **device × app compatibility matrix** on the hub.

It is a **recommendation/compatibility guide, not a player** — it never streams content. No legal or CORS complications; purely factual/technical.

---

## 3. Information architecture / URLs

- **Hub:** `/application-iptv` — intro + the device selector + the compatibility matrix + FAQ.
- **Per-device:** `/application-iptv/[appareil]` — e.g. `/application-iptv/firestick`, `/application-iptv/android-tv`, `/application-iptv/samsung-smart-tv`, `/application-iptv/lg-smart-tv`, `/application-iptv/apple-tv`, `/application-iptv/iphone-ipad`, `/application-iptv/android`, `/application-iptv/windows`, `/application-iptv/mag`.
- Static-generate (SSG) every device page so content is server-rendered and indexable; the selector is a convenience on top.
- Self-canonical each page; all in `sitemap.xml`.

**Seed devices (9):** Amazon Firestick / Fire TV, Android TV / Google TV, Samsung Smart TV (Tizen), LG Smart TV (webOS), Apple TV, iPhone / iPad, Android phone/tablet, Windows PC, MAG box. (Smart TV generic + Mac in phase 2.)

---

## 4. UX / behavior

**Hub (`/application-iptv`):**
- H1: "Quelle application IPTV pour votre appareil ?"
- One-paragraph intro (choose your device, get the right app).
- **Device selector:** searchable list / grid of device cards (icon + name). Choosing routes to `/application-iptv/[appareil]`. Real links — works without JS.
- **Compatibility matrix:** devices (rows) × apps (cols: IPTV Smarters Pro, TiviMate, others) with ✓ / ✗ / partial + text label (not colour/symbol alone).
- FAQ block (4 Q&As) with FAQPage schema.

**Device page (`/application-iptv/[appareil]`):**
- H1: "Application IPTV pour {Appareil} : le guide {année}".
- **Verdict line:** "✅ Compatible — application recommandée : IPTV Smarters Pro" (device-specific).
- Sections: *Applications recommandées* (1–3, with why) · *Comment l'installer* (numbered steps or link to the fuller guide) · *Astuces / limites* (device quirks) · *Abonnement compatible* (soft CTA).
- "Dernière vérification : {date}".
- Internal links: hub, 2–3 sibling devices, one contextual CTA to primeiptv `/abonnement`.

---

## 5. Data model

Two reviewed JSON files drive everything.

`data/apps.json`:
```json
[
  { "slug": "iptv-smarters-pro", "name": "IPTV Smarters Pro",
    "platforms": ["firestick","android-tv","android","iphone-ipad","windows"],
    "note": "…", "primary": true }
]
```

`data/devices.json`:
```json
[
  { "slug": "firestick", "name": "Amazon Firestick / Fire TV", "icon": "…",
    "supported": true,
    "recommended_apps": ["iptv-smarters-pro","tivimate"],
    "install_steps": ["…","…"],       // or "install_guide_url"
    "notes": "…device-specific quirks…",
    "last_reviewed": "2026-07-29" }
]
```

- App availability changes (store policies, device support) — so keep `last_reviewed` and let the owner correct. **Not YMYL**, so Claude may populate factual app/device data, but flag anything uncertain and keep it accurate (don't claim an app runs on a device it doesn't).
- Build warns if a device has no `recommended_apps` or `last_reviewed`.

---

## 6. SEO / structured data

- Hub `<title>` ≤60: "Application IPTV : quelle appli pour votre appareil ? (2026)". Target "application iptv".
- Device `<title>` ≤60, keyword-first per device: "Application IPTV pour Firestick (2026)" / "IPTV sur Samsung Smart TV : le guide".
- Unique meta ≤160 each.
- JSON-LD: `FAQPage` on hub; `HowTo` on device pages that have install steps (strong rich-result fit); `BreadcrumbList` on both.
- Breadcrumb: Accueil › Application IPTV › {Appareil}.
- All URLs in sitemap; internal-link the hub from the footer + relevant Smarters Pro content (one hub link, not per-device sitewide).

---

## 7. Design & accessibility

- Reuse smarters-live's existing components/tokens — must look native.
- Matrix: ✓/✗/partial as **icon + text**, never colour alone; AA contrast; horizontal-scroll wrapper on mobile so it never breaks layout.
- Device selector keyboard-navigable, proper labels/ARIA.
- Reserve space for the verdict line (no CLS); keep pages static and fast — Lighthouse mobile ≥ 90.

---

## 8. Internal linking & conversion

- Recommended app on every device page = **IPTV Smarters Pro** where accurate (builds the hub's target intent).
- Soft CTA per device: "Voir un abonnement compatible {Appareil} →" to primeiptv `/abonnement` (this is the funnel — smarters-live captures the app intent, primeiptv makes the sale).
- Hub linked once from smarters-live's footer + its Smarters Pro pages. No per-device sitewide links.

---

## 9. Acceptance criteria (verification)

1. `/application-iptv` and each `/application-iptv/[appareil]` return 200 and are **server-rendered** (view-source shows the app recommendations, not an empty shell).
2. Every device page: verdict line, recommended apps, install path, `last_reviewed`, sibling links, one CTA to primeiptv.
3. Valid `FAQPage` / `HowTo` / `BreadcrumbList` JSON-LD (Rich Results test passes).
4. All pages in sitemap; self-canonical; titles ≤60; descriptions ≤160.
5. Lighthouse mobile ≥ 90, CLS ~0 on hub + one device page.
6. Compatibility matrix legible without colour; keyboard/screen-reader pass on the selector.
7. Build warns/fails on a device missing recommended_apps / last_reviewed.
8. Every app-on-device claim is accurate (spot-check 3 devices against reality).

---

## 10. Out of scope / phase 2

- Add Mac, generic Smart TV, Fire tablet, Nvidia Shield, Chromecast.
- Localized clones for other markets (NL on iptvned, ES on iptvesp) targeting "iptv app"/"aplicación iptv" — different language, not duplicate content.
- Embeddable "works on your device" badge widget others can paste → passive link magnet.

---

## 11. Copy-paste dev prompt

> Paste into a Claude session opened on the **smarters-live.com** repo.

```
You are a senior Next.js engineer building a linkable SEO asset on smarters-live.com
(Next.js App Router on Vercel, French, www-canonical). Build an IPTV Player / Device
Compatibility Checker: users pick their device and get the recommended app(s), install path,
and a CTA to a compatible subscription. It is a recommendation guide, NOT a player — it never
streams content.

BUILD:
1. Data: create data/apps.json ({slug,name,platforms[],note,primary}) and data/devices.json
   ({slug,name,icon,supported,recommended_apps[],install_steps[] or install_guide_url,notes,
   last_reviewed}). Seed devices: firestick, android-tv, samsung-smart-tv, lg-smart-tv,
   apple-tv, iphone-ipad, android, windows, mag. Recommend IPTV Smarters Pro where accurate.
   Keep app-on-device claims factually correct; flag anything uncertain. Build warns if a device
   lacks recommended_apps or last_reviewed.
2. Routes (App Router, generateStaticParams / SSG):
   - /application-iptv → H1 "Quelle application IPTV pour votre appareil ?", intro, searchable
     device selector (real links, works without JS), a device×app compatibility matrix
     (icon+text, not colour alone, horizontal-scroll on mobile), and a 4-item FAQ.
   - /application-iptv/[appareil] → H1 "Application IPTV pour {Appareil} : le guide 2026",
     verdict line ("✅ Compatible — app recommandée : IPTV Smarters Pro"), sections
     (Applications recommandées / Comment l'installer / Astuces & limites / Abonnement
     compatible), "Dernière vérification : {date}", links to hub + 2-3 sibling devices, and one
     CTA "Voir un abonnement compatible {Appareil} →" to https://primeiptv-france.com/abonnement.
3. SEO: self-canonical; hub title "Application IPTV : quelle appli pour votre appareil ? (2026)"
   (≤60, targets "application iptv"); device titles keyword-first ≤60; unique meta ≤160;
   FAQPage JSON-LD on hub, HowTo on device pages with install steps, BreadcrumbList on both; add
   all URLs to sitemap.xml.
4. Design: reuse existing components/tokens; responsive; matrix legible without colour (icon+text,
   AA contrast); selector keyboard/ARIA accessible; reserve verdict-line space so CLS ~0; keep
   pages static, Lighthouse mobile ≥90.
5. Internal links: one link to /application-iptv from the footer and the Smarters Pro pages. No
   per-device sitewide links.

VERIFY: both routes 200 and server-rendered (view-source shows app recommendations); JSON-LD
valid in Rich Results; titles ≤60, descriptions ≤160; sitemap includes all pages; Lighthouse
≥90 and CLS ~0 on hub + one device page; app-on-device claims spot-checked on 3 devices. One
commit per numbered item: feat(device-checker): <item>.
```
