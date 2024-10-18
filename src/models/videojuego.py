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
            return []  # Retorna una lista vacía en caso de error
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
<<<<<<< HEAD
        pagination = Pagination(page=page, total=total_items, per_page=per_page, css_framework='bootstrap5')
=======
        pagination = Pagination(page=page, total=total_items, per_page=per_page)
>>>>>>> a493f0b (base login)
        
        return videojuegos, pagination, query
