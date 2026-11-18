# auto-postuler

Un assistant IA postule à des stages pour toi : il adapte ton CV et ta lettre à chaque offre, fait les PDF, dépose la candidature et tient un suivi Excel. Marche avec le portail de stages de n'importe quelle école (Poly, ETS, Concordia…), LinkedIn et les sites d'entreprise.

## Démarrer en 3 étapes

1. **Installe** [Python 3](https://www.python.org/downloads/) (puis `pip install openpyxl`) et LaTeX ([MiKTeX](https://miktex.org/download) sur Windows).
2. **Télécharge** ce dépôt et copie le dossier **`postulation`** où tu veux (ex. dans Documents).
3. **Ouvre ton assistant IA dans ce dossier** (Claude Code, Gemini CLI, Codex…), mets ton CV dedans et écris :

   > Configure le skill postuler-stages avec mon CV

L'assistant remplit tout (CV, lettres, profil) et te pose les quelques questions qui manquent. Ensuite : *« Postule aux nouvelles offres de stage »*.

Détails et exemples : [`postulation/README.md`](postulation/README.md).

## À savoir

- Il ne touche jamais aux captchas, aux mots de passe ni aux comptes. Sur LinkedIn, c'est toi qui cliques « Postuler ».
- Il apprend tes réponses aux formulaires et ne te les redemande pas.
- Tes infos restent dans **ton** dossier `postulation`. Ne le mets jamais sur un GitHub public.
