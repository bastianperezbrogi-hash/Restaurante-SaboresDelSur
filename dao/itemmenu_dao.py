from dao.dao import Dao
from model.itemmenu import ItemMenu

class ItemMenuDao(Dao):
    """
    Data Access Object para la entidad ItemMenu.
    """
    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS items_menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio_base INTEGER NOT NULL,
            tiempo_preparacion INTEGER NOT NULL,
            estacion_cocina TEXT NOT NULL
        )
        """
        self.cursor.execute(sql)
        self.conexion.commit()

    def insertar(self, item: ItemMenu):
        sql = "INSERT INTO items_menu (nombre, precio_base, tiempo_preparacion, estacion_cocina) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql, (item.nombre, item.precio_base, item.tiempo_preparacion, item.estacion_cocina))
        item.id = self.cursor.lastrowid
        self.conexion.commit()
