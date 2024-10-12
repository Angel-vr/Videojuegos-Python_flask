from flask import Blueprint, render_template
from src.models.videojuego import Videojuego

videojuego_bp = Blueprint('videojuegos', __name__)

@videojuego_bp.route('/')
def index():
    videojuegos = Videojuego.obtener_videojuegos()
    return render_template('index.html', videojuegos=videojuegos)