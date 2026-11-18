# Postulation automatique de stages

Un assistant IA (Claude Code, Gemini CLI, Codex…) adapte ton CV et ta lettre à chaque offre, fait les PDF, dépose la candidature et tient un suivi Excel.

## Installation (une seule fois)
1. Installe **Python 3** (`pip install openpyxl`) et **LaTeX** (MiKTeX sur Windows).
2. Mets ce dossier `postulation` où tu veux.
3. *(Facultatif)* Branche un outil de navigateur à ton assistant pour qu'il lise les offres et dépose tout seul. Sinon, colle les offres dans le chat et dépose les PDF toi-même.

## Premier lancement
1. Ouvre un terminal dans ce dossier et lance ton assistant.
2. Mets ton CV (PDF ou Word) dans le dossier et écris : **« Configure le skill postuler-stages avec mon CV »**.
3. Vérifie le CV qu'il te montre : tout le reste part de là.

## Ensuite, dis simplement
- « Postule aux nouvelles offres de stage »
- « Prépare une candidature pour cette offre : [lien ou texte] »
- « J'ai une entrevue chez [entreprise] »

Il te montre les candidatures prêtes. Réponds « oui » (ou « oui sauf 2 ») pour qu'il les dépose.

## Bon à savoir
- Ton CV garde toujours le même format ; seuls quelques mots changent selon l'offre.
- Il peut ajouter jusqu'à 3 compétences exigées par l'offre, notées dans « À apprendre » de l'Excel. Dis-lui si tu préfères qu'il n'en ajoute pas.
- Il ne crée pas de compte, ne tape pas de mot de passe et ne coche pas de captcha : il te le demande. Sur LinkedIn, tu cliques toi-même « Postuler ».
- Il retient tes réponses aux formulaires (`profil.json`) et ne te les redemande pas.
- Ferme l'Excel avant de lancer une session. Relis toujours ce qui part : c'est ton nom dessus.
