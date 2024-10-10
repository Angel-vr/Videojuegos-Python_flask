from decouple import config
import mysql.connector
from mysql.connector import Error

def conexion_db():
    try:
        conexion = mysql.connector.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            database=config('MYSQL_DB') 
        )
        if conexion.is_connected():
            print("Conexion Exitosa")            
            infoServer = conexion.get_server_info()
            print("Info del servidor:",infoServer)
            return conexion
    except Error as ex:
        print("Error conexion:" , ex)
        return