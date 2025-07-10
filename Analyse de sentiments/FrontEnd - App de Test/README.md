# Application Front-End pour l'Analyse de Sentiments

Cette application, développée avec Vue.js 3 et Vite, fournit une interface utilisateur simple et intuitive pour interagir avec l'API d'analyse de sentiments.

## Aperçu

L'application permet aux utilisateurs de saisir une phrase ou un texte dans un champ de formulaire. Une fois le texte soumis, il est envoyé à l'API Flask qui, en retour, renvoie le sentiment prédit (Positif, Négatif ou Neutre). Le résultat est ensuite affiché à l'utilisateur.

## Technologies utilisées

*   **Vue.js 3** : Le framework JavaScript progressif pour la construction de l'interface utilisateur.
*   **Vite** : Un outil de build moderne qui offre une expérience de développement rapide.
*   **Tailwind CSS** : Un framework CSS "utility-first" pour un style rapide et personnalisé.
*   **Axios** : Un client HTTP basé sur les promesses pour effectuer des requêtes à l'API.

## Installation et Lancement

Pour lancer l'application en local, suivez ces étapes :

1.  **Prérequis** : Assurez-vous d'avoir [Node.js](https://nodejs.org/) (version 16 ou supérieure) et [npm](https://www.npmjs.com/) installés sur votre machine.

2.  **Cloner le dépôt** (si ce n'est pas déjà fait) :
    ```bash
    git clone https://github.com/VOTRE_NOM_UTILISATEUR/VOTRE_PROJET.git
    cd VOTRE_PROJET/Analyse de sentiments/FrontEnd - App de Test
    ```

3.  **Installer les dépendances** :
    ```bash
    npm install
    ```

4.  **Lancer le serveur de développement** :
    ```bash
    npm run dev
    ```

    L'application sera alors accessible à l'adresse indiquée dans le terminal (généralement `http://localhost:5173`).

## Utilisation

1.  Assurez-vous que l'API Flask du back-end est en cours d'exécution (voir le `README.md` du dossier `Api - App de Test`).
2.  Ouvrez votre navigateur et accédez à l'application Vue.js.
3.  Saisissez un texte dans le champ prévu à cet effet.
4.  Cliquez sur le bouton "Analyser".
5.  Le sentiment prédit s'affichera à l'écran.

## Build pour la Production

Pour créer une version optimisée de l'application pour la production, exécutez la commande suivante :

```bash
npm run build
```

Les fichiers de production seront générés dans le dossier `dist/`.