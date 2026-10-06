import sys
import os
from typing import List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dao.dao import Dao
from model.ingrediente import Ingrediente


class IngredienteDao(Dao):
    """
    Data Access Object para la entidad Ingrediente.
    Proporciona operaciones CRUD completas y persistencia en SQLite.
    """
    def crear_tabla(self):
        """Crea la tabla 'ingredientes' si no existe en la base de datos."""
        sql = """
        CREATE TABLE IF NOT EXISTS ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock_actual INTEGER NOT NULL,
            es_clave INTEGER NOT NULL
        )
        """
        self.cursor.execute(sql)
        self.conexion.commit()

    def insertar(self, ingrediente: Ingrediente):
        """Inserta un nuevo ingrediente y asigna el id generado."""
        sql = "INSERT INTO ingredientes (nombre, stock_actual, es_clave) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (ingrediente.nombre, ingrediente.stock_actual, 1 if ingrediente.es_clave else 0))
        ingrediente.id = self.cursor.lastrowid
        self.conexion.commit()

    def buscar(self, id_ing: int) -> Optional[Ingrediente]:
        """Busca un ingrediente por su ID."""
        sql = "SELECT id, nombre, stock_actual, es_clave FROM ingredientes WHERE id = ?"
        self.cursor.execute(sql, (id_ing,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        return Ingrediente(nombre=fila[1], stock_actual=fila[2], es_clave=bool(fila[3]), id_ingrediente=fila[0])

    def listar(self) -> List[Ingrediente]:
        """Retorna todos los ingredientes registrados."""
        sql = "SELECT id, nombre, stock_actual, es_clave FROM ingredientes ORDER BY id ASC"
        self.cursor.execute(sql)
        ingredientes = []
        for fila in self.cursor.fetchall():
            ingredientes.append(Ingrediente(nombre=fila[1], stock_actual=fila[2], es_clave=bool(fila[3]), id_ingrediente=fila[0]))
        return ingredientes

    def actualizar(self, ingrediente: Ingrediente) -> Optional[Ingrediente]:
        """Actualiza los datos de un ingrediente existente."""
        sql = "UPDATE ingredientes SET nombre = ?, stock_actual = ?, es_clave = ? WHERE id = ?"
        self.cursor.execute(sql, (ingrediente.nombre, ingrediente.stock_actual, 1 if ingrediente.es_clave else 0, ingrediente.id))
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(ingrediente.id)

    def eliminar(self, id_ing: int) -> bool:
        """Elimina un ingrediente de la base de datos por su ID."""
        sql = "DELETE FROM ingredientes WHERE id = ?"
        self.cursor.execute(sql, (id_ing,))
        self.conexion.commit()
        return self.cursor.rowcount > 0
