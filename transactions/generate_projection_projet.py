"""Projection de projet : cout foncier (freehold ou leasehold), investissement
a consentir (terrain + jusqu'a 5 constructions + jusqu'a 5 ameublements +
PT PMA optionnelle) et revenus previsionnels de la villa. Tout sur une page."""

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation

ARIAL = "Arial"
IDR = '#,##0'
EUR = '#,##0.00'
PCT = '0.0%'
NB = '#,##0.0'

TAUX_CHANGE = 20788.62   # reference BCE du 20/08/2026
N_LIGNES = 5             # nombre de lignes construction / ameublement

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


def montant(row, label, formule_idr, bold=False):
    """Une ligne de resultat : libelle, montant IDR, montant EUR."""
    put("A%d" % row, label, bold=bold)
    put("C%d" % row, formule_idr, IDR, bold=bold)
    put("D%d" % row, "=C%d/$B$7" % row, EUR, bold=bold)


def saisie_eur(row, label, commentaire=None):
    """Une ligne saisie en EUR (colonne B) convertie en IDR."""
    put("A%d" % row, label)
    put("B%d" % row, None, EUR)
    put("C%d" % row, "=B%d*$B$7" % row, IDR)
    put("D%d" % row, "=B%d" % row, EUR)
    if commentaire:
        ws["B%d" % row].comment = Comment(commentaire, "Agence")


# --- En-tete ---
put("A1", "PROJECTION DE PROJET - VILLA", bold=True)
put("A2", "Client :")
put("A3", "Terrain / localisation :")
put("A4", "Date :")

# --- Parametres generaux ---
put("A6", "PARAMETRES GENERAUX (cellules a modifier)", bold=True)
put("A7", "Taux de change (IDR pour 1 EUR)");                  put("B7", TAUX_CHANGE, '#,##0.00')
put("A8", "Taxes gouvernementales (% du prix du terrain)");    put("B8", 0.05, PCT)
put("A9", "Honoraires du notaire (% du prix du terrain)");     put("B9", 0.01, PCT)
put("A10", "Honoraires du notaire - forfait minimum (IDR)");   put("B10", 10000000, IDR)
put("A11", "Frais de geometre (EUR)");                         put("B11", 1000, EUR)
put("A12", "Cout de creation de la PT PMA (EUR)");             put("B12", 2000, EUR)
ws["B7"].comment = Comment(
    "Taux de reference BCE du 20/08/2026 : 1 EUR = 20 788,62 IDR "
    "(source : api.frankfurter.dev). A actualiser au taux du jour.", "Agence")

# =====================  1. COUT FONCIER  =====================
put("A14", "1. COUT FONCIER", bold=True)
put("A15", "Option retenue : FREEHOLD ou LEASEHOLD");          put("B15", "LEASEHOLD")
put("A16", "Surface du terrain (ares)");                       put("B16", 6, '#,##0.00')
put("A17", "Surface du terrain (m2)");                         put("B17", "=B16*100", IDR)
put("A18", "Prix FREEHOLD - client avec commission (IDR / are)");        put("B18", None, IDR)
put("A19", "Prix LEASEHOLD - client avec commission (IDR / are / an)");  put("B19", 5000000, IDR)
put("A20", "Duree du leasehold (annees)");                     put("B20", 30, IDR)

dv_option = DataValidation(type="list", formula1='"FREEHOLD,LEASEHOLD"', allow_blank=False)
ws.add_data_validation(dv_option)
dv_option.add(ws["B15"])
ws["B15"].comment = Comment(
    "Choisir FREEHOLD ou LEASEHOLD dans la liste deroulante.\n"
    "FREEHOLD -> le prix du terrain utilise B18 (prix a l'are, sans duree).\n"
    "LEASEHOLD -> le prix du terrain utilise B19 x B20 (prix a l'are et par an x duree).",
    "Agence")

put("A22", "Poste", bold=True)
put("B22", "Taux", bold=True)
put("C22", "Montant IDR", bold=True)
put("D22", "Montant EUR", bold=True)

montant(23, "Prix du terrain (selon l'option retenue)",
        '=IF($B$15="FREEHOLD",$B$16*$B$18,$B$16*$B$19*$B$20)')
ws["C23"].comment = Comment(
    "FREEHOLD : surface x prix a l'are (B16 x B18).\n"
    "LEASEHOLD : surface x prix a l'are et par an x duree (B16 x B19 x B20).", "Agence")

montant(24, "Taxes gouvernementales (5% du prix du terrain)", "=C23*$B$8")
put("B24", "=$B$8", PCT)

montant(25, "Honoraires du notaire (1%, minimum 10 000 000 IDR)", "=MAX(C23*$B$9,$B$10)")
put("B25", "=IF(C23=0,0,C25/C23)", PCT)
ws["C25"].comment = Comment(
    "MAX entre le pourcentage d'honoraires et le forfait minimum : si le pourcentage "
    "donne moins de 10 000 000 IDR, c'est le forfait qui s'applique.\n"
    "La colonne Taux affiche le taux reellement supporte.", "Agence")

montant(26, "Sous-total frais de notaire (taxes + honoraires)", "=C24+C25")
put("B26", "=IF(C23=0,0,C26/C23)", PCT)

put("A27", "Frais de geometre (forfait)")
put("C27", "=$B$11*$B$7", IDR)
put("D27", "=$B$11", EUR)

montant(28, "COUT FONCIER TOTAL", "=C23+C26+C27", bold=True)

# =====================  2. INVESTISSEMENT  =====================
put("A30", "2. INVESTISSEMENT A CONSENTIR", bold=True)
put("A31", "Creation de la PT PMA - a inclure ? (OUI / NON)"); put("B31", "OUI")
dv_oui = DataValidation(type="list", formula1='"OUI,NON"', allow_blank=False)
ws.add_data_validation(dv_oui)
dv_oui.add(ws["B31"])
ws["B31"].comment = Comment(
    "Case a cocher : OUI ajoute les 2 000 EUR de creation de la PT PMA (cellule B12) "
    "a l'investissement, NON les retire.", "Agence")

put("A33", "Poste", bold=True)
put("B33", "Saisie (EUR)", bold=True)
put("C33", "Montant IDR", bold=True)
put("D33", "Montant EUR", bold=True)
put("E33", "Designation (libre)", bold=True)

montant(34, "Cout foncier (report du tableau 1)", "=C28")

aide = ("Saisir le montant en EUR. Laisser vide si la ligne n'est pas utilisee.\n"
        "Pour un devis exprime en IDR, saisir la formule =montant_IDR/$B$7.\n"
        "La colonne E permet de nommer la ligne (villa 1, piscine, pool house...).")

r_c1 = 36
for i in range(N_LIGNES):
    saisie_eur(r_c1 + i, "Construction %d" % (i + 1), aide)
r_csum = r_c1 + N_LIGNES
montant(r_csum, "SOUS-TOTAL CONSTRUCTION",
        "=SUM(C%d:C%d)" % (r_c1, r_csum - 1), bold=True)

r_a1 = r_csum + 2
for i in range(N_LIGNES):
    saisie_eur(r_a1 + i, "Ameublement %d" % (i + 1), aide)
r_asum = r_a1 + N_LIGNES
montant(r_asum, "SOUS-TOTAL AMEUBLEMENT",
        "=SUM(C%d:C%d)" % (r_a1, r_asum - 1), bold=True)

r_pt = r_asum + 2
put("A%d" % r_pt, "Creation de la PT PMA (si OUI en B31)")
put("B%d" % r_pt, '=IF($B$31="OUI",$B$12,0)', EUR)
put("C%d" % r_pt, "=B%d*$B$7" % r_pt, IDR)
put("D%d" % r_pt, "=B%d" % r_pt, EUR)

r_inv = r_pt + 1
montant(r_inv, "INVESTISSEMENT TOTAL",
        "=C34+C%d+C%d+C%d" % (r_csum, r_asum, r_pt), bold=True)

# =====================  3. REVENUS PREVISIONNELS  =====================
r = r_inv + 2
put("A%d" % r, "3. REVENUS PREVISIONNELS DE LA VILLA", bold=True)
r_occ, r_nuitee, r_nuits, r_charges = r + 1, r + 2, r + 3, r + 4
put("A%d" % r_occ, "Taux d'occupation previsionnel");            put("B%d" % r_occ, 0.65, PCT)
put("A%d" % r_nuitee, "Prix moyen de la nuitee (EUR)");          put("B%d" % r_nuitee, 250, EUR)
put("A%d" % r_nuits, "Nombre de nuits commercialisables / an");  put("B%d" % r_nuits, 365, '#,##0')
put("A%d" % r_charges, "Charges d'exploitation (% du revenu brut)"); put("B%d" % r_charges, 0.30, PCT)

r_hdr = r_charges + 2
put("A%d" % r_hdr, "Poste", bold=True)
put("C%d" % r_hdr, "Montant IDR", bold=True)
put("D%d" % r_hdr, "Montant EUR", bold=True)

r_occup = r_hdr + 1
put("A%d" % r_occup, "Nuits occupees par an")
put("B%d" % r_occup, "=B%d*B%d" % (r_nuits, r_occ), NB)

r_brut = r_occup + 1
put("A%d" % r_brut, "REVENUS BRUTS ANNUELS", bold=True)
put("C%d" % r_brut, "=D%d*$B$7" % r_brut, IDR, bold=True)
put("D%d" % r_brut, "=B%d*$B$%d" % (r_occup, r_nuitee), EUR, bold=True)

r_ch = r_brut + 1
montant(r_ch, "Charges d'exploitation (% du revenu brut)", "=C%d*$B$%d" % (r_brut, r_charges))
put("B%d" % r_ch, "=$B$%d" % r_charges, PCT)

r_net = r_ch + 1
montant(r_net, "REVENUS NETS ANNUELS", "=C%d-C%d" % (r_brut, r_ch), bold=True)

r_ind = r_net + 2
put("A%d" % r_ind, "INDICATEURS", bold=True)
put("A%d" % (r_ind + 1), "Rendement brut (revenus bruts / investissement total)")
put("B%d" % (r_ind + 1), "=IF(C%d=0,0,C%d/C%d)" % (r_inv, r_brut, r_inv), PCT)
put("A%d" % (r_ind + 2), "Rendement net (revenus nets / investissement total)")
put("B%d" % (r_ind + 2), "=IF(C%d=0,0,C%d/C%d)" % (r_inv, r_net, r_inv), PCT)
put("A%d" % (r_ind + 3), "Retour sur investissement (annees)")
put("B%d" % (r_ind + 3), "=IF(C%d=0,0,C%d/C%d)" % (r_net, r_inv, r_net), NB)

# --- Notes ---
r_notes = r_ind + 5
put("A%d" % r_notes, "NOTES / HYPOTHESES", bold=True)
notes = [
    "Tableau 1 : le choix FREEHOLD / LEASEHOLD en B15 pilote le calcul du prix du terrain. "
    "Le prix inutilise (B18 ou B19/B20) est simplement ignore.",
    "1 are = 100 m2. Prix freehold exprime en IDR par are ; prix leasehold en IDR par are et "
    "par an, multiplie par la duree du bail.",
    "Frais d'acquisition identiques dans les deux options : taxes gouvernementales 5% (B8) + "
    "honoraires du notaire 1% (B9) avec un forfait plancher de 10 000 000 IDR (B10), "
    "plus le geometre (B11).",
    "Tableau 2 : le cout foncier est repris automatiquement du tableau 1.",
    "Cinq lignes de construction (%d a %d) et cinq lignes d'ameublement (%d a %d) sont "
    "disponibles : n'en remplir que le nombre necessaire, les lignes vides comptent pour zero. "
    "La colonne E sert a nommer chaque ligne (villa 1, piscine, pool house, lot mobilier...)."
    % (r_c1, r_csum - 1, r_a1, r_asum - 1),
    "Constructions et ameublements se saisissent en EUR (colonne B) ; pour un devis en IDR, "
    "saisir =montant_IDR/$B$7. Les sous-totaux des lignes %d et %d alimentent "
    "l'investissement total." % (r_csum, r_asum),
    "La creation de la PT PMA (2 000 EUR, cellule B12) s'ajoute a l'investissement uniquement "
    "si B31 = OUI.",
    "Tableau 3 : revenus bruts = nuits commercialisables x taux d'occupation x prix de la "
    "nuitee. Les charges sont un pourcentage du revenu brut ; les revenus nets en decoulent.",
    "Taux de change en B7 : reference BCE du 20/08/2026 (1 EUR = 20 788,62 IDR). "
    "A actualiser avant presentation au client.",
    "Cellules a saisir : B7 a B12 (parametres), B15 a B20 (terrain), B31 (PT PMA), "
    "B%d a B%d (constructions et ameublements), B%d a B%d (exploitation). "
    "Tout le reste est calcule par formules."
    % (r_c1, r_asum - 1, r_occ, r_charges),
    "Projection previsionnelle a but indicatif : elle n'integre ni la fiscalite indonesienne "
    "sur les revenus locatifs, ni l'amortissement, ni les frais de gestion au-dela du "
    "pourcentage de charges saisi.",
]
for i, n in enumerate(notes):
    put("A%d" % (r_notes + 1 + i), n)

for col, w in [("A", 62), ("B", 18), ("C", 20), ("D", 16), ("E", 26)]:
    ws.column_dimensions[col].width = w

wb.calculation.fullCalcOnLoad = True
out = "/home/user/jamal/transactions/Projection_de_projet.xlsx"
wb.save(out)
print(out)
