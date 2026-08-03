# Plaquette « Apporteurs d'affaires » — Domus Cavalié Invest

Plaquette commerciale B2B (10 pages, A4, français) destinée au recrutement
d'apporteurs d'affaires pour l'accompagnement en investissement immobilier à Bali.

## Fichiers

| Fichier | Rôle |
|---|---|
| `Plaquette-Apporteurs-Affaires-Domus-Cavalie-Invest.pdf` | Le livrable diffusable |
| `brochure.html` | Source éditable (une `<section class="page">` par page) |
| `fonts_inline.css` | Polices Cormorant Garamond + Jost embarquées en base64 |
| `assets/` | Logo et visuels recadrés depuis la bannière de marque |

## Sommaire

1. Couverture
2. Le mot d'Aymeric Cavalié
3. Qui je suis — conseiller, pas vendeur
4. Balimmo, le partenaire
5. Le parcours investisseur en 6 étapes
6. Pourquoi Bali
7. Le programme apporteurs d'affaires
8. Votre rémunération
9. Le fonctionnement en 4 étapes
10. Contact

## À compléter avant diffusion

Page 10 : téléphone / WhatsApp, e-mail, site internet (marqués « à compléter »).

## Régénérer le PDF

```bash
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --disable-gpu --no-sandbox \
  --virtual-time-budget=8000 --no-pdf-header-footer \
  --print-to-pdf=Plaquette-Apporteurs-Affaires-Domus-Cavalie-Invest.pdf \
  file://$PWD/brochure.html
```

Tout chemin vers un Chromium/Chrome récent fonctionne. Les images et polices étant
locales, aucun accès réseau n'est nécessaire au rendu.

## Charte

- Vert profond `#07201A` → `#0B2C22`, or `#B08D4F` / `#E0C48D`, crème `#FBF7F0`
- Titres : Cormorant Garamond · Textes et capitales espacées : Jost
- Alternance de pages sombres (couverture, partenaire, programme, contact) et claires
