"""Suivi des candidatures dans suivi/candidatures.xlsx.

Usage (depuis le dossier postulation/) :
    python scripts/suivi.py deja 123456 123457 "NomEntreprise"   # déjà postulé ? (code ou nom)
    python scripts/suivi.py ajouter candidatures/*/candidature.json   # ajoute ou met à jour
    python scripts/suivi.py statut 123456 Entrevue          # change le statut
    python scripts/suivi.py liste [20]                      # dernières lignes

candidature.json (un par dossier de candidature) :
{
  "date": "2026-10-11", "entreprise": "NomEntreprise", "poste": "Stagiaire développeur",
  "source": "La Ruche", "code": "123456", "session": "Hiver 2027",
  "langue": "FR", "statut": "Postulé", "date_limite": "2026-10-20",
  "lien": "https://...", "mots_cles": ["C#", "REST"], "a_apprendre": ["Go"],
  "changements": "Projet X en 1er ; 2 puces du stage reformulées (API REST)",
  "commentaires": ""
}
Les liens vers le CV et la lettre sont trouvés automatiquement dans le dossier.
"""
import glob
import json
import os
import re
import sys
import unicodedata
from datetime import date

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(RACINE, "suivi", "candidatures.xlsx")


def suffixe_nom():
    """Prenom_Nom tiré de profil.json (même règle que compiler.py)."""
    try:
        p = json.load(open(os.path.join(RACINE, "profil.json"), encoding="utf-8"))
        brut = f"{p.get('prenom', '')} {p.get('nom', '')}".strip()
    except Exception:
        brut = ""
    if not brut:
        return "Candidat"
    brut = unicodedata.normalize("NFKD", brut).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", brut).strip("_") or "Candidat"


SUFFIXE = suffixe_nom()
COLONNES = [  # (titre, largeur)
    ("Date", 11), ("Entreprise", 22), ("Poste", 34), ("Source", 10), ("Code", 9),
    ("Session", 12), ("Langue", 7), ("Statut", 12), ("Date limite", 11),
    ("Offre", 8), ("CV", 8), ("Lettre", 8), ("Mots-clés ajoutés", 26),
    ("À apprendre", 18), ("Changements", 45), ("Commentaires", 30), ("Dossier", 30),
]
STATUTS = ["Prêt", "Postulé", "À compléter", "Entrevue", "Refusé", "Offre", "Retirée"]
LIEN = Font(color="0563C1", underline="single")
IDX = {t: i + 1 for i, (t, _) in enumerate(COLONNES)}


def ouvrir():
    if os.path.isfile(FICHIER):
        wb = load_workbook(FICHIER)
        return wb, wb["Candidatures"]
    os.makedirs(os.path.dirname(FICHIER), exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Candidatures"
    for i, (t, w) in enumerate(COLONNES, 1):
        c = ws.cell(row=1, column=i, value=t)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = Alignment(vertical="center")
        ws.column_dimensions[c.column_letter].width = w
    ws.freeze_panes = "C2"
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUTS) + '"', allow_blank=True)
    dv.add("H2:H2000")
    ws.add_data_validation(dv)
    return wb, ws


def sauver(wb, ws):
    ws.auto_filter.ref = f"A1:{ws.cell(row=1, column=len(COLONNES)).column_letter}{max(ws.max_row, 2)}"
    try:
        wb.save(FICHIER)
    except PermissionError:
        sys.exit("ERREUR : ferme candidatures.xlsx dans Excel, puis relance la commande.")


def lignes(ws):
    for r in range(2, ws.max_row + 1):
        yield r, {t: ws.cell(row=r, column=i).value for t, i in IDX.items()}


def lien(ws, r, col, cible, texte):
    c = ws.cell(row=r, column=IDX[col], value=texte)
    c.hyperlink = cible
    c.font = LIEN


def trouver_ligne(ws, code, dossier):
    for r, v in lignes(ws):
        if code and str(v["Code"] or "").strip() == str(code).strip():
            return r
        if dossier and v["Dossier"] == dossier:
            return r
    return None


def ajouter(chemins):
    wb, ws = ouvrir()
    for p in chemins:
        d = json.load(open(p, encoding="utf-8"))
        dossier_abs = os.path.dirname(os.path.abspath(p))
        dossier = os.path.basename(dossier_abs)
        r = trouver_ligne(ws, d.get("code"), dossier)
        nouveau = r is None
        if nouveau:
            r = ws.max_row + 1
        val = {
            "Date": d.get("date") or date.today().isoformat(),
            "Entreprise": d.get("entreprise"), "Poste": d.get("poste"),
            "Source": d.get("source"), "Code": str(d.get("code") or ""),
            "Session": d.get("session"), "Langue": d.get("langue"),
            "Statut": d.get("statut", "Prêt"), "Date limite": d.get("date_limite"),
            "Mots-clés ajoutés": ", ".join(d.get("mots_cles", [])),
            "À apprendre": ", ".join(d.get("a_apprendre", [])),
            "Changements": d.get("changements"), "Commentaires": d.get("commentaires"),
        }
        for t, v in val.items():
            ws.cell(row=r, column=IDX[t], value=v)
        ws.cell(row=r, column=IDX["Changements"]).alignment = Alignment(wrap_text=True, vertical="top")
        if d.get("lien"):
            lien(ws, r, "Offre", d["lien"], "Ouvrir")
        rel = os.path.relpath(dossier_abs, os.path.dirname(FICHIER))
        lien(ws, r, "Dossier", rel, dossier)
        for col, motifs in (("CV", ("CV_", "Resume_")), ("Lettre", ("Lettre_", "Cover_Letter_"))):
            pdf = next((f for m in motifs for f in glob.glob(os.path.join(dossier_abs, m + SUFFIXE + ".pdf"))), None)
            if pdf:
                lien(ws, r, col, os.path.join(rel, os.path.basename(pdf)), "PDF")
        print(("+ ajouté   " if nouveau else "~ mis à jour ") + f"{d.get('entreprise')} | {d.get('poste')} | {val['Statut']}")
    sauver(wb, ws)


def deja(termes):
    if not os.path.isfile(FICHIER):
        print("Aucun suivi encore : rien n'est déjà postulé.")
        return
    _, ws = ouvrir()
    toutes = list(lignes(ws))
    for t in termes:
        t_low = str(t).lower().strip()
        hits = [v for _, v in toutes
                if str(v["Code"] or "").strip().lower() == t_low
                or (not t_low.isdigit() and t_low in f"{v['Entreprise']} {v['Poste']}".lower())]
        if hits:
            for v in hits:
                print(f"DÉJÀ  {t} -> {v['Date']} | {v['Entreprise']} | {v['Poste']} | {v['Statut']}")
        else:
            print(f"NOUVEAU  {t}")


def statut(code, nouveau):
    wb, ws = ouvrir()
    r = trouver_ligne(ws, code, None)
    if not r:
        sys.exit(f"Code {code} introuvable dans le suivi.")
    ws.cell(row=r, column=IDX["Statut"], value=nouveau)
    sauver(wb, ws)
    print(f"Statut de {ws.cell(row=r, column=IDX['Entreprise']).value} ({code}) -> {nouveau}")


def liste(n=20):
    if not os.path.isfile(FICHIER):
        print("Suivi vide.")
        return
    _, ws = ouvrir()
    for _, v in list(lignes(ws))[-n:]:
        print(f"{v['Date']} | {v['Entreprise']} | {v['Poste']} | {v['Code']} | {v['Statut']}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "ajouter":
        ajouter([f for x in a[1:] for f in (glob.glob(x) or [x])])
    elif a[0] == "deja":
        deja(a[1:])
    elif a[0] == "statut" and len(a) >= 3:
        statut(a[1], " ".join(a[2:]))
    elif a[0] == "liste":
        liste(int(a[1]) if len(a) > 1 else 20)
    else:
        print(__doc__)
