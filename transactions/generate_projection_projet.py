"""Projection de projet multi-villas.

1. Cout foncier : freehold ou leasehold, commission agence activable,
   frais de notaire (taxes + honoraires avec forfait plancher) et geometre.
2. Investissement : cout foncier + une ligne par villa (construction et
   ameublement) + creation de la PT PMA activable.
3. Revenus previsionnels : taux d'occupation et prix de la nuitee propres a
   chaque villa, charges d'exploitation, rendements et retour sur investissement.

Les villas sont nommees une seule fois (tableau 2) et leur designation est
reprise automatiquement dans le tableau des revenus.
"""

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation

ARIAL = "Arial"
IDR = '#,##0'
EUR = '#,##0.00'
PCT = '0.0%'
NB = '#,##0.0'
ENT = '#,##0'

TAUX_CHANGE = 20788.62   # reference BCE du 20/08/2026
N_VILLAS = 5

wb = Workbook()
ws = wb.active
ws.title = "Projection"


def put(cell, value, fmt=None, bold=False):
    c = ws[cell]
    c.value = value
    c.font = Font(name=ARIAL, size=11, bold=bold)
    if fmt:
        c.number_format = fmt
    return c


def param(row, label, value, fmt, commentaire=None):
    put("A%d" % row, label)
    put("B%d" % row, value, fmt)
    if commentaire:
        ws["B%d" % row].comment = Comment(commentaire, "Agence")


def montant(row, label, formule_idr, taux=None, bold=False):
    """Ligne de resultat : libelle, taux facultatif, montant IDR, montant EUR."""
    put("A%d" % row, label, bold=bold)
    if taux is not None:
        put("B%d" % row, taux, PCT)
    put("C%d" % row, formule_idr, IDR, bold=bold)
    put("D%d" % row, "=C%d/$B$7" % row, EUR, bold=bold)


def entetes(row, libelles, cols="ABCDEFG"):
    for col, lib in zip(cols, libelles):
        if lib:
            put("%s%d" % (col, row), lib, bold=True)


def liste(cellule, valeurs, commentaire):
    dv = DataValidation(type="list", formula1='"%s"' % ",".join(valeurs), allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(ws[cellule])
    ws[cellule].comment = Comment(commentaire, "Agence")


# --- En-tete ---
put("A1", "PROJECTION DE PROJET - VILLAS", bold=True)
put("A2", "Client :")
put("A3", "Terrain / localisation :")
put("A4", "Date :")

# --- Parametres generaux ---
put("A6", "PARAMETRES GENERAUX (cellules a modifier)", bold=True)
param(7, "Taux de change (IDR pour 1 EUR)", TAUX_CHANGE, '#,##0.00',
      "Taux de reference BCE du 20/08/2026 : 1 EUR = 20 788,62 IDR "
      "(source : api.frankfurter.dev). A actualiser au taux du jour.")
param(8, "Taxes gouvernementales (% du prix du terrain)", 0.05, PCT)
param(9, "Honoraires du notaire (% du prix du terrain)", 0.01, PCT)
param(10, "Honoraires du notaire - forfait minimum (IDR)", 20000000, IDR,
      "Forfait plancher : si le pourcentage d'honoraires donne moins que ce montant, "
      "c'est le forfait qui s'applique.")
param(11, "Frais de geometre (EUR)", 1000, EUR)
param(12, "Cout de creation de la PT PMA (EUR)", 2000, EUR)
param(13, "Nombre de nuits commercialisables / an", 365, ENT,
      "Base annuelle appliquee a toutes les villas (365 nuits, ou moins si la villa "
      "est fermee une partie de l'annee).")

# =====================  1. COUT FONCIER  =====================
put("A15", "1. COUT FONCIER", bold=True)
param(16, "Option retenue : FREEHOLD ou LEASEHOLD", "LEASEHOLD", None)
param(17, "Surface du terrain (ares)", 6, '#,##0.00')
param(18, "Surface du terrain (m2)", "=B17*100", ENT)
param(19, "Prix FREEHOLD - prix vendeur (IDR / are)", None, IDR)
param(20, "Prix LEASEHOLD - prix vendeur (IDR / are / an)", 4000000, IDR)
param(21, "Duree du leasehold (annees)", 30, ENT)
param(22, "Commission agence - a appliquer ? (OUI / NON)", "OUI", None)
param(23, "Taux de commission agence (% du prix vendeur)", 0.25, PCT,
      "Taux applique au prix vendeur. 25% correspond a un prix vendeur de "
      "4 000 000 IDR/are/an revendu 5 000 000 au client. A ajuster selon le dossier.")

liste("B16", ["FREEHOLD", "LEASEHOLD"],
      "Choisir FREEHOLD ou LEASEHOLD dans la liste deroulante.\n"
      "FREEHOLD -> prix du terrain = surface x B19 (prix a l'are, sans duree).\n"
      "LEASEHOLD -> prix du terrain = surface x B20 x B21 (prix a l'are et par an x duree).")
liste("B22", ["OUI", "NON"],
      "Case a cocher : OUI ajoute la commission agence (taux de la cellule B23) "
      "au prix vendeur, NON la retire.")

entetes(25, ["Poste", "Taux", "Montant IDR", "Montant EUR"])
montant(26, "Prix du terrain - PRIX VENDEUR",
        '=IF($B$16="FREEHOLD",$B$17*$B$19,$B$17*$B$20*$B$21)')
ws["C26"].comment = Comment(
    "FREEHOLD : surface x prix a l'are (B17 x B19).\n"
    "LEASEHOLD : surface x prix a l'are et par an x duree (B17 x B20 x B21).", "Agence")
montant(27, "Commission agence (si OUI en B22)", '=IF($B$22="OUI",C26*$B$23,0)',
        taux='=IF($B$22="OUI",$B$23,0)')
montant(28, "PRIX DU TERRAIN AVEC COMMISSION", "=C26+C27", bold=True)
montant(29, "Taxes gouvernementales", "=C28*$B$8", taux="=$B$8")
montant(30, "Honoraires du notaire (forfait plancher en B10)",
        "=MAX(C28*$B$9,$B$10)", taux="=IF(C28=0,0,C30/C28)")
ws["C30"].comment = Comment(
    "MAX entre le pourcentage d'honoraires (B9) et le forfait minimum (B10) : "
    "si le pourcentage donne moins que le forfait, c'est le forfait qui s'applique.\n"
    "La colonne Taux affiche le taux reellement supporte.", "Agence")
montant(31, "Sous-total frais de notaire (taxes + honoraires)", "=C29+C30",
        taux="=IF(C28=0,0,C31/C28)")
put("A32", "Frais de geometre (forfait)")
put("C32", "=$B$11*$B$7", IDR)
put("D32", "=$B$11", EUR)
montant(33, "COUT FONCIER TOTAL", "=C28+C31+C32", bold=True)

# =====================  2. INVESTISSEMENT  =====================
put("A35", "2. INVESTISSEMENT A CONSENTIR", bold=True)
param(36, "Creation de la PT PMA - a inclure ? (OUI / NON)", "OUI", None)
liste("B36", ["OUI", "NON"],
      "Case a cocher : OUI ajoute les 2 000 EUR de creation de la PT PMA (cellule B12) "
      "a l'investissement, NON les retire.")

r_v1 = 39
r_vtot = r_v1 + N_VILLAS
entetes(38, ["", "Designation de la villa", "Construction (EUR)", "Ameublement (EUR)",
             "Total villa (EUR)", "Total villa (IDR)"])
for i in range(N_VILLAS):
    r = r_v1 + i
    put("A%d" % r, "Villa %d" % (i + 1), bold=True)
    put("B%d" % r, "Villa %d" % (i + 1) if i == 0 else None)
    put("C%d" % r, None, EUR)
    put("D%d" % r, None, EUR)
    put("E%d" % r, "=C%d+D%d" % (r, r), EUR)
    put("F%d" % r, "=E%d*$B$7" % r, IDR)
ws["B%d" % r_v1].comment = Comment(
    "Nommer chaque villa ici (villa principale, villa 2 chambres, pool house...). "
    "La designation est reprise automatiquement dans le tableau des revenus.\n"
    "Laisser vide les villas non utilisees : elles comptent pour zero.", "Agence")
ws["C%d" % r_v1].comment = Comment(
    "Budget de construction en EUR. Pour un devis exprime en IDR, "
    "saisir la formule =montant_IDR/$B$7.", "Agence")
ws["D%d" % r_v1].comment = Comment(
    "Budget d'ameublement en EUR. Pour un devis exprime en IDR, "
    "saisir la formule =montant_IDR/$B$7.", "Agence")

put("A%d" % r_vtot, "TOTAL VILLAS", bold=True)
for col in "CDE":
    put("%s%d" % (col, r_vtot), "=SUM(%s%d:%s%d)" % (col, r_v1, col, r_vtot - 1), EUR, bold=True)
put("F%d" % r_vtot, "=E%d*$B$7" % r_vtot, IDR, bold=True)

r_rec = r_vtot + 2
entetes(r_rec, ["Poste", "", "Montant IDR", "Montant EUR"])
montant(r_rec + 1, "Cout foncier (report du tableau 1)", "=C33")
montant(r_rec + 2, "Constructions et ameublements (total villas)", "=F%d" % r_vtot)
montant(r_rec + 3, "Creation de la PT PMA (si OUI en B36)",
        '=IF($B$36="OUI",$B$12*$B$7,0)')
r_inv = r_rec + 4
montant(r_inv, "INVESTISSEMENT TOTAL",
        "=C%d+C%d+C%d" % (r_rec + 1, r_rec + 2, r_rec + 3), bold=True)

# =====================  3. REVENUS PREVISIONNELS  =====================
r_t3 = r_inv + 2
put("A%d" % r_t3, "3. REVENUS PREVISIONNELS PAR VILLA", bold=True)
r_charges = r_t3 + 1
param(r_charges, "Charges d'exploitation (% du revenu brut)", 0.30, PCT,
      "Pourcentage applique au revenu brut cumule de toutes les villas "
      "(gestion, menage, entretien, energie...).")

r_h3 = r_charges + 2
entetes(r_h3, ["", "Designation de la villa", "Taux d'occupation", "Prix nuitee (EUR)",
               "Nuits occupees / an", "Revenus bruts (EUR)", "Revenus bruts (IDR)"])
r_r1 = r_h3 + 1
r_rtot = r_r1 + N_VILLAS
for i in range(N_VILLAS):
    r = r_r1 + i
    rv = r_v1 + i
    put("A%d" % r, "Villa %d" % (i + 1), bold=True)
    put("B%d" % r, '=IF($B$%d="","",$B$%d)' % (rv, rv))
    put("C%d" % r, 0.65 if i == 0 else None, PCT)
    put("D%d" % r, 250 if i == 0 else None, EUR)
    put("E%d" % r, "=$B$13*C%d" % r, NB)
    put("F%d" % r, "=E%d*D%d" % (r, r), EUR)
    put("G%d" % r, "=F%d*$B$7" % r, IDR)
ws["C%d" % r_r1].comment = Comment(
    "Taux d'occupation propre a cette villa (ex. 65% = 237 nuits sur 365).", "Agence")
ws["D%d" % r_r1].comment = Comment(
    "Prix moyen de la nuitee de cette villa, en EUR. Laisser vide si la villa "
    "n'est pas utilisee dans ce scenario.", "Agence")

put("A%d" % r_rtot, "TOTAL", bold=True)
for col in "EFG":
    fmt = NB if col == "E" else (EUR if col == "F" else IDR)
    put("%s%d" % (col, r_rtot), "=SUM(%s%d:%s%d)" % (col, r_r1, col, r_rtot - 1), fmt, bold=True)

r_h4 = r_rtot + 2
entetes(r_h4, ["Poste", "Taux", "Montant IDR", "Montant EUR"])
r_brut = r_h4 + 1
put("A%d" % r_brut, "REVENUS BRUTS ANNUELS", bold=True)
put("C%d" % r_brut, "=G%d" % r_rtot, IDR, bold=True)
put("D%d" % r_brut, "=F%d" % r_rtot, EUR, bold=True)
r_ch = r_brut + 1
montant(r_ch, "Charges d'exploitation", "=C%d*$B$%d" % (r_brut, r_charges),
        taux="=$B$%d" % r_charges)
r_net = r_ch + 1
montant(r_net, "REVENUS NETS ANNUELS", "=C%d-C%d" % (r_brut, r_ch), bold=True)

r_ind = r_net + 2
put("A%d" % r_ind, "INDICATEURS", bold=True)
put("A%d" % (r_ind + 1), "Nombre de villas retenues dans le scenario")
put("B%d" % (r_ind + 1), '=COUNTIF(D%d:D%d,">0")' % (r_r1, r_rtot - 1), ENT)
put("A%d" % (r_ind + 2), "Rendement brut (revenus bruts / investissement total)")
put("B%d" % (r_ind + 2), "=IF(C%d=0,0,C%d/C%d)" % (r_inv, r_brut, r_inv), PCT)
put("A%d" % (r_ind + 3), "Rendement net (revenus nets / investissement total)")
put("B%d" % (r_ind + 3), "=IF(C%d=0,0,C%d/C%d)" % (r_inv, r_net, r_inv), PCT)
put("A%d" % (r_ind + 4), "Retour sur investissement (annees)")
put("B%d" % (r_ind + 4), "=IF(C%d=0,0,C%d/C%d)" % (r_net, r_inv, r_net), NB)

# --- Notes ---
r_notes = r_ind + 6
put("A%d" % r_notes, "NOTES / HYPOTHESES", bold=True)
notes = [
    "MODE D'EMPLOI : renseigner le terrain (tableau 1), nommer les villas et saisir leurs "
    "budgets (tableau 2), puis leur occupation et leur prix de nuitee (tableau 3). "
    "Les villas non utilisees restent vides et comptent pour zero.",
    "Tableau 1 : le choix FREEHOLD / LEASEHOLD en B16 pilote le calcul du prix du terrain ; "
    "le prix inutilise (B19 ou B20/B21) est simplement ignore. 1 are = 100 m2.",
    "Les prix du terrain sont des PRIX VENDEUR : la commission agence est ajoutee "
    "separement en ligne %d, uniquement si B22 = OUI, au taux de la cellule B23." % 27,
    "Les frais de notaire portent sur le prix du terrain commission comprise (ligne %d) : "
    "taxes gouvernementales (B8) + honoraires (B9) avec un forfait plancher de "
    "20 000 000 IDR (B10). S'y ajoute le geometre (B11)." % 28,
    "Tableau 2 : une ligne par villa, construction et ameublement saisis en EUR ; pour un "
    "devis en IDR, saisir =montant_IDR/$B$7. La designation saisie en colonne B est reprise "
    "automatiquement dans le tableau 3.",
    "La creation de la PT PMA (2 000 EUR, cellule B12) s'ajoute a l'investissement uniquement "
    "si B36 = OUI. Elle est unique pour le projet, quel que soit le nombre de villas.",
    "Tableau 3 : chaque villa a son propre taux d'occupation et son propre prix de nuitee. "
    "Revenus bruts d'une villa = nuits commercialisables (B13) x taux d'occupation x prix de "
    "la nuitee. Les charges s'appliquent au revenu brut cumule.",
    "Taux de change en B7 : reference BCE du 20/08/2026 (1 EUR = 20 788,62 IDR). "
    "A actualiser avant presentation au client.",
    "Toutes les cellules a saisir sont en colonne B (parametres et options) et dans les "
    "colonnes B, C et D des deux grilles villas. Tout le reste est calcule par formules.",
    "Projection previsionnelle a but indicatif : elle n'integre ni la fiscalite indonesienne "
    "sur les revenus locatifs, ni l'amortissement, ni les frais de gestion au-dela du "
    "pourcentage de charges saisi. En leasehold, le rendement doit s'apprecier au regard de "
    "la duree residuelle du bail.",
]
for i, n in enumerate(notes):
    put("A%d" % (r_notes + 1 + i), n)

for col, w in [("A", 50), ("B", 26), ("C", 20), ("D", 20), ("E", 20), ("F", 20), ("G", 20)]:
    ws.column_dimensions[col].width = w

wb.calculation.fullCalcOnLoad = True
out = "/home/user/jamal/transactions/Projection_de_projet.xlsx"
wb.save(out)
print(out)
