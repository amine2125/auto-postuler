---
name: postuler-stages
description: Postule à des offres de stage (portail de stages de l'école de l'utilisateur, par ex. La Ruche à Polytechnique Montréal ; LinkedIn ; sites d'entreprise) en adaptant le CV et la lettre LaTeX de l'utilisateur à chaque offre, en compilant les PDF, en déposant et en tenant un suivi Excel. À utiliser aussi pour la configuration initiale (« configure le skill », « voici mon CV ») et pour mettre à jour le statut d'une candidature.
---

# Postuler aux stages

Objectif : faire beaucoup de candidatures vite, sans gaspiller de tokens. L'IA rédige. Les scripts compilent et tiennent le suivi. Le navigateur sert seulement à lire les offres et à déposer les fichiers.

## RÈGLE N°1 — AUTONOMIE ET AUTO-APPRENTISSAGE
L'utilisateur ne veut PAS être interrompu pour une question dont la réponse est connue ou déductible.
1. **Ne t'arrête pas et ne fais pas de rapport d'étape.** Un message à l'utilisateur n'est permis que pour un blocage réel (compte à créer, captcha, fichier introuvable) : une ligne, une seule fois, pendant que tu continues le reste.
2. **Avant toute question, cherche la réponse**, dans cet ordre : (a) `profil.json`, y compris `reponses_apprises` ; (b) l'offre, les CV de base, les anciennes candidatures dans `candidatures/` ; (c) son LinkedIn et son GitHub ; (d) le portail de l'école (documents, relevé) ; (e) le bon sens.
3. **Quand tu dois choisir**, prends l'option la plus raisonnable, note-la en une ligne dans le résumé final et continue.
4. **AUTO-APPRENTISSAGE.** Chaque fois qu'un formulaire pose une question nouvelle, ou que l'utilisateur donne ou corrige une réponse, ajoute-la aussitôt dans `profil.json` > `reponses_apprises` (clé claire, valeur courte, ex. `"deja_employe_par_l_entreprise": "Non"`). Au début de chaque candidature, relis cette section et réutilise les réponses sans les redemander. Une correction de l'utilisateur écrase l'ancienne valeur. Questions d'équité/diversité (EDI) : ne réponds que ce que l'utilisateur a déjà divulgué, sinon « Je préfère ne pas répondre » (ne devine jamais « Non »).
5. **Apprends aussi les portails** : quand tu comprends comment un site ou un portail fonctionne (filtres, champs de dépôt, piège), note-le dans `profil.json` > `portails` > `notes`.
6. En fin de session, si tu as appris une règle générale ou un piège utile à tout étudiant (jamais une donnée personnelle), propose de mettre à jour ce skill (donne le `SKILL.md` à jour ou ouvre une pull request sur le dépôt du skill).

## Préparation automatique (l'utilisateur ne configure RIEN lui-même)
Tu installes et règles tout toi-même. L'utilisateur ne fait que deux choses : répondre à quelques questions et joindre son CV. Ne lui donne jamais une liste d'étapes techniques à exécuter ; fais-les, et ne le sollicite que pour un blocage réel (mot de passe administrateur, installation refusée), en une ligne.
1. **Dossier** : si le dossier `postulation` (celui avec `profil.json`, `base/`, `scripts/`) n'est pas déjà ton dossier de travail, récupère-le (clone ou copie du dépôt du skill) dans `Documents/postulation` et travaille-y. Toutes les commandes se lancent depuis ce dossier.
2. **Outils** : détecte le système, puis vérifie `python --version`, `python -c "import openpyxl"` et `pdflatex --version`. Installe ce qui manque avec le gestionnaire du système : Windows `winget install Python.Python.3.12`, `winget install MiKTeX.MiKTeX` ; macOS `brew install python` et `brew install --cask mactex-no-gui` ; Linux `apt install python3-pip texlive-latex-extra texlive-lang-french` ; puis `pip install openpyxl`. Pour MiKTeX, autorise l'installation automatique des paquets manquants. Relance les vérifications et corrige jusqu'à ce que `python scripts/suivi.py` et `python scripts/compiler.py` fonctionnent.
3. **Navigateur** (phases 1 et 5) : vérifie que tu disposes d'un outil de navigateur (ouvrir une page, lire son texte, JavaScript, remplir un champ, téléverser dans un `input type=file`, cliquer), par exemple un serveur MCP Playwright ou Chrome DevTools. S'il manque, installe-le et branche-le toi-même si ton environnement le permet. Sinon, fonctionne sans : fais les phases 2, 3, 4 et 6 à partir des offres que l'utilisateur colle, puis donne-lui la liste des PDF à déposer. Dans les deux cas, l'utilisateur doit être connecté lui-même aux sites dans ce navigateur.
4. Ne refais ces vérifications qu'à la première session ou si une commande échoue.

## Phase 0 — Configuration (la première fois seulement)
Si `profil.json` a un `prenom` vide, ou s'il reste des `[[MOI: ...]]` dans `base/`, le skill n'est pas encore configuré. Avant toute candidature, fais la préparation automatique ci-dessus, puis :
1. Demande en UN seul message : (a) de joindre son CV actuel (PDF, Word ou texte collé) et (b) les quelques réponses dont tu as besoin (voir l'étape 4). Si le CV est déjà fourni, lis-le sans le redemander.
2. Remplis `base/cv_fr.tex` et `base/cv_en.tex` : remplace chaque `[[MOI: ...]]` par ses vraies infos. Garde le préambule et les commandes `\experience`, `\projet`, `\entre` tels quels. Ajoute ou retire des entrées et des puces pour coller à son vrai parcours (supprime une section vide). Les deux versions ont exactement les mêmes entrées et puces, traduites.
3. Remplis les `[[MOI: ...]]` de `base/lettre_fr.tex` et `base/letter_en.tex`, dont le paragraphe de réalisations par défaut (tiré du CV). Laisse tous les autres `[[...]]` : ils se remplissent pour chaque offre.
4. Remplis `profil.json` avec ce que le CV donne (nom, coordonnées, école, programme…). Demande en une seule fois ce qui manque pour les formulaires, ainsi que le nom et l'URL du portail de stages de son école (à noter dans `portails`) : civilité, adresse, pronoms, autorisation de travail, disponibilités, discipline recherchée, nom du relevé de notes sur La Ruche, etc.
5. Teste la compilation : crée `candidatures/_test_fr/` et `candidatures/_test_en/`. Copie-y le CV de base comme `cv.tex` et la lettre de base comme `lettre.tex` (en remplissant ses `[[...]]` avec des valeurs bidon). Lance `python scripts/compiler.py candidatures/_test_fr candidatures/_test_en` et corrige jusqu'à ce que tout tienne sur 1 page. Copie le CV anglais compilé en `base/cv_en_reference.pdf`, puis supprime les deux dossiers de test.
6. Montre le PDF du CV à l'utilisateur et demande s'il est fidèle à son vrai CV. Une fois validé, ce format est figé.

## Dossier de travail
- `base/cv_fr.tex`, `base/cv_en.tex` : CV de base, au format figé. `base/cv_en_reference.pdf` est le rendu de référence.
- `base/lettre_fr.tex`, `base/letter_en.tex` : lettres de base, avec des champs `[[...]]` et des paragraphes marqués `ADAPTER`.
- `scripts/compiler.py` : compile en parallèle et vérifie que tout tient sur 1 page et qu'il ne reste aucun `[[...]]`. Les PDF s'appellent `CV_Prenom_Nom.pdf`, `Lettre_Prenom_Nom.pdf` (ou `Resume_…`, `Cover_Letter_…` en anglais), d'après `profil.json`.
- `scripts/suivi.py` : gère l'Excel `suivi/candidatures.xlsx` (`deja`, `ajouter`, `statut`, `liste`).
- `candidatures/AAAA-MM-JJ_Entreprise_Code/` : un dossier par candidature (`offre.txt`, `cv.tex`, `lettre.tex`, les PDF, `candidature.json`).
- `profil.json` : coordonnées et réponses habituelles de l'utilisateur pour les formulaires. Quand il donne une nouvelle info dans le chat, ajoute-la à ce fichier pour les prochaines fois.

## Règles de vitesse
1. Lis les pages en texte (texte de la page, ou JavaScript qui renvoie `innerText`). Ne prends une capture d'écran que si une action échoue.
2. Travaille par lot, une phase à la fois pour toutes les offres, et non une offre de bout en bout puis la suivante.
3. Copie la base, puis fais des modifications ciblées. Ne réécris jamais un `.tex` en entier à la main : un petit script Python qui remplace des chaînes exactes (une seule occurrence chacune) pour tout le lot est le plus rapide.
4. Lis les fichiers de base une seule fois par session.
5. Ne commente pas chaque étape. Donne un seul tableau récapitulatif à la fin.

## Phase 1 — Collecte
**Portail de stages de l'école.** Consulte `profil.json` > `portails`. S'il est vide, demande une seule fois le nom et l'URL du portail (ETS, Concordia, UdeM, Polytechnique…), explore-le (filtres : type Stage, discipline de l'utilisateur, **sessions à venir seulement**), applique les règles générales ci-dessous (connexion par l'utilisateur, doublons, offres expirées, une offre par entreprise) et note ce que tu apprends dans `portails` > `notes`. Les détails suivants sont documentés pour **La Ruche (Polytechnique Montréal)** ; adapte-les aux autres portails.

**La Ruche** (https://laruche.polymtl.ca/, pour les étudiants de Polytechnique Montréal) :
- Si une page de connexion apparaît, demande à l'utilisateur de se connecter. Ne saisis jamais son mot de passe.
- Dans la recherche de mandats, coche le type Stage et la discipline de `profil.json` (`discipline_recherchee`, ex. Génie logiciel). Si elle est vide, demande-la.
- Coche **toutes les sessions à venir** proposées, c'est-à-dire toutes celles après la session en cours. Par exemple, en automne 2026 : Hiver 2027, Été 2027, Automne 2027, etc. Ne coche jamais la session en cours ni une session passée.
- Si une case ne réagit pas, clique sur son libellé texte. Chaque case recharge la page : coche-les une par une.
- Lis la liste des résultats une seule fois par session (le texte de la page donne 100 lignes `code titre employeur pays date_limite début durée type`). Vérifie les doublons en une seule commande : `python scripts/suivi.py deja <code1> <code2> …`.
- Écarte les offres déjà dans le suivi et les postes sans rapport avec le domaine de l'utilisateur. Préfère une offre par entreprise dans un même lot, sauf s'il en demande plus.
- **Offres expirées : ne postule jamais.** Une offre est expirée si sa date limite (colonne « Date Limite », format JJ-MM-AAAA) est avant aujourd'hui, si « État du mandat » n'est pas « Ouvert pour postulation », ou si le site externe affiche que l'offre est fermée (« No longer accepting applications », « Ce poste n'est plus disponible », page introuvable…). S'il n'y a aucune date limite, vérifie que la page indique encore qu'on peut postuler ; dans le doute, demande. Une offre dont la date limite est aujourd'hui passe en premier.
- Ouvre chaque offre retenue en cliquant depuis la liste. Ne modifie jamais les URL `detail-mandat` (le checksum `cs` provoque une erreur de session). Le plus rapide : exécuter ce JavaScript dans la page, qui clique le lien de la ligne contenant le code : `[...document.querySelectorAll('tr')].find(r=>r.innerText.includes('CODE')).querySelector('a').click()`, puis attendre 3 s.
- Ne lis JAMAIS tout le texte de la page juste après le clic : si la navigation n'est pas finie, tu reçois toute la liste (très long). Lis plutôt avec ce JavaScript : `document.querySelector('main').innerText.replace(/\s+/g,' ')`, découpé en morceaux de ~1000 caractères : description, puis exigences, puis la section après « Mon intérêt » (formulaire de dépôt OU « Instruction de postulation »).
- Pour revenir à la liste en gardant les filtres, clique le bouton « Retour » de la page de détail (JS : bouton dont le texte contient « Retour »). Le bouton Précédent du navigateur peut ramener au tableau de bord.
- Si l'offre affiche « … préfère ne pas recevoir votre candidature via La Ruche », note le lien externe dans `offre.txt` et `lien` : la candidature se fera sur le site de l'entreprise (phase 5).
- Enregistre le texte utile de l'offre dans `candidatures/<AAAA-MM-JJ>_<Entreprise>_<code>/offre.txt`, avec l'URL sur la première ligne.

**LinkedIn et autres sites** : même chose, à partir de la page de l'offre ou du texte collé par l'utilisateur. Sans code d'offre, utilise un code court unique (ex. `LI-` + l'identifiant dans l'URL).

## Phase 2 — Rédaction (pour chaque offre)
**Langue** : utilise l'anglais si l'offre est en anglais, si l'entreprise demande des documents en anglais, ou si c'est une grande entreprise internationale (Google, Microsoft…). Sinon, utilise le français.

### CV : même format que le CV de base
- Copie `base/cv_fr.tex` ou `base/cv_en.tex` dans `cv.tex`.
- **Ne touche jamais** au préambule, aux commandes, aux marges, aux polices, à l'en-tête, à l'ordre des sections ni au nombre d'entrées et de puces. Le PDF doit être identique au CV de base, à quelques mots près, et tenir sur une page.
- Modifications permises, de la plus sûre à la moins sûre :
  1. Réordonner les projets (le plus pertinent en premier) et les puces à l'intérieur d'une entrée.
  2. Reformuler 2 à 5 puces avec le vocabulaire de l'offre, **seulement si c'est vrai pour ce projet ou ce stage**. Test : si un recruteur demande « où as-tu utilisé X dans ce projet ? », l'utilisateur doit pouvoir répondre. Exemple de ce qu'il ne faut pas faire : mettre « IoT » dans un jeu d'échecs qui n'a rien à voir avec l'IoT. Pas de mot-clé collé en fin de puce, pas de nouvelle puce inventée.
  3. Dans les compétences techniques, mettre en tête ce que l'offre demande et ajouter les technos de l'offre que l'utilisateur connaît déjà.
- **Coller aux exigences** : compare la section « Exigences » de l'offre avec les compétences du CV. Le CV doit couvrir les exigences, même si l'utilisateur ne les maîtrise pas encore (il les apprend avant l'entrevue).
  - **Exigé** (langages, frameworks, outils listés comme requis) : ajoute chaque élément manquant dans la bonne ligne de « Technical Skills / Compétences techniques ».
  - **Atout / nice to have** : au plus 2 ajouts, les plus proches de son profil.
  - Plafond : au plus 3 compétences nouvelles par CV, pour ne pas abuser. Si l'offre en exige plus, garde les plus importantes et signale le reste.
  - Pas de plateforme propriétaire pointue ni de domaine sans lien avec son profil.
  - Jamais dans les puces d'expérience ou de projet : seulement dans les compétences.
  - Note chaque ajout dans `a_apprendre` (colonne « À apprendre » de l'Excel).
  - Quand l'offre ne cite des technos qu'« à titre d'exemple », n'ajoute rien.
  - Si l'utilisateur préfère ne rien ajouter qu'il ne connaît pas, respecte-le et note-le dans `profil.json` (`ajouter_competences_a_apprendre: non`).
- Ajoute au plus 6 mots-clés au total par CV. Un CV naturel vaut mieux qu'un CV bourré de mots-clés.

### Lettre
- Copie `base/lettre_fr.tex` ou `base/letter_en.tex` dans `lettre.tex`, sans changer le format.
- Remplace tous les `[[...]]`. Réécris seulement les paragraphes marqués `ADAPTER`, avec des éléments précis de l'offre : mission, produits, responsabilités.
- N'invente rien sur l'entreprise. Pas de ligne « Objet ».
- Utilise la session de l'offre. Vise 250 à 350 mots, sur une page.
- Si le CV de base montre qu'un stage marqué « présent » est terminé, adapte la phrase d'intro (voir le commentaire dans la lettre).

### candidature.json
Écris ce fichier dans le dossier de la candidature avec : `date`, `entreprise`, `poste`, `source`, `code`, `session`, `langue` (FR ou EN), `statut` à `"Prêt"`, `date_limite`, `lien`, `mots_cles`, `a_apprendre`, et `changements` (une phrase qui dit ce qui a changé et pourquoi). Le format exact s'affiche avec `python scripts/suivi.py`.

## Phase 3 — Compilation
Lance une seule commande : `python scripts/compiler.py candidatures/<d1> candidatures/<d2> …`, ou `--tout`.

Corrige les erreurs signalées, puis relance :
- `[[...]]` oublié : remplis-le.
- CV sur 2 pages : raccourcis une reformulation, sans toucher au format.

Ne fais une vérification visuelle (PDF en image) que sur un CV par lot (surtout si les projets ont été réordonnés), ou si un fichier a dû être corrigé deux fois.

## Phase 4 — Confirmation (une seule fois pour tout le lot)
Montre un tableau court : # | Entreprise | Poste | Session | Langue | Date limite | À apprendre. Indique où se trouvent les PDF.

Demande : « Je dépose ces N candidatures ? ». L'utilisateur peut répondre « oui », « oui sauf 2 et 5 », etc. Ne soumets rien sans ce oui.

**Exception** : si l'utilisateur a déjà dit de postuler ou de déposer (« lance le skill », « postule à 10 offres », « dépose tout »), ne redemande pas. Montre le tableau en passant et dépose directement. Une fois qu'il a donné le go dans la conversation, ne le redemande plus.

## Phase 5 — Dépôt
**Portail de l'école** (détaillé ci-dessous pour La Ruche ; autres portails : même logique, champs de fichier + bouton d'envoi, voir `portails` > `notes`), pour chaque candidature approuvée :
1. Ouvre le détail du mandat depuis la recherche (clic JS sur la ligne, puis attends 3 s). Si la session a expiré, relance la recherche.
2. Repère les champs de fichier : « Choisir un CV (français) », « Choisir une lettre (français) » et « Choisir un relevé », ainsi que le bouton « Postuler ». S'il n'y a que « Instruction de postulation » (« préfère ne pas recevoir votre candidature via La Ruche »), c'est un dépôt externe : passe à la section suivante.
3. Téléverse les PDF avec l'action de téléversement de ton outil de navigateur, directement dans le vrai `input type=file`, avec le chemin absolu du PDF dans le dossier de la candidature. Ne clique jamais sur le bouton de fichier : il ouvre une fenêtre système que tu ne peux pas contrôler. Les cases s'appellent « (français) » même pour une candidature en anglais : mets-y quand même les PDF anglais.
4. Pour le relevé, le menu est vide par défaut : choisis le relevé indiqué dans `profil.json` (`releve_de_notes`), sinon le plus récent, avec ce JavaScript : `const s=[...document.querySelectorAll('select')].find(x=>/Relevé/.test(x.innerText));const o=[...s.options].find(o=>/Relevé/.test(o.text));s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}))`. Vérifie en même temps que les deux fichiers sont bien attachés.
5. Clique sur « Postuler », attends 3 s, puis vérifie `success_msg` dans l'URL ou le message « La postulation a été effectuée avec succès ». Passe le statut à `"Postulé"`.
6. Si l'offre exige autre chose (questionnaire, document particulier), n'invente rien. Laisse le statut à `"À compléter"` et signale-le à la fin.

**Sites d'entreprise (lien externe, Zoho Recruit, BambooHR, Workday, etc.)** : l'utilisateur veut que tu postules toi-même.
1. Ouvre le lien. Bannière de cookies : refuse les cookies non essentiels (« Tout refuser », ou « Personnaliser » puis « Refuser » pour chaque catégorie avant de confirmer).
2. Si l'offre est fermée (« No longer accepting applications »), statut `"Retirée"` avec un commentaire, et passe à la suivante.
3. Remplis le formulaire avec `profil.json`, téléverse le CV (et la lettre s'il y a un champ), puis soumets et vérifie le message de succès. Statut `"Postulé"`.
4. S'il manque une info (adresse, disponibilités, question particulière…), applique la règle n°1 (cherche dans `profil.json`, le CV, LinkedIn, GitHub, choisis l'option raisonnable), remplis-la et **ajoute-la à `reponses_apprises`** ; ne demande à l'utilisateur qu'en dernier recours.
5. Si le site exige de créer un compte ou un mot de passe, ne le fais jamais toi-même, même si l'utilisateur donne les infos : demande-lui de créer le compte ou de se connecter dans le navigateur, mets le statut `"À compléter"`, puis continue avec les autres offres. Reprends quand il dit que c'est fait.
6. **reCAPTCHA / « I'm not a robot »** : ne le coche jamais, même sur demande. Remplis tout le formulaire, laisse la page ouverte et demande à l'utilisateur de cocher le captcha. Quand il dit l'avoir coché, clique « Submit ».
7. Case de consentement vie privée obligatoire pour envoyer : tu peux la cocher si l'utilisateur a autorisé les dépôts. Signale-le dans le message final.
8. Champs obligatoires sans info (salaire souhaité, site/portfolio) : utilise `profil.json` (`salaire_souhaite`, `site_web_par_defaut`), sinon règle n°1. Un « petit mot de présentation » se rédige à partir du CV (3–4 phrases vraies).
9. Relis la page entière (défile jusqu'en bas) avant de soumettre : un champ obligatoire peut se cacher au milieu (ex. « College/University » chez BambooHR). Les questions habituelles (autorisation de travail, résidence, disponibilité 40 h, pronoms, langue de contact) se répondent avec `profil.json`.
10. Remplis les champs texte en ciblant chaque champ (sélecteur ou référence d'élément) plutôt qu'en cliquant puis tapant : la page peut bouger et le texte atterrir dans le mauvais champ. Pour un téléversement, vise le vrai `input type=file`, pas le bouton visible.

**LinkedIn** : tu peux soumettre toi-même (candidature simplifiée « Easy Apply » ; si l'offre renvoie vers le site de l'entreprise, applique les règles des sites d'entreprise). **Mets en garde l'utilisateur une seule fois** (au premier dépôt LinkedIn de la session) : LinkedIn interdit l'automatisation et peut restreindre ou bannir le compte si on postule en rafale ; c'est son choix et son risque. Réduis ce risque : rythme humain (pause de quelques secondes à plusieurs dizaines de secondes entre deux actions), quelques dizaines de candidatures par jour au maximum (environ 15 à 25), arrête-toi et préviens au moindre avertissement, vérification ou captcha de LinkedIn, et ne contourne jamais une vérification. Statut `"Postulé"` après un succès confirmé.

## Phase 6 — Suivi
Mets à jour le statut dans chaque `candidature.json`, puis lance une seule commande : `python scripts/suivi.py ajouter candidatures/*/candidature.json`. Elle ajoute les nouvelles lignes ou met à jour les existantes. Si l'Excel est ouvert, demande à l'utilisateur de le fermer.

Message final : un tableau (entreprise, poste, statut) et la liste « À apprendre avant les entrevues ». Rien d'autre, sauf ce que l'utilisateur doit faire lui-même (compte à créer, captcha).

## Autres demandes
- « J'ai une entrevue chez X » : lance `python scripts/suivi.py statut <code> Entrevue`. Statuts possibles : Prêt, Postulé, À compléter, Entrevue, Refusé, Offre, Retirée.
- Nouveau CV : mets à jour `base/cv_en.tex` **et** `base/cv_fr.tex` en gardant exactement leur format, et remplace `base/cv_en_reference.pdf`.

## Pièges connus
### Généraux
- Comptes/codes obligatoires (Workday, tal.net, ADP, etc.) : statut « À compléter », demande une seule fois, continue avec les autres offres.
- Workday : Échap revient en arrière ; sélectionner dans une liste fait défiler la page (refais la recherche d'éléments) ; les champs d'études demandent une recherche puis Entrée.
- Formulaires multi-pages (tal.net) : « Save and Continue » enregistre la page ; recharger sans l'avoir fait perd les fichiers joints.
- Listes déroulantes (select2) : vise le vrai `<select>` et choisis le libellé exact de l'option ; les champs conditionnels n'apparaissent qu'après le choix précédent.
- Taille des PDF : souvent < 512 Ko (tal.net).
- Sortie JavaScript souvent tronquée vers 1000 caractères et parfois bloquée si elle contient une URL avec paramètres : lis plutôt le texte de la page.
- Offres sans formulaire, non logicielles, fédérales/municipales ou de site inatteignable : saute-les et note-le.

### La Ruche (Polytechnique Montréal)
- Entre toujours par https://laruche.polymtl.ca/ (racine). `/sp/` seul mène à une page de connexion Oracle APEX inutile.
- Les URL `detail-mandat` sont liées à la session et protégées par un checksum : navigue par clics.
- `ERR_FILE_NOT_FOUND` au téléversement veut dire que le chemin est mauvais : utilise le chemin absolu exact du PDF.
- Les cases de dépôt s'appellent « (français) » même pour une candidature en anglais.
- Les PDF doivent faire moins de 1000 Ko.
- Beaucoup d'offres renvoient vers le site de l'entreprise (voir la phase 5).

Quand tu résous un nouveau piège général, propose-le à la fin en une ligne (règle n°1.6).
