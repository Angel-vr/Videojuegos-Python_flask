from flask import session


class ShoppingCart:
     
    @classmethod
    def init_cart(cls):
        """Inicializa el carrito si no existe en la sesión."""
        if "cart" not in session:
            session["cart"] = {}
        session.modified = True
               
    @staticmethod
    def add_to_cart(product_id, product_name, product_price):
        ShoppingCart.init_cart()
        cart = session["cart"]
        
        # cart = {int(k): v for k, v in cart.items()}
        cart = {int(product_id): product_info for product_id, product_info in cart.items()}

        product_id = int(product_id)  
        
        # Verificar los tipos de los valores antes de almacenarlos
        print(f"Carrito actual antes de añadir: {cart}")
        


        
        # Convertir el precio a float si es necesario
        try:
            product_price = float(product_price) 
        except ValueError:
            print(f"Error al convertir el precio: {product_price}")# Si el precio es un Decimal, lo convertimos a float
            return
        print(f"Agregando al carrito - ID: {product_id}, Nombre: {product_name}, Precio: {product_price}, Cantidad: 1")
        
        if product_id in cart:
            cart[product_id]["quantity"] += 1
        else:
            cart[product_id] = {"nombre": product_name, "precio": product_price, "quantity": 1}
        
        # Imprimir el contenido del carrito antes de guardarlo en la sesión
        print(f"Carrito: {cart}")
        print(f"Product ID: {product_id} (type: {type(product_id)})")
        print(f"Product Price: {product_price} (type: {type(product_price)})")

        session["cart"] = cart
        session.modified = True

    @staticmethod
    def get_cart_items():
        # Obtiene los elementos del carrito desde la sesión
        return session.get("cart", {})

    
        
    @staticmethod
    def remove_from_cart(product_id):
        ShoppingCart.init_cart()
        cart = session["cart"]
        
        if product_id in cart:
            del cart[product_id]
            session.modified = True
            
    @staticmethod
    def clear_cart():
        session.pop("cart", None)
        

        
    @staticmethod
    def get_total_price(cart):
        cart = ShoppingCart.get_cart_items()
        
        # Debugging: Ver los elementos del carrito y sus precios
        print("Calculando el total del carrito:")
        for product_id, item in cart.items():
            print(f"Producto: {item['nombre']}, Precio: {item['precio']}, Cantidad: {item['quantity']}")
        

        
        # Asegúrate de que el precio sea un número decimal (float) al calcular el total
        total = round(sum(float(item["precio"]) * item["quantity"] for item in cart.values()), 2)
        print(f"Total del carrito: {total}")  # Mensaje de depuración
        
        return total

