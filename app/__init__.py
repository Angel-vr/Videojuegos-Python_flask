from flask import Flask
from src.routes.videojuego_routes import videojuego_bp
from decouple import config


def create_app():
    app = Flask(__name__,
                template_folder="../src/templates",
                static_folder="../src/static")  # Configura el folder de templates y static

    app.config['SECRET_KEY'] = config('SECRET_KEY')

    # verificar si esta configurada variable de entorno
    if not app.config['SECRET_KEY']:
        raise ValueError("La variable SECRET_KEY no está configurada en variables de entorno")
    # print(app.config['SECRET_KEY'])
    
    # Importa y registra tus rutas    
    app.register_blueprint(videojuego_bp)

    return app
