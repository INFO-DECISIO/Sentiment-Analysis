from flask import Blueprint

# Créer le blueprint avec le préfixe /api
bp = Blueprint('api', __name__, url_prefix='/api')

# Importer les routes
from app.api import routes