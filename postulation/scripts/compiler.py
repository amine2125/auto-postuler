"""Compile le CV et la lettre de un ou plusieurs dossiers de candidature, en parallèle.

Usage (depuis le dossier postulation/) :
    python scripts/compiler.py candidatures/2026-10-11_Entreprise_123456 candidatures/...
    python scripts/compiler.py --tout        # tous les dossiers sans PDF à jour

Chaque dossier contient cv.tex et lettre.tex. Résultat dans le même dossier :
    FR : CV_Prenom_Nom.pdf       + Lettre_Prenom_Nom.pdf
    EN : Resume_Prenom_Nom.pdf   + Cover_Letter_Prenom_Nom.pdf
(Prenom_Nom vient de profil.json.)
Vérifie : placeholders [[...]] oubliés, compilation sans erreur, CV et lettre sur 1 page.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def suffixe_nom():
    """Prenom_Nom tiré de profil.json, sans accents ni espaces."""
    import unicodedata
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
NOMS = {
    "fr": {"cv": f"CV_{SUFFIXE}", "lettre": f"Lettre_{SUFFIXE}"},
    "en": {"cv": f"Resume_{SUFFIXE}", "lettre": f"Cover_Letter_{SUFFIXE}"},
}
CHEMINS_WINDOWS = [
    r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe",
    r"%APPDATA%\TinyTeX\bin\windows\pdflatex.exe",
    r"%ProgramFiles%\MiKTeX\miktex\bin\x64\pdflatex.exe",
]


def trouver_pdflatex():
    p = shutil.which("pdflatex")
    if p:
        return p
    for c in CHEMINS_WINDOWS:
        c = os.path.expandvars(c)
        if os.path.isfile(c):
            return c
    sys.exit("ERREUR : pdflatex introuvable. Installe MiKTeX ou TinyTeX, ou ajoute pdflatex au PATH.")


def langue(tex):
    return "fr" if re.search(r"\\usepackage\[french\]\{babel\}", tex) else "en"


def compiler_un(pdflatex, dossier, cle):
    src = os.path.join(dossier, f"{cle}.tex")
    if not os.path.isfile(src):
        return f"{cle}: fichier {cle}.tex absent"
    tex = open(src, encoding="utf-8").read()
    sans_commentaires = re.sub(r"(?<!\\)%.*", "", tex)
    reste = re.findall(r"\[\[[^\]]*\]\]", sans_commentaires)
    if reste:
        return f"{cle}: placeholders non remplis -> {', '.join(sorted(set(reste)))}"
    lg = langue(tex)
    nom = NOMS[lg][cle]
    for autre in NOMS:  # retire un ancien PDF de l'autre langue
        vieux = os.path.join(dossier, NOMS[autre][cle] + ".pdf")
        if autre != lg and os.path.isfile(vieux):
            os.remove(vieux)
    cmd =[pdflatex, "-interaction=nonstopmode", "-halt-on-error",
           f"-jobname={nom}", f"{cle}.tex"]
    r = subprocess.run(cmd, cwd=dossier, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=180)
    log_path = os.path.join(dossier, f"{nom}.log")
    log = open(log_path, encoding="utf-8", errors="replace").read() if os.path.isfile(log_path) else r.stdout
    m = re.search(r"Output written on .*?\((\d+) pages?", log)
    if r.returncode != 0 or not m:
        err = "\n".join(l for l in log.splitlines() if l.startswith("!"))[:600]
        return f"{cle}: ÉCHEC de compilation (voir {nom}.log)\n{err}"
    for ext in (".aux", ".log", ".out"):
        f = os.path.join(dossier, nom + ext)
        if os.path.isfile(f):
            os.remove(f)
    pages = int(m.group(1))
    if pages != 1:
        return f"{cle}: {nom}.pdf fait {pages} pages (doit tenir sur 1 page : raccourcir)"
    return None


def a_jour(dossier):
    pdfs = glob.glob(os.path.join(dossier, f"*_{SUFFIXE}.pdf"))
    texs = glob.glob(os.path.join(dossier, "*.tex"))
    if len(pdfs) < 2 or not texs:
        return False
    return min(os.path.getmtime(p) for p in pdfs) >= max(os.path.getmtime(t) for t in texs)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args == ["--tout"]:
        dossiers = [d for d in sorted(glob.glob(os.path.join(RACINE, "candidatures", "*")))
                    if os.path.isdir(d) and not a_jour(d)]
    else:
        dossiers = [os.path.abspath(a) for a in args]
    if not dossiers:
        print("Rien à compiler.")
        return
    pdflatex = trouver_pdflatex()
    taches = [(d, c) for d in dossiers for c in ("cv", "lettre")]
    with ThreadPoolExecutor(max_workers=min(8, len(taches))) as ex:
        resultats = list(ex.map(lambda t: compiler_un(pdflatex, *t), taches))
    erreurs = 0
    for d in dossiers:
        errs = [r for (dd, _), r in zip(taches, resultats) if dd == d and r]
        nom = os.path.basename(d.rstrip("/\\"))
        if errs:
            erreurs += 1
            print(f"[ERREUR] {nom}")
            for e in errs:
                print("   " + e.replace("\n", "\n   "))
        else:
            pdfs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(d, f"*_{SUFFIXE}.pdf")))
            print(f"[OK] {nom} -> {', '.join(pdfs)}")
    print(f"\n{len(dossiers) - erreurs}/{len(dossiers)} dossier(s) OK")
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()
