import sqlite3
import os

class Database:
    #Clase para gestionar la conexión y operaciones con SQLite
    
    def __init__(self, db_name="usuarios.db"):
        #Inicializa la conexión con la base de datos SQLite
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        #Establece la conexión con la base de datos SQLite
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.connection
    
    def close(self):
        #Cierra la conexión con la base de datos
        if self.connection:
            self.connection.close()
    
    def crear_tabla(self):
        #Crea la tabla de usuarios si no existe
        self.connect()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena TEXT NOT NULL,
                plataforma TEXT NOT NULL,
                nombre TEXT,
                apellido TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()
        self.close()
    
    def insertar_usuario(self, usuario, contrasena, plataforma, nombre=None, apellido=None):
        #Inserta un nuevo usuario en la base de datos
        self.connect()
        try:
            self.cursor.execute("""
                INSERT INTO usuarios (usuario, contrasena, plataforma, nombre, apellido)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario, contrasena, plataforma, nombre, apellido))
            self.connection.commit()
            self.close()
            return True
        except sqlite3.IntegrityError:
            self.close()
            return False
    
    def verificar_usuario(self, usuario, contrasena):
        #Verifica si las credenciales del usuario son válidas
        self.connect()
        self.cursor.execute("""
            SELECT usuario, contrasena, plataforma FROM usuarios 
            WHERE usuario = ? AND contrasena = ?
        """, (usuario, contrasena))
        resultado = self.cursor.fetchone()
        self.close()
        return resultado
    
    def obtener_usuario(self, usuario):
        #Obtiene los datos de un usuario específico
        self.connect()
        self.cursor.execute("""
            SELECT id, usuario, contrasena, plataforma, nombre, apellido, fecha_registro 
            FROM usuarios WHERE usuario = ?
        """, (usuario,))
        resultado = self.cursor.fetchone()
        self.close()
        return resultado
    
    def actualizar_contrasena(self, usuario, nueva_contrasena):
        #Actualiza la contraseña de un usuario
        self.connect()
        self.cursor.execute("""
            UPDATE usuarios SET contrasena = ? WHERE usuario = ?
        """, (nueva_contrasena, usuario))
        self.connection.commit()
        self.close()
    
    def eliminar_usuario(self, usuario):
        #Elimina un usuario de la base de datos
        self.connect()
        self.cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
        self.connection.commit()
        self.close()
    
    def listar_usuarios(self):
     
        self.connect()
        self.cursor.execute("""
            SELECT id, usuario, plataforma, nombre, apellido, fecha_registro 
            FROM usuarios
        """)
        resultados = self.cursor.fetchall()
        self.close()
        return resultados


# Instancia global de la base de datos
db = Database()

# Inicializar la tabla al importar el módulo
if __name__ == "__main__":
    # Crear la tabla si no existe
    db.crear_tabla()
    print("Base de datos inicializada correctamente.")
    print(f"Archivo de base de datos: {os.path.abspath(db.db_name)}")
