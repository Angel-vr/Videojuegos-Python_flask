from src.database.database import conexion_db
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, idusuario, nomusuario, dni, email, password) -> None:
        self.idusuario= idusuario
        self.nomusuario= nomusuario
        self.dni=dni
        self.email=email
        self.password=password
    
    def get_id(self):
        return str(self.idusuario)  # Devuelve el ID como cadena

     
    @classmethod    
    def check_password(cls,hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    # print(generate_password_hash('prueba'))
    
class ModelUser:
    
    @classmethod
    def login(cls,user):
        sql="""
        SELECT idusuario, email, password, nomusuario 
        FROM usuarios
        WHERE email = %s"""
        
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return []  # Retorna una lista vacía si no hay conexión
        print("\nAccediendo a datos.")  
          
        try:            
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql, (user.email,))
            row=cursor.fetchone()
            if row is not None:
                if User.check_password(row['password'], user.password):
                    return User(row['idusuario'],row['nomusuario'], None, row['email'], row['password'])
            return None
           
            
        except Exception as ex:
            print(f"Error: {ex}")
            return None



    @classmethod
    def get_by_id(cls, user_id):
        sql = """
        SELECT idusuario, nomusuario, email, password
        FROM usuarios
        WHERE idusuario = %s"""
        
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return None  # Retorna None si no hay conexión

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            if row is not None:
                # Devuelve un objeto User con la información
                return User(row['idusuario'], row['nomusuario'], None, row['email'], row['password'])
            return None
        except Exception as ex:
            print(f"Error: {ex}")
            return None

    @classmethod
    def create(cls, user):
        sql = """
        INSERT INTO usuarios (nomusuario, dni, email, password)
        VALUES (%s, %s, %s, %s)"""
            
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return None  # Retorna None si no hay conexión
        
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(sql, (user.nomusuario, user.dni, user.email, user.password))
            conexion.commit()
            return True
        except Exception as ex:
            print(f"Error al registrar usuario: {ex}")
            return False

            

    @classmethod
    def check_user_exists(cls, email, dni, nomusuario):
        sql="""
        SELECT 1 FROM usuarios
        WHERE email = %s OR dni = %s OR nomusuario = %s
        """
        conexion = conexion_db()
        if conexion is None:
            print("No se pudo establecer conexión a la base de datos.")
            return False
        cursor = conexion.cursor()
        cursor.execute(sql, (email, dni, nomusuario))
        result = cursor.fetchone()
        return bool(result)















        
# user_to_test = User(idusuario=None, nomusuario=None, dni=None, email='a@a.com', password='prueba')

# logged_user = ModelUser.login(user_to_test)

# if logged_user:
#     print(f'Usuario logueado: {logged_user.nomusuario}')
# else:
#     print('login fallido')