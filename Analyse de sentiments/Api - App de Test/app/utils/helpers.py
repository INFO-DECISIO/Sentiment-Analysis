import re
from flask import current_app


def preprocess_text(text):
    """
    Version simplifiée du prétraitement de texte
    Idéalement, cette fonction devrait réimplémenter le même prétraitement
    que celui utilisé pendant l'entraînement du modèle.
    """
    if not text:
        return ""

    # Conversion en minuscules
    text = text.lower()

    # Suppression des URLs, mentions, hashtags
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)

    # Suppression des caractères spéciaux et de la ponctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Suppression des espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def get_confidence_indicator(probability):
    """
    Transforme une probabilité en indicateur de confiance qualitatif
    """
    if probability is None:
        return "unknown"

    if probability >= 0.8:
        return "very_high"
    elif probability >= 0.6:
        return "high"
    elif probability >= 0.4:
        return "moderate"
    elif probability >= 0.2:
        return "low"
    else:
        return "very_low"