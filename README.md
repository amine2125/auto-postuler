# auto-postuler

Un assistant IA postule à des stages pour toi : il adapte ton CV et ta lettre à chaque offre, fait les PDF, dépose la candidature et tient un suivi Excel. Marche avec le portail de stages de n'importe quelle école (Poly, ETS, Concordia…), LinkedIn et les sites d'entreprise.

## Comment l'utiliser

Tu ne configures rien : l'assistant installe tout lui-même.

1. Ouvre ton assistant IA (Claude Code, Gemini CLI, Codex…).
2. Joins ton CV et écris :

   > Installe et configure https://github.com/amine2125/auto-postuler pour moi. Voici mon CV.

3. Réponds à ses quelques questions (nom, école, disponibilités…). C'est tout : ensuite, dis *« Postule aux nouvelles offres de stage »*.

Le dossier [`postulation/`](postulation/README.md) contient le skill et les modèles que l'assistant utilise.

## À savoir

- Il ne touche jamais aux captchas, aux mots de passe ni aux comptes. Sur LinkedIn, il peut postuler seul, mais attention : LinkedIn peut restreindre un compte qui postule en rafale, donc il va doucement.
- Il apprend tes réponses aux formulaires et ne te les redemande pas.
- Tes infos restent dans **ton** dossier `postulation`. Ne le mets jamais sur un GitHub public.
