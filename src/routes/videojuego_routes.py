from flask import Blueprint, render_template, request
from src.models.videojuego import Videojuego

videojuego_bp = Blueprint('videojuegos', __name__)

@videojuego_bp.route('/', methods=['GET'])
def index():
    videojuegos, pagination, query = Videojuego.obtener_videojuegos_paginados(request)
    return render_template('index.html', videojuegos=videojuegos, pagination=pagination, query=query)

@videojuego_bp.route('/login', methods=['GET'])
def login():
        return render_template('login.html')

