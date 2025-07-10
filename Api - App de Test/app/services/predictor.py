import os
import joblib
import pandas as pd
import numpy as np
from flask import current_app


class SentimentPredictor:
    """Service pour charger et utiliser les modèles de prédiction de sentiment"""

    def __init__(self, app=None):
        """Initialise le service en chargeant les modèles"""
        self.text_model = None
        self.text_model_loaded = False
        self.text_model_name = "Unknown"

        self.full_model = None
        self.full_model_loaded = False
        self.full_model_name = "Unknown"

        # Stocke l'app pour une utilisation ultérieure si fournie
        self.app = app

        # Les modèles seront chargés lors de la première utilisation
        # ou explicitement via load_models()

    def load_models(self, app=None):
        """Charge explicitement les modèles, utile pour les initialiser avec l'app"""
        if app:
            self.app = app

        try:
            # Utiliser le contexte de l'application pour charger les modèles
            with self.app.app_context():
                self._load_models()
        except Exception as e:
            print(f"Erreur lors du chargement des modèles: {str(e)}")

    def _load_models(self):
        """Charge les modèles à partir des fichiers joblib"""
        # Modèle texte seulement
        try:
            # Utilise le modèle par défaut si nous ne sommes pas dans un contexte d'application
            text_model_path = current_app.config.get('MODEL_TEXT_PATH', 'app/models/sentiment_model_text_only.joblib')

            if os.path.exists(text_model_path):
                self.text_model = joblib.load(text_model_path)
                self.text_model_loaded = True
                self.text_model_name = "Multinomial NB (Text Only)"
                print(f"Modèle texte chargé depuis {text_model_path}")
                if hasattr(current_app, 'logger'):
                    current_app.logger.info(f"Modèle texte chargé depuis {text_model_path}")
            else:
                print(f"Fichier modèle texte non trouvé: {text_model_path}")
                if hasattr(current_app, 'logger'):
                    current_app.logger.error(f"Fichier modèle texte non trouvé: {text_model_path}")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle texte: {str(e)}")
            if hasattr(current_app, 'logger'):
                current_app.logger.error(f"Erreur lors du chargement du modèle texte: {str(e)}")

        # Modèle texte + métadonnées
        try:
            # Utilise le modèle par défaut si nous ne sommes pas dans un contexte d'application
            full_model_path = current_app.config.get('MODEL_FULL_PATH',
                                                     'app/models/sentiment_model_text_metadata.joblib')

            if os.path.exists(full_model_path):
                self.full_model = joblib.load(full_model_path)
                self.full_model_loaded = True
                self.full_model_name = "SVC Linear (Text + Metadata)"
                print(f"Modèle avec métadonnées chargé depuis {full_model_path}")
                if hasattr(current_app, 'logger'):
                    current_app.logger.info(f"Modèle avec métadonnées chargé depuis {full_model_path}")
            else:
                print(f"Fichier modèle avec métadonnées non trouvé: {full_model_path}")
                if hasattr(current_app, 'logger'):
                    current_app.logger.error(f"Fichier modèle avec métadonnées non trouvé: {full_model_path}")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle avec métadonnées: {str(e)}")
            if hasattr(current_app, 'logger'):
                current_app.logger.error(f"Erreur lors du chargement du modèle avec métadonnées: {str(e)}")

    def _format_result(self, prediction_encoded, probability):
        """Formate le résultat de la prédiction"""
        # Récupérer le mapping et le seuil de confiance
        try:
            sentiment_map = current_app.config.get('SENTIMENT_MAP', {
                0: {'label': 'neutral', 'value': 0, 'emoji': '😐'},
                1: {'label': 'positive', 'value': 1, 'emoji': '😄'},
                2: {'label': 'negative', 'value': -1, 'emoji': '😔'}
            })
            threshold = current_app.config.get('CONFIDENCE_THRESHOLD', 0.2)
            undetermined = current_app.config.get('UNDETERMINED', {
                'label': 'undetermined', 'value': None, 'emoji': '🤔'
            })
        except RuntimeError:
            # Fallback values if not in app context
            sentiment_map = {
                0: {'label': 'neutral', 'value': 0, 'emoji': '😐'},
                1: {'label': 'positive', 'value': 1, 'emoji': '😄'},
                2: {'label': 'negative', 'value': -1, 'emoji': '😔'}
            }
            threshold = 0.5
            undetermined = {'label': 'undetermined', 'value': None, 'emoji': '🤔'}

        # Si la probabilité est trop faible, considérer comme indéterminé
        if probability is not None and probability < threshold:
            result = undetermined
        else:
            # Sinon, obtenir le résultat à partir du mapping
            result = sentiment_map.get(prediction_encoded, undetermined)

        return result, probability

    def predict_text_only(self, text):
        """Prédit le sentiment à partir du texte seulement"""
        # Charge les modèles si ce n'est pas déjà fait
        if not self.text_model_loaded:
            self._load_models()

        if not self.text_model_loaded:
            raise ValueError("Modèle texte non disponible")

        # Préparer les données d'entrée (liste de texte)
        input_data = [text]

        # Faire la prédiction
        prediction_encoded = self.text_model.predict(input_data)[0]

        # Obtenir les probabilités si disponibles
        probability = None
        raw_probas = None

        if hasattr(self.text_model, 'predict_proba'):
            raw_probas = self.text_model.predict_proba(input_data)[0].tolist()
            probability = float(raw_probas[prediction_encoded])

        # Formater le résultat
        result, probability = self._format_result(prediction_encoded, probability)

        return result, probability, raw_probas

    def predict_with_metadata(self, cleaned_text, platform, time):
        """Prédit le sentiment avec texte + métadonnées"""
        # Charge les modèles si ce n'est pas déjà fait
        if not self.full_model_loaded:
            self._load_models()

        if not self.full_model_loaded:
            raise ValueError("Modèle avec métadonnées non disponible")

        # Préparer les données d'entrée
        input_data = {
            'cleaned_text': cleaned_text,
            'Platform': platform,
            'Time of Tweet': time
        }

        # Convertir en DataFrame
        input_df = pd.DataFrame([input_data])

        # Faire la prédiction
        prediction_encoded = self.full_model.predict(input_df)[0]

        # Obtenir les probabilités si disponibles
        probability = None
        raw_probas = None

        if hasattr(self.full_model, 'predict_proba'):
            raw_probas = self.full_model.predict_proba(input_df)[0].tolist()
            probability = float(raw_probas[prediction_encoded])

        # Formater le résultat
        result, probability = self._format_result(prediction_encoded, probability)

        return result, probability, raw_probas