# auto-postuler 🎓📨

Un **skill pour assistant IA** qui postule à des stages pour toi : il lit l'offre, adapte ton CV et ta lettre (LaTeX), compile les PDF, dépose la candidature et tient un suivi Excel. Il fonctionne pour **n'importe quelle école** (Polytechnique Montréal, ETS, Concordia, UdeM…) : tout ce qui est personnel est stocké chez toi, rien n'est dans ce dépôt.

## Ce que tu as besoin

| Quoi | Pourquoi |
|---|---|
| Un **assistant IA capable d'agir** (l'assistant, Gemini, ChatGPT… avec accès à des fichiers, à un terminal et à un navigateur) | exécute le skill |
| Un **outil de navigation web** pour l'assistant (extension de navigateur, navigateur intégré, automatisation) | lire les offres et déposer les fichiers dans *ton* navigateur déjà connecté |
| **Python 3** + `pip install openpyxl` | scripts de compilation et de suivi |
| **LaTeX** : MiKTeX (Windows), MacTeX (macOS), `texlive-latex-extra texlive-lang-french` (Linux) | génère les PDF |
| Ton **CV** (PDF, Word, LaTeX ou simple texte) | base de toutes tes candidatures |

Pas de dossier, pas d'Excel, pas de profil à préparer : **l'assistant les crée au premier lancement.**

## Installation (2 minutes)

### Option A : l'assistant s'en occupe
Donne ce message à ton assistant (il doit pouvoir lire des fichiers et utiliser un terminal) :

> Récupère le skill `postuler-stages` depuis https://github.com/amine2125/auto-postuler (dossier `skills/postuler-stages`), installe-le comme skill ou instructions permanentes, puis lance-le pour faire l'installation complète (dossier `postulation`, scripts, profil, mon CV).

### Option B : à la main
```bash
git clone https://github.com/amine2125/auto-postuler
```
Puis selon ton assistant :
- **l'assistant Code** : copie `skills/postuler-stages` dans `~/.claude/skills/`. Sur claude.ai : zip du dossier, importé dans les réglages des skills.
- **Gemini, ChatGPT ou autre** : pas de format « skill » commun. Colle le contenu de `skills/postuler-stages/SKILL.md` comme instructions du projet / du Gem / du GPT (ou dans le fichier d'instructions de ton outil, ex. `GEMINI.md`, `AGENTS.md`), et mets le dossier `skills/postuler-stages` à portée de l'assistant pour qu'il copie les scripts et gabarits.

## Premier lancement : ce que l'assistant fait avec toi

Dis simplement : **« lance le skill postuler-stages »** (ou « suis les instructions de postuler-stages »). Comme tu n'as encore rien, l'assistant passe par la **Phase 0 (installation)** :

1. **Crée ton dossier `postulation/`** (par défaut dans `Documents/`) avec `base/`, `scripts/`, `candidatures/`, `suivi/`.
2. **Installe les scripts** (`compiler.py`, `suivi.py`) et vérifie Python, openpyxl et LaTeX.
3. **Te pose tes questions UNE seule fois** (nom, coordonnées, école, programme, dates d'études, autorisation de travail, langues, disponibilité, liens LinkedIn/GitHub…) et les range dans `profil.json`. Les questions de diversité sont facultatives.
4. **Te demande le nom et l'adresse du portail de stages de ton école** (La Ruche pour Poly, le portail de l'ETS, celui de Concordia…). Si tu n'en as pas, LinkedIn et les sites d'entreprise suffisent.
5. **Prend ton CV** et le met en format LaTeX à ton nom (en gardant ton contenu, rien d'inventé), en français et en anglais. Tu valides le rendu une fois ; ensuite le format ne bouge plus jamais.
6. **Prépare tes lettres de base** FR/EN.

Après ça, il enchaîne sur ta première demande, par exemple : *« postule à 10 stages en génie logiciel pour l'été 2027 »*.

## Comment ça marche ensuite

```
Collecte → Rédaction → Compilation → Confirmation → Dépôt → Suivi
```

1. **Collecte** : cherche sur le portail de ton école (filtres : Stage, tes disciplines, sessions *à venir* seulement), ignore les doublons et les offres expirées.
2. **Rédaction** : pour chaque offre, copie ton CV et ta lettre de base et les adapte.
   - CV : projets réordonnés, quelques puces reformulées *seulement si c'est vrai*, compétences alignées sur l'offre (maximum 3 ajouts, notés dans « À apprendre » pour que tu les révises avant l'entrevue).
   - Lettre : paragraphes réécrits avec des éléments précis de l'offre, 1 page.
3. **Compilation** : `compiler.py` vérifie 1 page et aucun champ `[[...]]` oublié.
4. **Confirmation** : un tableau du lot, un seul « je dépose ? » (sauté si tu as déjà dit « postule »).
5. **Dépôt** : sur le portail de l'école ou le site de l'entreprise (Workday, tal.net, BambooHR…), à partir de ton profil.
6. **Suivi** : `suivi/candidatures.xlsx` (statuts : Prêt, Postulé, À compléter, Entrevue, Refusé, Offre, Retirée).

Dis aussi : *« J'ai une entrevue chez X »* → statut mis à jour + questions probables + simulation d'entrevue.

## 🧠 Il apprend de toi

Chaque fois qu'un formulaire pose une question nouvelle ou que tu corriges une réponse, l'assistant l'enregistre dans `profil.json` > `reponses_apprises` et **ne te la redemande plus jamais**. Il retient aussi comment fonctionne chaque portail. Il t'interrompt seulement pour un vrai blocage.

## Garde-fous

- **LinkedIn** : il prépare tout mais c'est **toi** qui cliques « Postuler » (les bots sont interdits, ton compte pourrait être restreint).
- **reCAPTCHA** : jamais coché par l'assistant, il te le demande.
- **Comptes et mots de passe** : jamais créés ni saisis par l'assistant.
- **Offres expirées** : jamais envoyées.
- **Honnêteté** : aucun fait ni projet inventé ; les compétences ajoutées sont signalées.
- Cookies non essentiels : refusés.

## Structure

```
skills/postuler-stages/
  SKILL.md                  # les instructions de l'assistant (installation + 6 phases + règles)
  scripts/compiler.py       # compile cv.tex / lettre.tex, vérifie 1 page
  scripts/suivi.py          # suivi Excel
  templates/                # CV et lettres de base FR/EN, profil.example.json
```

Ce qui sera créé **chez toi** : `postulation/` avec `base/`, `candidatures/`, `suivi/candidatures.xlsx`, `profil.json`.

## 🔒 Confidentialité

Ton dossier `postulation/` contient tes infos personnelles (adresse, téléphone, CV…). Ne le publie jamais sur GitHub. Le `.gitignore` de ce dépôt l'exclut déjà.

## Contribuer

Tu as un piège à signaler ou un portail d'école à documenter (ETS, Concordia, UdeM…) ? l'assistant te proposera la mise à jour du skill en fin de session, ou ouvre une pull request. **Ne mets jamais de données personnelles dans le skill.**
