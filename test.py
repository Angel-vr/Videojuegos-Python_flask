# from src.database.database import conexion_db

# try:
#     conexion = conexion_db()
# except Exception as e:
#     print("Error al conectar db",e)


from src.models.videojuego import Videojuego

videojuegos = Videojuego.obtener_videojuegos()
print("Videojuegos en la base de datos:\n")
for juego in videojuegos:
    print(juego)