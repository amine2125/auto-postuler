#!/usr/bin/env python3
"""Suivi des candidatures dans suivi/candidatures.xlsx.

Usage (depuis le dossier postulation/) :
    python scripts/suivi.py                      # affiche ce mode d'emploi + le format de candidature.json
    python scripts/suivi.py deja <code> [...]    # indique quels codes sont deja dans le suivi
    python scripts/suivi.py ajouter candidatures/*/candidature.json   # ajoute ou met a jour des lignes
    python scripts/suivi.py statut <code> <Statut>                    # change le statut d'une ligne
    python scripts/suivi.py liste [Statut]       # liste les candidatures (filtre optionnel)

Necessite openpyxl (pip install openpyxl). Fermer l'Excel avant d'ecrire.
"""
import json
import sys
from pathlib import Path

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font
except ImportError:
    sys.exit("openpyxl manquant : pip install openpyxl")

XLSX = Path("suivi/candidatures.xlsx")
STATUTS = ["Prêt", "Postulé", "À compléter", "Entrevue", "Refusé", "Offre", "Retirée"]
# (cle dans candidature.json, titre de colonne)
COLONNES = [
    ("date", "Date"), ("entreprise", "Entreprise"), ("poste", "Poste"),
    ("source", "Source"), ("code", "Code"), ("session", "Session"),
    ("langue", "Langue"), ("statut", "Statut"), ("date_limite", "Date limite"),
    ("lien", "Lien"), ("mots_cles", "Mots-clés ajoutés"),
    ("a_apprendre", "À apprendre"), ("changements", "Changements"),
]
CLES = [c for c, _ in COLONNES]
I_CODE = CLES.index("code")
I_STATUT = CLES.index("statut")

EXEMPLE = {
    "date": "2026-01-15", "entreprise": "Acme", "poste": "Stagiaire développeur",
    "source": "Portail école | LinkedIn | Site entreprise", "code": "12345",
    "session": "Été 2027", "langue": "FR", "statut": "Prêt",
    "date_limite": "2026-02-01", "lien": "https://...",
    "mots_cles": ["React", "Docker"], "a_apprendre": ["Docker"],
    "changements": "Projets réordonnés ; compétences alignées sur l'offre.",
}


def ouvrir():
    if XLSX.exists():
        wb = load_workbook(XLSX)
        return wb, wb.active
    XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Candidatures"
    ws.append([t for _, t in COLONNES])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "A2"
    return wb, ws


def lignes(ws):
    return list(ws.iter_rows(min_row=2))


def texte(v):
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v)
    return "" if v is None else str(v)


def sauver(wb):
    try:
        wb.save(XLSX)
    except PermissionError:
        sys.exit(f"Impossible d'écrire {XLSX} : fermer le fichier Excel puis relancer.")


def cmd_deja(codes):
    wb, ws = ouvrir()
    connus = {str(r[I_CODE].value): r for r in lignes(ws)}
    for c in codes:
        r = connus.get(str(c))
        print(f"{c}: " + (f"DÉJÀ ({r[I_STATUT].value})" if r else "nouveau"))


def cmd_ajouter(fichiers):
    wb, ws = ouvrir()
    index = {str(r[I_CODE].value): r for r in lignes(ws)}
    ajoutes = maj = 0
    for f in fichiers:
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        valeurs = [texte(d.get(c)) for c in CLES]
        ligne = index.get(str(d.get("code")))
        if ligne:
            for cell, v in zip(ligne, valeurs):
                cell.value = v
            maj += 1
        else:
            ws.append(valeurs)
            index[str(d.get("code"))] = ws[ws.max_row]
            ajoutes += 1
    sauver(wb)
    print(f"{ajoutes} ajoutée(s), {maj} mise(s) à jour -> {XLSX}")


def cmd_statut(code, statut):
    if statut not in STATUTS:
        sys.exit(f"Statut inconnu. Choix : {', '.join(STATUTS)}")
    wb, ws = ouvrir()
    for r in lignes(ws):
        if str(r[I_CODE].value) == str(code):
            r[I_STATUT].value = statut
            sauver(wb)
            print(f"{code} -> {statut}")
            return
    sys.exit(f"Code {code} introuvable dans le suivi.")


def cmd_liste(filtre=None):
    _, ws = ouvrir()
    for r in lignes(ws):
        v = [texte(c.value) for c in r]
        if filtre and v[I_STATUT] != filtre:
            continue
        print(f"{v[I_CODE]:<12} {v[I_STATUT]:<12} {v[1]} — {v[2]} ({v[5]}, {v[6]})")


def main(a):
    if not a:
        print(__doc__)
        print("Format de candidature.json :")
        print(json.dumps(EXEMPLE, ensure_ascii=False, indent=2))
        print("Statuts :", ", ".join(STATUTS))
    elif a[0] == "deja" and len(a) > 1:
        cmd_deja(a[1:])
    elif a[0] == "ajouter" and len(a) > 1:
        cmd_ajouter(a[1:])
    elif a[0] == "statut" and len(a) == 3:
        cmd_statut(a[1], a[2])
    elif a[0] == "liste":
        cmd_liste(a[1] if len(a) > 1 else None)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
