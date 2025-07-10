# API d'Analyse de Sentiment

Cette API permet d'analyser le sentiment de textes en utilisant des modèles ML préentraînés avec NLP.
Elle fournit des prédictions indiquant si un texte est positif, négatif, neutre ou indéterminé.

## Installation et démarrage

### Prérequis
- Python 3.7+
- Flask
- Scikit-learn
- Joblib
- Pandas

### Installation
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installer les dépendances
pip install flask flask-cors pandas scikit-learn joblib