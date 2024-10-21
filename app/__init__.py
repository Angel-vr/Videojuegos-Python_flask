from flask import Flask
from src.routes.videojuego_routes import videojuego_bp



def create_app():
    app = Flask(__name__,
                template_folder="../src/templates",
                static_folder="../src/static")  # Configura el folder de templates y static

    # Importa y registra tus rutas
    
    app.register_blueprint(videojuego_bp)

    return app
