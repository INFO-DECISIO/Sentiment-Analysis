# Membres du Groupe

- **DONFACK Pascal Arthur (M1-GI) – 21P457 (Chef de projet)**
- TEMGOUA FOBANKE Emmanuelle (M1-GI) – 21P436
- FEKE Jimmy (M1-GI) – 21P474
- TIWA TIOTSAP (M1-GI) – 21P450
- WESSIBASSIEBAH Mike (M1-GI) – 21P459
- MBOLANG TIDANG Henri (M1-GI) – 21P471
- DONGMO PRINCE WILLIAMS (M1-GI) – 21P445
- TOLOKOUM David Rive (M1-GI) – 21P478

# Projet d'Analyse de Sentiments - M1 GI ENSPY

Ce projet, réalisé dans le cadre du cours d'Informatique Décisionnelle pour le Master 1 Génie Informatique à l'ENSPY, porte sur l'analyse de sentiments à partir de données textuelles. L'objectif principal était de construire et d'évaluer rigoureusement un modèle de classification de sentiments, tout en mettant en évidence l'impact de certaines mauvaises pratiques comme le *data leaking*.

## Contexte et Objectifs

L'analyse de sentiments est une branche du Traitement Automatique du Langage Naturel (NLP) qui vise à déterminer la polarité émotionnelle (positive, négative, neutre) d'un texte.

Ce projet s'est particulièrement intéressé à la comparaison de performances entre :
1.  Une approche d'entraînement naïve, inspirée de travaux précédents présentant des fuites de données (*data leaking*).
2.  Une approche méthodologique rigoureuse, avec une séparation stricte des données et une validation croisée pour obtenir une estimation fiable des performances du modèle.

Les travaux précédents (disponibles sur Kaggle : [Sentiment Analysis - EDA and Prediction](https://www.kaggle.com/code/alokkumar2507/sentiment-analysis-eda-and-prediction)) rapportaient un score de **72%** de précision, un chiffre artificiellement élevé en raison du *data leaking*. Notre propre réplication de cette erreur a donné **39%** de précision une fois la fuite corrigée.

Grâce à une meilleure méthodologie, notre modèle final atteint un score de **61%** en validation croisée et **54%** sur un jeu de test dédié, démontrant une amélioration significative et une évaluation plus honnête des performances.

## Structure du Dépôt

Le projet est organisé en trois grands dossiers :

```
.
├── Api - App de Test/      # Contient l'API Flask qui sert le modèle.
├── Etude Sentiment Analysis/ # Contient toute l'analyse exploratoire et l'entraînement des modèles.
└── FrontEnd - App de Test/ # Contient l'application web Vue.js pour tester le modèle.
```

### 1. `Etude Sentiment Analysis/`

Ce dossier est le cœur du projet. Il contient les notebooks Jupyter de l'analyse exploratoire des données (EDA), de l'entraînement des modèles et de l'évaluation.

*   **`Data/`**: Contient le jeu de données `sentiment_analysis.csv`.
*   **`Exploratory analysis/`**: Notebook et graphiques de l'analyse exploratoire. On y étudie la distribution des sentiments, la longueur des textes, la fréquence des mots, etc.
*   **`Training/`**: Notebook détaillant le prétraitement des données, l'entraînement du modèle (avec et sans métadonnées) et l'évaluation rigoureuse via validation croisée et jeu de test.
*   **`sentiment_model_text_only.joblib`**: Le modèle final, entraîné uniquement sur le texte des tweets. C'est ce modèle qui est utilisé par l'API.

### 2. `Api - App de Test/`

Cette API, développée avec Flask, expose le modèle de classification de sentiments. Elle reçoit du texte et retourne une prédiction (positif, négatif ou neutre).

*   **`app/`**: Le code source de l'application Flask.
    *   `api/routes.py`: Le point d'entrée de l'API qui gère les requêtes.
    *   `services/predictor.py`: Charge le modèle `.joblib` et effectue les prédictions.
    *   `models/`: Contient les modèles sauvegardés.
*   **`run.py`**: Le script pour lancer le serveur de l'API.
*   **`requirements.txt`**: Les dépendances Python à installer.

### 3. `FrontEnd - App de Test/`

Une application web simple, développée avec Vue.js, qui permet d'interagir avec l'API pour tester le modèle en temps réel.

*   **`src/`**: Le code source de l'application Vue.
    *   `components/SentimentAnalyzer.vue`: Le composant principal qui contient le formulaire de saisie et affiche le résultat.
*   **`index.html`**: Le point d'entrée de l'application web.
*   **`package.json`**: Les dépendances Node.js à installer.

## Comment lancer l'application de test ?

Pour tester le modèle, tu dois lancer le back-end (l'API Flask) et le front-end (l'application Vue.js).

### Étape 1 : Lancer l'API (Back-end)

1.  **Ouvre un premier terminal** et navigue dans le dossier de l'API :
    ```bash
    cd "Api - App de Test"
    ```

2.  Crée un environnement virtuel et active-le :
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Installe les dépendances Python :
    ```bash
    pip install -r requirements.txt
    ```

4.  Lance l'API :
    ```bash
    python run.py
    ```
    L'API devrait maintenant tourner sur `http://127.0.0.1:5000`.

### Étape 2 : Lancer l'application web (Front-end)

1.  **Ouvre un deuxième terminal** et navigue dans le dossier du front-end :
    ```bash
    cd "FrontEnd - App de Test"
    ```

2.  Installe les dépendances Node.js :
    ```bash
    npm install
    ```

3.  Lance le serveur de développement :
    ```bash
    npm run dev
    ```
    L'application web sera accessible à l'adresse indiquée dans le terminal (généralement `http://localhost:5173`).

4.  **Ouvre ton navigateur** à l'adresse du front-end. Tu peux maintenant saisir du texte et voir l'analyse de sentiment en temps réel !

## Conclusion de l'étude

Ce projet a permis non seulement de développer un modèle fonctionnel pour l'analyse de sentiments, mais aussi de mettre en pratique des concepts fondamentaux de la science des données, notamment l'importance d'une évaluation rigoureuse et la détection de biais comme le *data leaking*. Les résultats obtenus, bien que modestes, sont une représentation bien plus fidèle de la performance réelle du modèle sur de nouvelles données.