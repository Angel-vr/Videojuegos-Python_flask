from flask import Flask
from src.routes.videojuego_routes import videojuego_bp
from decouple import config
from src.models.usuario import User, ModelUser
from flask_login import LoginManager

def create_app():
    app = Flask(__name__,
                template_folder="../src/templates",
                static_folder="../src/static")  # Configura el folder de templates y static
    
    app.secret_key = config('SECRET_KEY')

    # verificar si esta configurada variable de entorno
    if not app.config['SECRET_KEY']:
        raise ValueError("La variable SECRET_KEY no está configurada en variables de entorno")
    # print(app.config['SECRET_KEY'])

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "videojuegos.login"
     
    @login_manager.user_loader
    
    def load_user(user_id):
        return ModelUser.get_by_id(user_id) 
    

    # Importa y registra tus rutas    
    app.register_blueprint(videojuego_bp)

    return app
