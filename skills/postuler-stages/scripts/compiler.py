#!/usr/bin/env python3
"""Compile cv.tex et lettre.tex (pdflatex) pour une ou plusieurs candidatures.

Usage (depuis le dossier postulation/) :
    python scripts/compiler.py candidatures/<dossier1> candidatures/<dossier2> ...
    python scripts/compiler.py --tout

Verifie pour chaque PDF : 1 seule page, aucun champ [[...]] oublie.
Code de sortie 0 si tout est OK, 1 sinon.
"""
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FICHIERS = ("cv.tex", "lettre.tex")
PLACEHOLDER = re.compile(r"\[\[.*?\]\]")


def compiler_un(tex: Path):
    erreurs = []
    texte = tex.read_text(encoding="utf-8", errors="replace")
    restes = PLACEHOLDER.findall(texte)
    if restes:
        erreurs.append(f"champs non remplis : {', '.join(sorted(set(restes)))}")
    try:
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             tex.name],
            cwd=tex.parent, capture_output=True, text=True, timeout=180,
        )
    except FileNotFoundError:
        return tex, ["pdflatex introuvable (installer MiKTeX / TeX Live)"]
    except subprocess.TimeoutExpired:
        return tex, ["pdflatex a depasse 180 s"]
    log = r.stdout + r.stderr
    m = re.search(r"Output written on .*?\((\d+) page", log)
    if r.returncode != 0 or not m:
        err = [l for l in log.splitlines() if l.startswith("!")][:3]
        erreurs.append("erreur LaTeX : " + (" | ".join(err) or "voir le .log"))
    elif int(m.group(1)) != 1:
        erreurs.append(f"{m.group(1)} pages au lieu de 1 : raccourcir")
    for ext in (".aux", ".out", ".log"):
        tex.with_suffix(ext).unlink(missing_ok=True)
    return tex, erreurs


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv == ["--tout"]:
        dossiers = sorted(p for p in Path("candidatures").glob("*") if p.is_dir())
    else:
        dossiers = [Path(a) for a in argv]
    cibles = [d / f for d in dossiers for f in FICHIERS if (d / f).exists()]
    if not cibles:
        print("Aucun cv.tex / lettre.tex trouve.")
        return 1
    if shutil.which("pdflatex") is None:
        print("pdflatex introuvable. Installer MiKTeX (Windows), MacTeX (macOS) "
              "ou texlive-latex-extra texlive-lang-french (Linux).")
        return 1
    echec = 0
    with ThreadPoolExecutor(max_workers=4) as ex:
        for tex, erreurs in ex.map(compiler_un, cibles):
            if erreurs:
                echec += 1
                print(f"[ERREUR] {tex}: " + " ; ".join(erreurs))
            else:
                print(f"[OK]     {tex.with_suffix('.pdf')}")
    print(f"\n{len(cibles) - echec}/{len(cibles)} fichiers OK")
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
