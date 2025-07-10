import os

from application import create_app


# Déterminer l'environnement (dev, test, prod)
env = os.environ.get('FLASK_ENV', 'dev')
app = create_app()

if __name__ == '__main__':
    # Obtenir le port depuis les variables d'environnement ou utiliser 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    # Lancer le serveur
    app.run(host='0.0.0.0', port=port)