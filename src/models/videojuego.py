from src.database.database import conexion_db

class Videojuego:
    
    
    def obtener_videojuegos():
        """Obtiene una lista de videojuegos de la base de datos."""
        sql = """
        SELECT `videojuegos`.`idvideojuego`, `nomvideojuego`, `feclanzamiento`, `precio`, `nomimagen`
        FROM `videojuegos`
        INNER JOIN `videojuegoimagenes` ON `videojuegos`.`idvideojuego` = `videojuegoimagenes`.`idvideojuego`
        LEFT JOIN `imagenes` ON `videojuegoimagenes`.`idimagen` = `imagenes`.`idimagen`
        LIMIT 6
        """
        
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return []  # Retorna una lista vacía si no hay conexión
        print("\nAccediendo a datos.")
        
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql)
            videojuegos = cursor.fetchall()
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []  # Retorna una lista vacía en caso de error
        finally:
            cursor.close()
            conexion.close()
        
        return videojuegos