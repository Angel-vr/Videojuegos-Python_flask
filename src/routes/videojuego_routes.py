from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.videojuego import Videojuego
from src.models.usuario import User, ModelUser
from flask_login import login_manager, login_user,logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.shoppingcart import ShoppingCart

videojuego_bp = Blueprint('videojuegos', __name__)


@videojuego_bp.route('/', methods=['GET'])

def index():
    videojuegos, pagination, query = Videojuego.obtener_videojuegos_paginados(request)
    
    cart = session.get("cart", {})
    
    total_quantity = sum(item['quantity'] for item in cart.values())
    
    
    total = ShoppingCart.get_total_price(cart)
    return render_template('index.html', videojuegos=videojuegos, pagination=pagination, query=query, cart=cart, total=total, total_quantity=total_quantity)

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
    
    
@videojuego_bp.route('/add_to_cart/<int:videojuego_id>', methods=['GET', 'POST'])
def add_to_cart(videojuego_id):
    videojuego_id = int(videojuego_id)
    # Obtener los detalles del videojuego a partir del ID
    videojuego = Videojuego.obtener_videojuego_por_id(videojuego_id)
    
    if videojuego:
        # Asegúrate de que el precio sea un número decimal (float)
        precio = float(videojuego['precio'])  # Convertir el precio a float
        print(f"Añadiendo al carrito: {videojuego['nomvideojuego']} con precio {precio}")  # Mensaje de depuración
        
        # Agregar al carrito
        ShoppingCart.add_to_cart(int(videojuego['idvideojuego']), videojuego['nomvideojuego'], precio)
        
        flash(f'{videojuego["nomvideojuego"]} añadido al carrito')  # Mensaje de éxito
    else:
        flash("Videojuego no encontrado.", "error")  # Mensaje de error si no se encuentra el videojuego
        
    return redirect(url_for('videojuegos.index'))  # Redirigir a la página de inicio (o donde lo necesites)

@videojuego_bp.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)  # Elimina el carrito de la sesión
    flash("El carrito ha sido vaciado", "info")
    return redirect(url_for('videojuegos.index'))  # Redirige de nuevo a la página principal o donde desees
           

    
    

@videojuego_bp.route('/logout')
@login_required
def logout():
    session.pop('cart', None)
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