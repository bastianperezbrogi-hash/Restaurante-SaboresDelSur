from dao.dao import Dao
from model.ingrediente import Ingrediente

class IngredienteDao(Dao):
    """
    Data Access Object para la entidad Ingrediente.
    """
    def crear_tabla(self):
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
        sql = "INSERT INTO ingredientes (nombre, stock_actual, es_clave) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (ingrediente.nombre, ingrediente.stock_actual, 1 if ingrediente.es_clave else 0))
        ingrediente.id = self.cursor.lastrowid
        self.conexion.commit()
