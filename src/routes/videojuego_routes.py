from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models.videojuego import Videojuego
from src.models.usuario import User, ModelUser
from flask_login import login_manager, login_user,logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

videojuego_bp = Blueprint('videojuegos', __name__)


@videojuego_bp.route('/', methods=['GET'])

def index():
    videojuegos, pagination, query = Videojuego.obtener_videojuegos_paginados(request)
    return render_template('index.html', videojuegos=videojuegos, pagination=pagination, query=query)

@videojuego_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']  
        password = request.form['password']

        user = User(None, None, None, email, password)
        logged_user = ModelUser.login(user)

        if logged_user is not None:
            login_user(logged_user)
            return redirect(url_for('videojuegos.index'))  
        else:
            flash('Correo o contraseña incorrectos', 'danger')
            return render_template('login.html')  
    else:    
        return render_template('login.html')

@videojuego_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('videojuegos.index'))


@videojuego_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nomusuario = request.form['nomusuario']
        dni = request.form['dni']
        email = request.form['email']  
        password = request.form['password']
        
        if ModelUser.check_user_exists(email, dni, nomusuario):
            flash('El email, DNI o nombre de usuario ya están registrados. Intenta con otros datos.', 'danger')
            return redirect(url_for('videojuegos.create'))
        
        hashed_password = generate_password_hash(password)
        
        new_user = User(None, nomusuario, dni, email, hashed_password)
        
        if ModelUser.create(new_user):
            flash("Usuario registrado correctamente", "success")
            return redirect(url_for('videojuegos.create')) 
        else:
            flash("Error al registrar usuario", "danger")
            return render_template('create.html')
        
                
    return render_template('create.html')