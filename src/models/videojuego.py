from src.database.database import conexion_db
from flask_paginate import Pagination, get_page_args


class Videojuego:
    
    @staticmethod
    def obtener_videojuegos(offset=0, limit=6):
        """Obtiene una lista de videojuegos de la base de datos."""
        sql = """
        SELECT `videojuegos`.`idvideojuego`, `nomvideojuego`, `feclanzamiento`, `precio`, `nomimagen`
        FROM `videojuegos`
        INNER JOIN `videojuegoimagenes` ON `videojuegos`.`idvideojuego` = `videojuegoimagenes`.`idvideojuego`
        LEFT JOIN `imagenes` ON `videojuegoimagenes`.`idimagen` = `imagenes`.`idimagen`
        LIMIT %s OFFSET %s        
        """
        
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return []  # Retorna una lista vacía si no hay conexión
        print("\nAccediendo a datos.")
        
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql, (limit, offset)) #ejecuta la consulta con limit y offset para paginación
            videojuegos = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(*) AS total FROM videojuegos")
            total = cursor.fetchone()['total']
            
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return [] # Retorna una lista vacía en caso de error
        finally:
            cursor.close()
            conexion.close()
        
        return videojuegos, total
    
    @staticmethod    
    def buscar_videojuegos(offset=0, limit=6, search_query=''):
        """Busca videojuegos en la base de datos filtrados por un término de búsqueda."""
        
        sql = """
        SELECT `videojuegos`.`idvideojuego`, `nomvideojuego`, `feclanzamiento`, `precio`, `nomimagen`
        FROM `videojuegos`
        INNER JOIN `videojuegoimagenes` ON `videojuegos`.`idvideojuego` = `videojuegoimagenes`.`idvideojuego`
        LEFT JOIN `imagenes` ON `videojuegoimagenes`.`idimagen` = `imagenes`.`idimagen`
        WHERE `nomvideojuego` LIKE %s
        LIMIT %s OFFSET %s
        """
        
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return []  # Retorna una lista vacía si no hay conexión
        
        print("\nBuscando videojuegos.")
        
        try:
            cursor = conexion.cursor(dictionary=True)
            # Ejecuta la consulta con el término de búsqueda
            cursor.execute(sql, ('%' + search_query + '%', limit, offset))
            videojuegos = cursor.fetchall()
            
            # Consulta para contar el total de videojuegos que coinciden con el término de búsqueda
            count_sql = "SELECT COUNT(*) AS total FROM `videojuegos` WHERE `nomvideojuego` LIKE %s"
            cursor.execute(count_sql, ('%' + search_query + '%',))
            total = cursor.fetchone()['total']
            
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []  # Retorna una lista vacía en caso de error
        finally:
            cursor.close()
            conexion.close()
        
        return videojuegos, total
        
    @staticmethod
    def obtener_videojuegos_paginados(request):
        query = request.args.get('query', '')
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page=6)
        
        if query:
            # Si hay un término de búsqueda, llama a la función buscar_videojuegos
            videojuegos, total_items = Videojuego.buscar_videojuegos(offset=offset, limit=per_page, search_query=query)
        else:
            # Si no hay búsqueda, llama a la función original obtener_videojuegos
            videojuegos, total_items = Videojuego.obtener_videojuegos(offset=offset, limit=per_page)

        # Crea la paginación usando el total de elementos y la configuración actual
        pagination = Pagination(page=page, total=total_items, per_page=per_page)
        
        return videojuegos, pagination, query
    
    

    @staticmethod
    def obtener_videojuego_por_id(videojuego_id):
        """Obtiene un videojuego específico por su ID de la base de datos."""
        sql = """
        SELECT `idvideojuego`, `nomvideojuego`, `precio`
        FROM `videojuegos`
        WHERE `idvideojuego` = %s
        """
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return None
        
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql, (videojuego_id,))
            videojuego = cursor.fetchone()  # Devuelve el primer resultado si existe
            
            if videojuego:
                # Asegúrate de que 'precio' sea un número serializable (float)
                videojuego['precio'] = float(videojuego['precio'])


            
        except Exception as e:
            print(f"Error al obtener el videojuego: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

        return videojuego


    
    


# from werkzeug.security import check_password_hash


# class User:
    
#     def __init__(self, idusuario, nomusuario, dni, email, password) -> None:
#         self.idusuario= idusuario
#         self.nomusuario= nomusuario
#         self.dni=dni
#         self.email=email
#         self.password=password
     
#     @classmethod    
#     def check_password(cls,hashed_password, password):
#         return check_password_hash(hashed_password, password)
    
#     # print(generate_password_hash('prueba'))
    
# class ModelUser:
    
#     @classmethod
#     def login(cls,user):
#         sql="""
#         SELECT idusuario, email, password, nomusuario 
#         FROM usuarios
#         WHERE email = %s"""
        
#         conexion = conexion_db()
#         if conexion is None:
#             print("No se pudo establecer conexión a la base de datos.")
#             return []  # Retorna una lista vacía si no hay conexión
#         print("\nAccediendo a datos.")  
          
#         try:            
#             cursor = conexion.cursor(dictionary=True)
#             cursor.execute(sql, (user.email,))
#             row=cursor.fetchone()
#             if row is not None:
#                 if User.check_password(row['password'], user.password):
#                     return User(row['idusuario'],row['nomusuario'], None, row['email'], row['password'])
#             return None
           
            
#         except Exception as ex:
#             print(f"Error: {ex}")
#             return None
        
# user_to_test = User(idusuario=None, nomusuario=None, dni=None, email='a@a.com', password='prueba')

# logged_user = ModelUser.login(user_to_test)

# if logged_user:
#     print(f'Usuario logueado: {logged_user.nomusuario}')
# else:
#     print('login fallido')