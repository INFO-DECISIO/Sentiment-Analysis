import os


class Config:
    """Configuration de base pour l'application"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_very_secret')

    # Chemins des modèles - Assurez-vous que ces chemins sont corrects!
    MODEL_TEXT_PATH = os.path.join('app', 'models', 'sentiment_model_text_only.joblib')
    MODEL_FULL_PATH = os.path.join('app', 'models', 'sentiment_model_text_metadata.joblib')

    # Paramètres de prédiction
    CONFIDENCE_THRESHOLD = 0.2

    # Mapping final pour les sentiments
    SENTIMENT_MAP = {
        0: {'label': 'neutral', 'value': 0, 'emoji': '😐'},
        1: {'label': 'positive', 'value': 1, 'emoji': '😄'},
        2: {'label': 'negative', 'value': -1, 'emoji': '😔'}
    }
    # Définir un sentiment "indéterminé" quand la confiance est faible
    UNDETERMINED = {'label': 'undetermined', 'value': None, 'emoji': '🤔'}


class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True


class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True


class ProductionConfig(Config):
    """Configuration pour la production"""
    # En production, utiliser des variables d'environnement sécurisées
    pass


# Configuration active selon l'environnement
config_by_name = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}

# Configuration par défaut
active_config = config_by_name[os.environ.get('FLASK_ENV', 'dev')]