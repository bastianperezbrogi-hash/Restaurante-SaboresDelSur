import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "restaurante.db")

def crear_conexion(db_path: str = DB_PATH):
    """
    Crea y retorna una conexión a la base de datos SQLite 'restaurante.db'.
    Habilita el uso de Foreign Keys (claves foráneas) por defecto.
    """
    conexion = sqlite3.connect(db_path)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

