# Build Spec — IPTV Bandwidth Calculator ("Quel débit pour l'IPTV ?")

**Site:** primeiptv-france.com · **Type:** Tier-2 link magnet #4
**Angle:** upgrades the existing /guides/iptv-4k-debit-internet guide into an interactive asset.
Client-side arithmetic only.

## Page
`/calculateur-debit-iptv` — inputs: qualité (SD/HD/FHD/4K/4K HDR), nombre d'écrans simultanés,
marge réseau (Wi-Fi/Ethernet), autres usages du foyer (visio, gaming, streaming). Output: débit
recommandé en Mbps + verdict vs a user-entered speed ("votre connexion suffit-elle ?") + tips.
Values grounded in public streaming standards (e.g. ~25 Mbps per 4K stream, ~5-8 HD) — cite the
assumptions on-page. SoftwareApplication + FAQPage JSON-LD, 600+ words FR support copy, CTA to
/abonnement. Cross-link both ways with /guides/iptv-4k-debit-internet and /guides/iptv-4k.

## Copy-paste prompt
```
>>> TARGET WEBSITE: primeiptv-france.com <<<
Switch to the primeiptv-france.com project. Do NOT touch any other site.

Build /calculateur-debit-iptv — "Calculateur de débit IPTV : quel Mbps pour 2026 ?" (French,
static page + one client component, all math in-browser):
1. Inputs: qualité par flux (SD 3 / HD 6 / FHD 10 / 4K 25 / 4K HDR 32 Mbps — show these
   assumptions transparently on the page), nombre d'écrans simultanés (1-5), connexion
   (Ethernet ×1.0 / Wi-Fi ×1.3 marge), autres usages (+0/5/15 Mbps presets).
2. Output: débit minimum recommandé (Mbps, arrondi), et si l'utilisateur saisit son débit
   actuel → verdict clair (✓ suffisant / ⚠ juste / ✗ insuffisant) + 2 conseils contextuels.
3. Page: title ≤60 keyword-first ("Calculateur débit IPTV 2026 : quel Mbps pour la 4K ?"),
   meta ≤160, H1, 600+ mots FR autour (pourquoi le débit compte, buffering, QoS, Ethernet vs
   Wi-Fi), FAQ 4 items AVEC FAQPage JSON-LD + SoftwareApplication JSON-LD, self-canonical,
   sitemap.xml.
4. Links: cross-link both ways with /guides/iptv-4k-debit-internet and /guides/iptv-4k; one CTA
   to /abonnement. No sitewide links.
5. Design: existing components/tokens, Lighthouse ≥90, CLS ~0.
VERIFY: route 200 server-rendered; calculator correct on 3 test cases (1×4K Ethernet=25→ arrondi
+marge affiché; 2×HD Wi-Fi≈16; 3×FHD+gaming Ethernet≈45); JSON-LD valid; titles/meta lengths OK;
sitemap updated. Commits: feat(calculateur-debit): <item>.
```
