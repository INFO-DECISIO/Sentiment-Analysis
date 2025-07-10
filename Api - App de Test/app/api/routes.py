from flask import request, jsonify, current_app
import time

from app.services.predictor import SentimentPredictor

from application.app.api import bp

# Ne pas initialiser le prédicteur tout de suite
predictor = None


# Fonction pour obtenir le prédicteur initialisé
def get_predictor():
    global predictor
    if predictor is None:
        predictor = SentimentPredictor()
    return predictor


@bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint pour vérifier la santé de l'API"""
    p = get_predictor()
    return jsonify({
        'status': 'ok',
        'timestamp': time.time(),
        'models': {
            'text_only': p.text_model_loaded,
            'text_metadata': p.full_model_loaded
        }
    })


@bp.route('/predict', methods=['POST'])
def predict_sentiment():
    """Endpoint principal pour prédire le sentiment d'un texte"""
    data = request.get_json(force=True)
    current_app.logger.info(f"Requête de prédiction reçue: {str(data)[:100]}...")

    response = {
        'success': False,
        'result': None,
        'probability': None,
        'error': None
    }

    try:
        # Obtenir le prédicteur
        p = get_predictor()

        # Vérification des données d'entrée
        if 'use_metadata' in data and data['use_metadata']:
            # Cas du modèle avec métadonnées
            required_fields = ['cleaned_text', 'Platform', 'Time of Tweet']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Champ requis manquant: {field}")

            # Appeler la prédiction avec métadonnées
            result, probability, raw_probas = p.predict_with_metadata(
                cleaned_text=data['cleaned_text'],
                platform=data['Platform'],
                time=data['Time of Tweet']
            )
        else:
            # Cas du modèle texte seulement
            if 'text' not in data:
                raise ValueError("Champ 'text' requis pour la prédiction")

            # Appeler la prédiction texte seulement
            result, probability, raw_probas = p.predict_text_only(data['text'])

        # Ajouter les résultats à la réponse
        response.update({
            'success': True,
            'result': result,
            'probability': probability,
            'all_probabilities': raw_probas,
            'error': None
        })

        current_app.logger.info(f"Prédiction réussie: {result['label']} avec probabilité {probability}")
        return jsonify(response)

    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Erreur de prédiction: {error_msg}")
        response['error'] = error_msg
        return jsonify(response), 400


@bp.route('/models/info', methods=['GET'])
def model_info():
    """Retourne des informations sur les modèles disponibles"""
    p = get_predictor()

    # Récupérer le mapping et le seuil de confiance depuis la configuration
    sentiment_map = current_app.config.get('SENTIMENT_MAP', {
        0: {'label': 'neutral', 'value': 0, 'emoji': '😐'},
        1: {'label': 'positive', 'value': 1, 'emoji': '😄'},
        2: {'label': 'negative', 'value': -1, 'emoji': '😔'}
    })
    undetermined = current_app.config.get('UNDETERMINED', {
        'label': 'undetermined', 'value': None, 'emoji': '🤔'
    })

    return jsonify({
        'text_only': {
            'name': p.text_model_name,
            'loaded': p.text_model_loaded,
            'path': current_app.config.get('MODEL_TEXT_PATH', 'app/models/sentiment_model_text_only.joblib')
        },
        'text_metadata': {
            'name': p.full_model_name,
            'loaded': p.full_model_loaded,
            'path': current_app.config.get('MODEL_FULL_PATH', 'app/models/sentiment_model_text_metadata.joblib')
        },
        'sentiment_classes': {
            'neutral': sentiment_map.get(0),
            'positive': sentiment_map.get(1),
            'negative': sentiment_map.get(2),
            'undetermined': undetermined
        }
    })