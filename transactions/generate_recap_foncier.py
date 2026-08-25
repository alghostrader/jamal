from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.comments import Comment

wb = Workbook()
ws = wb.active
ws.title = "Recapitulatif"

ARIAL = "Arial"
IDR = '#,##0'
EUR = '#,##0.00'
PCT = '0.0%'

def put(cell, value, fmt=None, bold=False):
    c = ws[cell]
    c.value = value
    c.font = Font(name=ARIAL, size=11, bold=bold)
    if fmt:
        c.number_format = fmt
    return c

# --- En-tete ---
put("A1", "RECAPITULATIF TRANSACTION FONCIERE - APPEL DE FONDS", bold=True)
put("A2", "Client :")
put("A3", "Terrain / localisation :")
put("A4", "Date :")

# --- Parametres (cellules a modifier) ---
put("A6", "PARAMETRES (cellules a modifier)", bold=True)
rows = [
    ("A7",  "Surface du terrain (ares)",                        "B7",  6,        '#,##0.00'),
    ("A8",  "Surface du terrain (m2)",                          "B8",  "=B7*100", '#,##0'),
    ("A9",  "Duree du leasehold (annees)",                      "B9",  30,       '#,##0'),
    ("A10", "Prix vendeur (IDR / are / an)",                    "B10", 4000000,  IDR),
    ("A11", "Prix client avec commission (IDR / are / an)",     "B11", 5000000,  IDR),
    ("A12", "Taux de change (IDR pour 1 EUR)",                  "B12", 20788.62, '#,##0.00'),
    ("A13", "Taxes gouvernementales (% du prix client)",        "B13", 0.05,     PCT),
    ("A14", "Honoraires du notaire (% du prix client)",         "B14", 0.01,     PCT),
    ("A15", "Honoraires du notaire - forfait minimum (IDR)",    "B15", 10000000, IDR),
    ("A16", "Frais de geometre (EUR)",                          "B16", 1000,     EUR),
    ("A17", "Taux d'acompte (appel de fonds)",                  "B17", 0.10,     PCT),
]
for lab_cell, lab, val_cell, val, fmt in rows:
    put(lab_cell, lab)
    put(val_cell, val, fmt)

ws["B12"].comment = Comment(
    "Taux de reference BCE du 20/08/2026 : 1 EUR = 20 788,62 IDR (source : api.frankfurter.dev).\n"
    "A actualiser au taux du jour / au taux retenu avec le client.", "Agence")
ws["B13"].comment = Comment(
    "Taxes gouvernementales : 5% du prix client (prix avec commission). "
    "Hypothese indiquee par l'agent.", "Agence")
ws["B14"].comment = Comment(
    "Honoraires du notaire : 1% du prix client (prix avec commission). "
    "Hypothese indiquee par l'agent.", "Agence")
ws["B15"].comment = Comment(
    "Forfait plancher : si 1% du prix client donne moins de 10 000 000 IDR, "
    "ce forfait s'applique a la place du pourcentage.", "Agence")

# --- Detail du calcul ---
put("A19", "DETAIL DU CALCUL", bold=True)
hdr = [("A20", "Poste"), ("B20", "Surface (ares)"), ("C20", "Duree (ans)"),
       ("D20", "Prix unitaire (IDR/are/an)"), ("E20", "Montant IDR"), ("F20", "Montant EUR")]
for cell, lab in hdr:
    put(cell, lab, bold=True)

# Ligne 21 : prix vendeur
put("A21", "Prix du terrain - PRIX VENDEUR")
put("B21", "=B7", '#,##0.00')
put("C21", "=B9", '#,##0')
put("D21", "=B10", IDR)
put("E21", "=B21*C21*D21", IDR)
put("F21", "=E21/$B$12", EUR)

# Ligne 22 : prix client
put("A22", "Prix du terrain - PRIX CLIENT (avec commission)")
put("B22", "=B7", '#,##0.00')
put("C22", "=B9", '#,##0')
put("D22", "=B11", IDR)
put("E22", "=B22*C22*D22", IDR)
put("F22", "=E22/$B$12", EUR)

# Ligne 23 : commission agence
put("A23", "dont commission agence (ecart vendeur / client)")
put("E23", "=E22-E21", IDR)
put("F23", "=E23/$B$12", EUR)

# --- Frais annexes ---
put("A25", "FRAIS ANNEXES", bold=True)
put("A26", "Taxes gouvernementales (5% du prix client)")
put("D26", "=B13", PCT)
put("E26", "=E22*$B$13", IDR)
put("F26", "=E26/$B$12", EUR)

put("A27", "Honoraires du notaire (1% du prix client, minimum 10 000 000 IDR)")
put("D27", "=IF(E22=0,0,E27/E22)", PCT)
put("E27", "=MAX(E22*$B$14,$B$15)", IDR)
put("F27", "=E27/$B$12", EUR)
ws["E27"].comment = Comment(
    "MAX entre 1% du prix client et le forfait minimum de la cellule B15 : "
    "si le pourcentage donne moins de 10 000 000 IDR, c'est le forfait qui s'applique.\n"
    "La colonne D affiche le taux reellement supporte.", "Agence")

put("A28", "Sous-total frais de notaire (taxes + honoraires)")
put("D28", "=IF(E22=0,0,E28/E22)", PCT)
put("E28", "=E26+E27", IDR)
put("F28", "=E28/$B$12", EUR)

put("A29", "Frais de geometre (forfait 1 000 EUR)")
put("E29", "=$B$16*$B$12", IDR)
put("F29", "=$B$16", EUR)

# --- Total ---
put("A31", "TOTAL DE L'OPERATION POUR L'ACHETEUR", bold=True)
put("E31", "=E22+E28+E29", IDR, bold=True)
put("F31", "=E31/$B$12", EUR, bold=True)

# --- Appel de fonds ---
put("A33", "APPEL DE FONDS", bold=True)
put("A34", "Acompte 10% du total de l'operation (reservation notaire)")
put("D34", "=B17", PCT)
put("E34", "=E31*$B$17", IDR, bold=True)
put("F34", "=E34/$B$12", EUR, bold=True)

put("A35", "Solde a regler apres acompte")
put("E35", "=E31-E34", IDR)
put("F35", "=E35/$B$12", EUR)

put("A37", "Pour information : 10% du prix du terrain seul")
put("E37", "=E22*$B$17", IDR)
put("F37", "=E37/$B$12", EUR)

# --- Notes ---
put("A39", "NOTES / HYPOTHESES", bold=True)
put("A40", "1 are = 100 m2 -> terrain de 600 m2. Prix leasehold exprime en IDR par are et par an, sur 30 ans.")
put("A41", "Taux de change en B12 : reference BCE du 20/08/2026 (1 EUR = 20 788,62 IDR). A actualiser avant envoi au client.")
put("A42", "Frais de notaire detailles : taxes gouvernementales 5% (B13) + honoraires du notaire 1% (B14).")
put("A43", "Honoraires du notaire : le pourcentage s'applique sauf s'il donne moins que le forfait minimum de 10 000 000 IDR (B15), auquel cas le forfait est retenu (formule MAX en E27).")
put("A44", "Ces taux sont appliques au prix client avec commission. Remplacer E22 par E21 dans les formules E26 et E27 si la base retenue est le prix vendeur.")
put("A45", "Frais de geometre saisis en EUR (B16) et convertis en IDR au taux B12.")
put("A46", "Seules les cellules de parametres (colonne B, lignes 7 a 17) sont a saisir : tout le reste du tableau est calcule par formules et se met a jour automatiquement.")

# largeurs de colonnes (lisibilite uniquement)
for col, w in [("A", 62), ("B", 16), ("C", 13), ("D", 26), ("E", 18), ("F", 15)]:
    ws.column_dimensions[col].width = w

wb.calculation.fullCalcOnLoad = True

out = "/home/user/jamal/transactions/Recap_transaction_fonciere_appel_de_fonds.xlsx"
wb.save(out)
print(out)
