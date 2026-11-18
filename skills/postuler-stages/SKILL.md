---
name: "postuler-stages"
description: "Postule aux stages d'un étudiant (portail de stages de son école, LinkedIn, sites d'entreprise) : installe son dossier de travail au premier lancement, adapte son CV et sa lettre LaTeX à chaque offre, compile les PDF, dépose la candidature et tient un suivi Excel. Apprend de ses réponses au fil du temps."
---

# Postuler aux stages

Objectif : faire beaucoup de candidatures vite, sans gaspiller de tokens. L'IA rédige. Les scripts compilent et tiennent le suivi. Le navigateur sert à lire les offres et à déposer les fichiers.

Ce skill est générique : il sert à n'importe quel étudiant (Polytechnique Montréal, ETS, Concordia, UdeM, etc.). Tout ce qui est personnel vit dans `profil.json`, jamais dans ce fichier.

## Phase 0 — Installation (premier lancement)
Au début de CHAQUE session, vérifie si le dossier de travail `postulation/` existe avec `profil.json` rempli. Si oui, passe à la Phase 1. Sinon, fais l'installation ci-dessous, en posant les questions groupées en un seul message, puis continue directement avec la demande de l'utilisateur.

1. **Dossier de travail** : demande où le créer (par défaut `Documents/postulation`). Si l'assistant tourne dans le cloud, demande à l'utilisateur de lui donner accès à son dossier (ajout à la conversation, upload ou équivalent). Crée :
   ```
   postulation/
     base/  scripts/  candidatures/  suivi/  profil.json
   ```
2. **Scripts** : copie `scripts/compiler.py` et `scripts/suivi.py` de ce skill dans `postulation/scripts/`. Vérifie `python --version`, installe `openpyxl` (`pip install openpyxl`) et un moteur LaTeX (`pdflatex` : MiKTeX sous Windows, MacTeX sous macOS, `texlive-latex-extra texlive-lang-french` sous Linux). Teste avec `python scripts/suivi.py`.
3. **Profil** : copie `templates/profil.example.json` en `postulation/profil.json`. Remplis-le en posant les questions manquantes en un seul message : identité, coordonnées, liens LinkedIn/GitHub, école et programme, dates d'études, autorisation de travail, citoyenneté, langues, disponibilité, salaire souhaité, expériences à saisir dans les formulaires. Les questions d'équité/diversité (EDI) sont facultatives : ne remplis que ce que la personne dit ; sinon « Je préfère ne pas répondre » (ne jamais deviner « Non »).
4. **Portail de stages de l'école** : demande son nom et son URL (ex. La Ruche pour Poly Montréal, le portail de stages de l'ETS, celui de Concordia…). Note-les dans `profil.json` > `portails`, avec les filtres habituels (type Stage, discipline, sessions futures seulement). Pas de portail : LinkedIn et les sites d'entreprise suffisent.
5. **CV de l'utilisateur** : demande son CV actuel (PDF, Word ou LaTeX) ou son texte.
   - S'il est déjà en `.tex` : copie-le tel quel en `base/cv_en.tex` (ou `cv_fr.tex`) et garde son format.
   - Sinon : pars de `templates/cv_en.tex` / `cv_fr.tex`, remplace les champs `[[...]]` et les entrées d'exemple par SON contenu (rien d'inventé), et compile pour vérifier qu'il tient sur 1 page. Montre le PDF et fais valider le rendu.
   - Fais l'autre langue (FR ↔ EN) par traduction fidèle. Garde un `base/cv_<langue>_reference.pdf`.
   - À partir de maintenant, ces CV de base sont la source de vérité : le format ne change plus jamais.
6. **Lettres de base** : copie `templates/lettre_fr.tex` et `templates/letter_en.tex` dans `base/`, remplis seulement les champs fixes (nom, coordonnées, école, programme). Garde `[[Entreprise]]`, `[[Poste]]`, `[[Session]]`, `[[Date]]` et les paragraphes `ADAPTER` pour chaque candidature.
7. **Relevé de notes** : si un portail le demande, demande à l'utilisateur de glisser son relevé dans `base/releve_notes.pdf`.
8. **Confidentialité** : rappelle une fois que `postulation/` contient des données personnelles et ne doit jamais être publié sur GitHub.
9. Confirme en 3 lignes que tout est prêt, puis enchaîne.

## RÈGLE N°1 — AUTONOMIE ET AUTO-APPRENTISSAGE
L'utilisateur ne veut PAS être interrompu pour une question dont la réponse est connue ou déductible.
1. **Ne t'arrête pas et ne fais pas de rapport d'étape.** Un message à l'utilisateur n'est permis que pour un blocage réel (compte à créer, captcha, fichier introuvable) ; une ligne, une seule fois, pendant que tu continues le reste.
2. **Avant toute question, cherche la réponse**, dans cet ordre : (a) `profil.json`, y compris `reponses_apprises` ; (b) l'offre, les CV de base, les anciennes candidatures dans `candidatures/` ; (c) son LinkedIn et son GitHub ; (d) le portail de l'école (documents, relevé) ; (e) le bon sens.
3. **Quand tu dois choisir**, prends l'option la plus raisonnable, note-la en une ligne dans le résumé final et continue.
4. **AUTO-APPRENTISSAGE — apprends au fur et à mesure.** Chaque fois qu'un formulaire pose une question nouvelle, ou que l'utilisateur donne ou corrige une réponse, ajoute-la aussitôt dans `profil.json` > `reponses_apprises` (clé claire, valeur courte, ex. `"deja_employe_par_l_entreprise": "Non"`). Au début de chaque candidature, relis cette section et réutilise les réponses sans les redemander. Une correction de l'utilisateur écrase l'ancienne valeur.
5. **Apprends aussi les portails** : quand tu comprends comment un site ou un portail fonctionne (filtres, champs d'upload, piège), note-le dans `profil.json` > `portails` > `notes`.
6. En fin de session, si tu as appris une règle générale ou un piège qui servirait à tout étudiant (pas une donnée personnelle), propose de mettre à jour ce skill (donne le SKILL.md complet à jour, ou ouvre une pull request sur le dépôt du skill), sans attendre qu'on te le demande. Ne mets jamais d'information personnelle dans le skill.

## Dossier de travail
- `base/cv_fr.tex`, `base/cv_en.tex` : CV de base, format figé. `base/cv_<langue>_reference.pdf` : rendu de référence.
- `base/lettre_fr.tex`, `base/letter_en.tex` : lettres de base, champs `[[...]]` et paragraphes `ADAPTER`.
- `base/releve_notes.pdf` : relevé de notes réutilisé pour les dépôts qui en demandent un.
- `scripts/compiler.py` : compile en parallèle, vérifie 1 page et aucun `[[...]]` restant.
- `scripts/suivi.py` : gère `suivi/candidatures.xlsx` (`deja`, `ajouter`, `statut`, `liste`).
- `candidatures/AAAA-MM-JJ_Entreprise_Code/` : un dossier par candidature (`offre.txt`, `cv.tex`, `lettre.tex`, PDF, `candidature.json`).
- `profil.json` : identité, coordonnées, disponibilité, portails, `reponses_apprises`.

Lance les scripts depuis `postulation/`. Si le moteur LaTeX manque, compile dans l'espace de travail cloud puis recopie les PDF dans le dossier de la candidature.

## Règles de vitesse
1. Lis les pages en texte (extraction du texte ou de l'arbre d'accessibilité de la page, recherche d'éléments). Capture d'écran seulement si une action échoue.
2. Travaille par lot, une phase à la fois pour toutes les offres.
3. Copie la base, puis fais des modifications ciblées. Ne réécris jamais un `.tex` en entier : un petit script Python qui remplace des chaînes exactes (une seule occurrence chacune) pour tout le lot est le plus rapide.
4. Lis les fichiers de base une seule fois par session.
5. Ne commente pas chaque étape. Un seul tableau récapitulatif à la fin.

## Phase 1 — Collecte
**Portail de l'école** (avec un outil de navigation web piloté par l'assistant : extension de navigateur, navigateur intégré ou automatisation, session de l'utilisateur déjà connectée) :
- Si une page de connexion apparaît, demande à l'utilisateur de se connecter. Ne saisis jamais son mot de passe.
- Applique les filtres de `profil.json` : type Stage, ses disciplines, **sessions à venir seulement** (jamais la session en cours ni une passée). Si une case ne réagit pas, clique son libellé ; vérifie l'état réel des cases avec JavaScript.
- Lis la liste des résultats une seule fois. Vérifie les doublons en une commande : `python scripts/suivi.py deja <code1> <code2> …`.
- Écarte les offres déjà dans le suivi et celles sans rapport avec ses disciplines. Préfère une offre par entreprise par lot, sauf demande contraire.
- **Offres expirées : ne postule jamais** (date limite avant aujourd'hui, état différent de « ouvert », ou site externe qui indique que l'offre est fermée). Dans le doute, demande.
- Ouvre chaque offre en cliquant depuis la liste : beaucoup de portails lient l'URL de détail à la session (checksum), ne la modifie jamais. Lis la page avec l'extraction de texte ou JavaScript (sortie tronquée vers 1000 caractères : découpe).
- Si l'offre demande de postuler sur le site de l'entreprise, note le lien dans `offre.txt` et `lien` (Phase 5).
- Enregistre le texte utile dans `candidatures/<AAAA-MM-JJ>_<Entreprise>_<code>/offre.txt`, URL sur la première ligne.

**LinkedIn et autres sites** : même chose, à partir de la page de l'offre ou du texte collé. Si l'utilisateur ouvre une offre et demande d'y postuler, rouvre l'URL dans un nouvel onglet et traite la candidature de bout en bout ; réutilise le dossier existant s'il y en a un.

## Phase 2 — Rédaction (par offre)
**Langue** : anglais si l'offre est en anglais, si l'entreprise le demande, ou si c'est une grande entreprise internationale. Sinon français.

### CV : même format que le CV de base
- Copie `base/cv_fr.tex` ou `base/cv_en.tex` dans `cv.tex`.
- **Ne touche jamais** au préambule, aux commandes, marges, polices, en-tête, ordre des sections, ni au nombre d'entrées et de puces. Une page.
- Modifications permises, de la plus sûre à la moins sûre :
  1. Réordonner les projets (le plus pertinent en premier) et les puces d'une entrée.
  2. Reformuler 2 à 5 puces avec le vocabulaire de l'offre, **seulement si c'est vrai**. Test : si un recruteur demande « où as-tu utilisé X dans ce projet ? », l'utilisateur doit pouvoir répondre. Pas de mot-clé collé en fin de puce, pas de puce inventée.
  3. Dans les compétences techniques, mettre en tête ce que l'offre demande.
- **Coller aux exigences** : compare l'offre au CV. L'utilisateur peut vouloir couvrir les exigences qu'il apprendra avant l'entrevue ; demande-lui son préférence UNE fois à l'installation et note-la dans `profil.json` > `preferences` > `ajouter_competences_exigees` (par défaut : oui, jusqu'à 3 compétences, jamais plus).
  - **Exigé** : ajoute l'élément manquant dans la bonne ligne de compétences. **Atout** : au plus 2 ajouts proches du profil. Plafond : 3 nouvelles compétences par CV ; signale le reste.
  - Jamais dans les puces d'expérience ou de projet : seulement dans les compétences.
  - Note chaque ajout dans `a_apprendre`. Si l'offre ne cite des technos qu'« à titre d'exemple », n'ajoute rien.
- Au plus 6 mots-clés ajoutés au total. Un CV naturel vaut mieux qu'un CV bourré de mots-clés.

### Lettre
- Copie la lettre de base dans `lettre.tex`, sans changer le format.
- Remplace tous les `[[...]]`. Réécris seulement les paragraphes `ADAPTER`, avec des éléments précis de l'offre (mission, produits, responsabilités).
- N'invente rien sur l'entreprise. Pas de ligne « Objet ». 250 à 350 mots, une page.

### candidature.json
Dans le dossier de la candidature : `date`, `entreprise`, `poste`, `source`, `code`, `session`, `langue` (FR/EN), `statut` à `"Prêt"`, `date_limite`, `lien`, `mots_cles`, `a_apprendre`, `changements` (une phrase). Format exact : `python scripts/suivi.py`.

## Phase 3 — Compilation
Une seule commande : `python scripts/compiler.py candidatures/<d1> candidatures/<d2> …` ou `--tout`. Corrige (`[[...]]` oublié, CV sur 2 pages : raccourcis une reformulation) et relance. Vérification visuelle (PDF en image) sur un CV par lot, surtout si des projets ont été réordonnés.

## Phase 4 — Confirmation (une seule fois par lot)
Tableau court : # | Entreprise | Poste | Session | Langue | Date limite | À apprendre. Demande : « Je dépose ces N candidatures ? ». Ne soumets rien sans ce oui.
**Exception** : si l'utilisateur a déjà dit de postuler/déposer (« postule à 10 offres », « dépose tout »), ne redemande pas. Une fois le go donné dans la conversation, ne le redemande plus.

## Phase 5 — Dépôt
**Portail de l'école** : ouvre le détail depuis la recherche, repère les champs (recherche d'éléments : champs de fichier CV et lettre, bouton d'envoi), téléverse les PDF avec l'outil de téléversement de fichiers du navigateur, en utilisant le chemin absolu exact (ne clique jamais le bouton de fichier : il ouvre une fenêtre système invisible). Refais la recherche d'éléments sur CHAQUE page de détail (les `ref` changent). Relevé : sélectionne-le dans le menu (JavaScript : change la valeur du `select` puis `dispatchEvent(new Event('change',{bubbles:true}))`). Clique « Postuler », vérifie le message de succès, statut `"Postulé"`. Si l'offre exige autre chose, applique la règle n°1 ; n'invente jamais un fait ; sinon statut `"À compléter"`.

**Sites d'entreprise** : postule de bout en bout.
1. Cookies : refuse les non essentiels, à chaque page si la bannière revient.
2. Offre fermée → statut `"Retirée"` avec commentaire.
3. Remplis avec `profil.json` et `reponses_apprises`, téléverse CV (et lettre si demandée), soumets, vérifie le succès.
4. Info manquante : règle n°1, option raisonnable, note-la, **ajoute-la à `reponses_apprises`**.
5. Création de compte ou mot de passe : ne le fais jamais ; demande à l'utilisateur de le faire, statut `"À compléter"`, continue avec les autres offres.
6. **reCAPTCHA** : ne le coche jamais. Remplis tout, laisse la page ouverte, demande à l'utilisateur de le cocher, puis soumets.
7. **Consentements obligatoires** (vie privée, conditions) : accepte-les seulement si l'utilisateur l'a autorisé une fois (note-le dans `profil.json` > `preferences`) ; sinon demande une seule fois puis mémorise. Signale-les dans le message final.
8. Champs obligatoires sans info : `profil.json` (`salaire_souhaite`, site par défaut = GitHub). « Petit mot de présentation » : 3–4 phrases vraies tirées du CV.
9. Relis la page entière avant de soumettre (un champ obligatoire peut se cacher au milieu).
10. Remplis les champs texte avec l'outil de saisie de formulaire et les références d'éléments plutôt qu'en cliquant/tapant. Pour le téléversement, il faut la référence du vrai `input type=file`.
11. Listes déroulantes (select2) : retrouve le vrai `<select>`, puis choisis l'option avec le libellé exact. Les champs conditionnels n'apparaissent qu'après le choix précédent.
12. Formulaires multi-pages : « Save and Continue » enregistre la page ; recharger sans l'avoir fait perd les fichiers.

**LinkedIn** : **ne soumets jamais automatiquement** (interdit aux bots, risque de restriction du compte). Prépare les fichiers ; c'est l'utilisateur qui clique « Postuler ». Statut `"Prêt"`.

## Phase 6 — Suivi
Mets à jour le statut dans chaque `candidature.json`, puis : `python scripts/suivi.py ajouter candidatures/*/candidature.json`. Si l'Excel est ouvert, demande de le fermer.

Message final : un tableau (entreprise, poste, statut), la liste « À apprendre avant les entrevues », les choix que tu as faits toi-même (une ligne chacun), les nouvelles réponses mémorisées, et ce que l'utilisateur doit faire lui-même (compte, captcha). Rien d'autre.

## Autres demandes
- « J'ai une entrevue chez X » : `python scripts/suivi.py statut <code> Entrevue` ET `"statut": "Entrevue"` dans le `candidature.json` (sinon le prochain `ajouter` le remet à « Postulé »). Statuts : Prêt, Postulé, À compléter, Entrevue, Refusé, Offre, Retirée. Relis `offre.txt`, résume le poste, prépare questions probables et réponses fondées uniquement sur le CV de base, propose une simulation.
- Nouveau CV : mets à jour `base/cv_en.tex` et `base/cv_fr.tex` en gardant le format, et remplace le PDF de référence.

## Pièges connus
- Navigue par clics : les URL de détail sont souvent liées à la session.
- `ERR_FILE_NOT_FOUND` au téléversement = mauvais chemin : utilise le chemin absolu exact.
- Les cases de dépôt peuvent être étiquetées « (français) » même pour un dépôt en anglais : mets-y quand même les PDF anglais.
- Taille des PDF : souvent < 1000 Ko sur les portails d'école, < 512 Ko sur tal.net.
- `javascript_tool` bloque la sortie qui contient une URL avec paramètres : lis avec l'extraction de texte. Sortie JS tronquée vers 1000 caractères.
- Comptes/codes obligatoires (Workday, tal.net, ADP…) : statut « À compléter », demande une seule fois, continue.
- Workday : Échap revient en arrière ; sélectionner dans une liste fait défiler la page (refais la recherche d'éléments) ; les champs d'études demandent une recherche puis Entrée.
- BambooHR : reCAPTCHA, laisse la page ouverte.
- Offres sans formulaire, non logicielles, fédérales/municipales ou de site inatteignable : saute-les et note-le.
- tal.net : l'extraction de texte est souvent vide, utilise l'arbre d'accessibilité.

Quand tu résous un nouveau piège général, propose de l'ajouter ici (règle n°1.6).
