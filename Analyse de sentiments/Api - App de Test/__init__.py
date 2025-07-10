from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import os
from config import active_config


def create_app(config=active_config):
    """Initialise et configure l'application Flask"""
    print(f"Configuration active: {config}")

    # Créer l'application
    app = Flask(__name__)
    app.config.from_object(config)

    # Configurer CORS correctement pour autoriser les requêtes depuis n'importe quelle origine
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Configurer le logging
    # Configurer le logging avec gestion des erreurs
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    log_file = os.path.join(log_dir, 'sentiment_api.log')

    # Si le fichier log est verrouillé, utiliser un nom alternatif
    if os.path.exists(log_file):
        try:
            # Test si on peut écrire dans le fichier
            with open(log_file, 'a'):
                pass
        except IOError:
            # Si on ne peut pas écrire, utiliser un nom de fichier avec timestamp
            import time
            log_file = os.path.join(log_dir, f'sentiment_api_{int(time.time())}.log')

    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=5)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    # Éviter les erreurs de rotation de logs
    try:
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('API Sentiment démarrée')
    except Exception as e:
        print(f"Erreur de configuration des logs: {e}")

    # Enregistrer les blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    # Route de test direct
    @app.route('/')
    def index():
        return "API d'analyse de sentiment active! Utilisez /api/predict pour analyser un texte."

    # Route de test pour debugger
    @app.route('/test')
    def test():
        # Vérifier l'existence des fichiers de modèles
        text_model_path = app.config.get('MODEL_TEXT_PATH', 'app/models/sentiment_model_text_only.joblib')
        full_model_path = app.config.get('MODEL_FULL_PATH', 'app/models/sentiment_model_text_metadata.joblib')

        return {
            'app': 'Sentiment API',
            'status': 'running',
            'models': {
                'text_model': {
                    'path': text_model_path,
                    'exists': os.path.exists(text_model_path)
                },
                'full_model': {
                    'path': full_model_path,
                    'exists': os.path.exists(full_model_path)
                }
            }
        }

    @app.route('/test-predict', methods=['POST', 'OPTIONS'])
    def test_predict():
        print("Test de prédiction")
        if request.method == 'OPTIONS':
            # Gérer la demande préliminaire CORS
            response = app.make_default_options_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

        from app.services.predictor import SentimentPredictor
        predictor = SentimentPredictor()

        data = request.get_json(force=True)

        if 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Champ text requis'
            }), 400

        result, probability, raw_probas = predictor.predict_text_only(data['text'])

        return jsonify({
            'success': True,
            'result': result,
            'probability': probability,
            'all_probabilities': raw_probas
        })

    # Pré-charger les modèles (optionnel)
    with app.app_context():
        from app.services.predictor import SentimentPredictor
        predictor = SentimentPredictor(app)
        predictor.load_models(app)

    return app