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
    ("A7",  "Surface du terrain (ares)",                    "B7",  6,        '#,##0.00'),
    ("A8",  "Surface du terrain (m2)",                      "B8",  "=B7*100", '#,##0'),
    ("A9",  "Duree du leasehold (annees)",                  "B9",  30,       '#,##0'),
    ("A10", "Prix vendeur (IDR / are / an)",                "B10", 4000000,  IDR),
    ("A11", "Prix client avec commission (IDR / are / an)", "B11", 5000000,  IDR),
    ("A12", "Taux de change (IDR pour 1 EUR)",              "B12", 20788.62, '#,##0.00'),
    ("A13", "Taux frais de notaire",                        "B13", 0.06,     PCT),
    ("A14", "Frais de geometre (EUR)",                      "B14", 1000,     EUR),
    ("A15", "Taux d'acompte (appel de fonds)",              "B15", 0.10,     PCT),
]
for lab_cell, lab, val_cell, val, fmt in rows:
    put(lab_cell, lab)
    put(val_cell, val, fmt)

ws["B12"].comment = Comment(
    "Taux de reference BCE du 20/08/2026 : 1 EUR = 20 788,62 IDR (source : api.frankfurter.dev).\n"
    "A actualiser au taux du jour / au taux retenu avec le client.", "Agence")
ws["B13"].comment = Comment(
    "Frais de notaire calcules sur le prix client (prix avec commission). "
    "Hypothese : 6% indique par l'agent.", "Agence")

# --- Detail du calcul ---
put("A17", "DETAIL DU CALCUL", bold=True)
hdr = [("A18", "Poste"), ("B18", "Surface (ares)"), ("C18", "Duree (ans)"),
       ("D18", "Prix unitaire (IDR/are/an)"), ("E18", "Montant IDR"), ("F18", "Montant EUR")]
for cell, lab in hdr:
    put(cell, lab, bold=True)

# Ligne 19 : prix vendeur
put("A19", "Prix du terrain - PRIX VENDEUR")
put("B19", "=B7", '#,##0.00')
put("C19", "=B9", '#,##0')
put("D19", "=B10", IDR)
put("E19", "=B19*C19*D19", IDR)
put("F19", "=E19/$B$12", EUR)

# Ligne 20 : prix client
put("A20", "Prix du terrain - PRIX CLIENT (avec commission)")
put("B20", "=B7", '#,##0.00')
put("C20", "=B9", '#,##0')
put("D20", "=B11", IDR)
put("E20", "=B20*C20*D20", IDR)
put("F20", "=E20/$B$12", EUR)

# Ligne 21 : commission agence
put("A21", "dont commission agence (ecart vendeur / client)")
put("E21", "=E20-E19", IDR)
put("F21", "=E21/$B$12", EUR)

# --- Frais annexes ---
put("A23", "FRAIS ANNEXES", bold=True)
put("A24", "Frais de notaire (6% du prix client)")
put("D24", "=B13", PCT)
put("E24", "=E20*$B$13", IDR)
put("F24", "=E24/$B$12", EUR)

put("A25", "Frais de geometre (forfait 1 000 EUR)")
put("E25", "=$B$14*$B$12", IDR)
put("F25", "=$B$14", EUR)

# --- Total ---
put("A27", "TOTAL DE L'OPERATION POUR L'ACHETEUR", bold=True)
put("E27", "=E20+E24+E25", IDR, bold=True)
put("F27", "=E27/$B$12", EUR, bold=True)

# --- Appel de fonds ---
put("A29", "APPEL DE FONDS", bold=True)
put("A30", "Acompte 10% du total de l'operation (reservation notaire)")
put("D30", "=B15", PCT)
put("E30", "=E27*$B$15", IDR, bold=True)
put("F30", "=E30/$B$12", EUR, bold=True)

put("A31", "Solde a regler apres acompte")
put("E31", "=E27-E30", IDR)
put("F31", "=E31/$B$12", EUR)

put("A33", "Pour information : 10% du prix du terrain seul")
put("E33", "=E20*$B$15", IDR)
put("F33", "=E33/$B$12", EUR)

# --- Notes ---
put("A35", "NOTES / HYPOTHESES", bold=True)
put("A36", "1 are = 100 m2 -> terrain de 600 m2. Prix leasehold exprime en IDR par are et par an, sur 30 ans.")
put("A37", "Taux de change en B12 : reference BCE du 20/08/2026 (1 EUR = 20 788,62 IDR). A actualiser avant envoi au client.")
put("A38", "Frais de notaire (B13) calcules sur le prix client avec commission. Modifier la formule en E24 si la base retenue est le prix vendeur.")
put("A39", "Frais de geometre saisis en EUR (B14) et convertis en IDR au taux B12.")
put("A40", "Seules les cellules de parametres (colonne B, lignes 7 a 15) sont a saisir : tout le reste du tableau est calcule par formules et se met a jour automatiquement.")

# largeurs de colonnes (lisibilite uniquement)
for col, w in [("A", 52), ("B", 16), ("C", 13), ("D", 26), ("E", 18), ("F", 15)]:
    ws.column_dimensions[col].width = w

wb.calculation.fullCalcOnLoad = True

out = "/tmp/claude-0/-home-user-jamal/26cdd4d1-672b-5bfa-bab5-b8b170387652/scratchpad/foncier/Recap_transaction_fonciere_appel_de_fonds.xlsx"
wb.save(out)
print(out)
