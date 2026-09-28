import sqlite3  # Importa el módulo sqlite3 para interactuar con bases de datos SQLite

def crear_conexion():  # Define la función encargada de establecer la conexión
    """
    Crea y retorna una conexión a la base de datos SQLite 'restaurante.db'.
    Habilita el uso de Foreign Keys (claves foráneas) por defecto.
    """
    conexion = sqlite3.connect("restaurante.db")  # Crea la conexión a la base de datos 'restaurante.db'
    conexion.execute("PRAGMA foreign_keys = ON")  # Habilita el soporte para claves foráneas
    return conexion  # Retorna el objeto de conexión
