"""Projection de projet : cout foncier (freehold ou leasehold), investissement
a consentir (terrain + construction + ameublement + PT PMA optionnelle) et
revenus previsionnels de la villa. Tout tient sur une seule page."""

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

montant(34, "Cout foncier (report du tableau 1)", "=C28")
put("A35", "Cout de construction")
put("B35", None, EUR)
put("C35", "=B35*$B$7", IDR)
put("D35", "=B35", EUR)
ws["B35"].comment = Comment(
    "Saisir le budget de construction en EUR.\n"
    "Pour un devis exprime en IDR, saisir la formule =montant_IDR/$B$7.", "Agence")

put("A36", "Cout d'ameublement")
put("B36", None, EUR)
put("C36", "=B36*$B$7", IDR)
put("D36", "=B36", EUR)
ws["B36"].comment = Comment(
    "Saisir le budget d'ameublement en EUR.\n"
    "Pour un devis exprime en IDR, saisir la formule =montant_IDR/$B$7.", "Agence")

put("A37", "Creation de la PT PMA (si OUI en B31)")
put("B37", '=IF($B$31="OUI",$B$12,0)', EUR)
put("C37", "=B37*$B$7", IDR)
put("D37", "=B37", EUR)

montant(38, "INVESTISSEMENT TOTAL", "=C34+C35+C36+C37", bold=True)

# =====================  3. REVENUS PREVISIONNELS  =====================
put("A40", "3. REVENUS PREVISIONNELS DE LA VILLA", bold=True)
put("A41", "Taux d'occupation previsionnel");        put("B41", 0.65, PCT)
put("A42", "Prix moyen de la nuitee (EUR)");         put("B42", 250, EUR)
put("A43", "Nombre de nuits commercialisables / an"); put("B43", 365, '#,##0')
put("A44", "Charges d'exploitation (% du revenu brut)"); put("B44", 0.30, PCT)

put("A46", "Poste", bold=True)
put("C46", "Montant IDR", bold=True)
put("D46", "Montant EUR", bold=True)

put("A47", "Nuits occupees par an")
put("B47", "=B43*B41", NB)

put("A48", "REVENUS BRUTS ANNUELS", bold=True)
put("C48", "=D48*$B$7", IDR, bold=True)
put("D48", "=B47*$B$42", EUR, bold=True)

montant(49, "Charges d'exploitation (30% du revenu brut)", "=C48*$B$44")
put("B49", "=$B$44", PCT)

montant(50, "REVENUS NETS ANNUELS", "=C48-C49", bold=True)

put("A52", "INDICATEURS", bold=True)
put("A53", "Rendement brut (revenus bruts / investissement total)")
put("B53", "=IF(C38=0,0,C48/C38)", PCT)
put("A54", "Rendement net (revenus nets / investissement total)")
put("B54", "=IF(C38=0,0,C50/C38)", PCT)
put("A55", "Retour sur investissement (annees)")
put("B55", "=IF(C50=0,0,C38/C50)", NB)

# --- Notes ---
put("A57", "NOTES / HYPOTHESES", bold=True)
notes = [
    "Tableau 1 : le choix FREEHOLD / LEASEHOLD en B15 pilote le calcul du prix du terrain. "
    "Le prix inutilise (B18 ou B19/B20) est simplement ignore.",
    "1 are = 100 m2. Prix freehold exprime en IDR par are ; prix leasehold en IDR par are et "
    "par an, multiplie par la duree du bail.",
    "Frais d'acquisition identiques dans les deux options : taxes gouvernementales 5% (B8) + "
    "honoraires du notaire 1% (B9) avec un forfait plancher de 10 000 000 IDR (B10), "
    "plus le geometre (B11).",
    "Tableau 2 : le cout foncier est repris automatiquement du tableau 1. Construction et "
    "ameublement se saisissent en EUR (colonne B) ; pour un devis en IDR, saisir "
    "=montant_IDR/$B$7.",
    "La creation de la PT PMA (2 000 EUR, cellule B12) s'ajoute a l'investissement uniquement "
    "si B31 = OUI.",
    "Tableau 3 : revenus bruts = nuits commercialisables x taux d'occupation x prix de la "
    "nuitee. Les charges sont un pourcentage du revenu brut ; les revenus nets en decoulent.",
    "Taux de change en B7 : reference BCE du 20/08/2026 (1 EUR = 20 788,62 IDR). "
    "A actualiser avant presentation au client.",
    "Cellules a saisir : B7 a B12 (parametres), B15 a B20 (terrain), B31 (PT PMA), "
    "B35 et B36 (construction et ameublement), B41 a B44 (exploitation). "
    "Tout le reste est calcule par formules.",
    "Projection previsionnelle a but indicatif : elle n'integre ni la fiscalite indonesienne "
    "sur les revenus locatifs, ni l'amortissement, ni les frais de gestion au-dela du "
    "pourcentage de charges saisi.",
]
for i, n in enumerate(notes):
    put("A%d" % (58 + i), n)

for col, w in [("A", 62), ("B", 18), ("C", 20), ("D", 16)]:
    ws.column_dimensions[col].width = w

wb.calculation.fullCalcOnLoad = True
out = "/home/user/jamal/transactions/Projection_de_projet.xlsx"
wb.save(out)
print(out)
