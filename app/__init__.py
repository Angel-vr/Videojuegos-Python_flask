from flask import Flask
from src.routes.videojuego_routes import videojuego_bp

def create_app():
    app = Flask(__name__, template_folder="../src/templates")  # Configura el folder de templates

    # Importa y registra tus rutas
    
    app.register_blueprint(videojuego_bp)

    return app
