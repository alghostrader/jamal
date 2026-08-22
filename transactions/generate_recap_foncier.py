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
    ("A15", "Frais de geometre (EUR)",                          "B15", 1000,     EUR),
    ("A16", "Taux d'acompte (appel de fonds)",                  "B16", 0.10,     PCT),
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

# --- Detail du calcul ---
put("A18", "DETAIL DU CALCUL", bold=True)
hdr = [("A19", "Poste"), ("B19", "Surface (ares)"), ("C19", "Duree (ans)"),
       ("D19", "Prix unitaire (IDR/are/an)"), ("E19", "Montant IDR"), ("F19", "Montant EUR")]
for cell, lab in hdr:
    put(cell, lab, bold=True)

# Ligne 20 : prix vendeur
put("A20", "Prix du terrain - PRIX VENDEUR")
put("B20", "=B7", '#,##0.00')
put("C20", "=B9", '#,##0')
put("D20", "=B10", IDR)
put("E20", "=B20*C20*D20", IDR)
put("F20", "=E20/$B$12", EUR)

# Ligne 21 : prix client
put("A21", "Prix du terrain - PRIX CLIENT (avec commission)")
put("B21", "=B7", '#,##0.00')
put("C21", "=B9", '#,##0')
put("D21", "=B11", IDR)
put("E21", "=B21*C21*D21", IDR)
put("F21", "=E21/$B$12", EUR)

# Ligne 22 : commission agence
put("A22", "dont commission agence (ecart vendeur / client)")
put("E22", "=E21-E20", IDR)
put("F22", "=E22/$B$12", EUR)

# --- Frais annexes ---
put("A24", "FRAIS ANNEXES", bold=True)
put("A25", "Taxes gouvernementales (5% du prix client)")
put("D25", "=B13", PCT)
put("E25", "=E21*$B$13", IDR)
put("F25", "=E25/$B$12", EUR)

put("A26", "Honoraires du notaire (1% du prix client)")
put("D26", "=B14", PCT)
put("E26", "=E21*$B$14", IDR)
put("F26", "=E26/$B$12", EUR)

put("A27", "Sous-total frais de notaire (taxes + honoraires)")
put("D27", "=B13+B14", PCT)
put("E27", "=E25+E26", IDR)
put("F27", "=E27/$B$12", EUR)

put("A28", "Frais de geometre (forfait 1 000 EUR)")
put("E28", "=$B$15*$B$12", IDR)
put("F28", "=$B$15", EUR)

# --- Total ---
put("A30", "TOTAL DE L'OPERATION POUR L'ACHETEUR", bold=True)
put("E30", "=E21+E27+E28", IDR, bold=True)
put("F30", "=E30/$B$12", EUR, bold=True)

# --- Appel de fonds ---
put("A32", "APPEL DE FONDS", bold=True)
put("A33", "Acompte 10% du total de l'operation (reservation notaire)")
put("D33", "=B16", PCT)
put("E33", "=E30*$B$16", IDR, bold=True)
put("F33", "=E33/$B$12", EUR, bold=True)

put("A34", "Solde a regler apres acompte")
put("E34", "=E30-E33", IDR)
put("F34", "=E34/$B$12", EUR)

put("A36", "Pour information : 10% du prix du terrain seul")
put("E36", "=E21*$B$16", IDR)
put("F36", "=E36/$B$12", EUR)

# --- Notes ---
put("A38", "NOTES / HYPOTHESES", bold=True)
put("A39", "1 are = 100 m2 -> terrain de 600 m2. Prix leasehold exprime en IDR par are et par an, sur 30 ans.")
put("A40", "Taux de change en B12 : reference BCE du 20/08/2026 (1 EUR = 20 788,62 IDR). A actualiser avant envoi au client.")
put("A41", "Frais de notaire detailles : 5% de taxes gouvernementales (B13) + 1% d'honoraires du notaire (B14), soit 6% au total.")
put("A42", "Ces deux taux sont appliques au prix client avec commission. Remplacer E21 par E20 dans les formules E25 et E26 si la base retenue est le prix vendeur.")
put("A43", "Frais de geometre saisis en EUR (B15) et convertis en IDR au taux B12.")
put("A44", "Seules les cellules de parametres (colonne B, lignes 7 a 16) sont a saisir : tout le reste du tableau est calcule par formules et se met a jour automatiquement.")

# largeurs de colonnes (lisibilite uniquement)
for col, w in [("A", 52), ("B", 16), ("C", 13), ("D", 26), ("E", 18), ("F", 15)]:
    ws.column_dimensions[col].width = w

wb.calculation.fullCalcOnLoad = True

out = "/home/user/jamal/transactions/Recap_transaction_fonciere_appel_de_fonds.xlsx"
wb.save(out)
print(out)
