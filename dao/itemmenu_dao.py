from typing import List, Optional
from dao.dao import Dao
from model.itemmenu import ItemMenu

class ItemMenuDao(Dao):
    """
    Data Access Object para la entidad ItemMenu.
    Proporciona operaciones CRUD completas y persistencia en SQLite.
    """
    def crear_tabla(self):
        """Crea la tabla 'items_menu' si no existe en la base de datos."""
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
        """Inserta un nuevo ítem del menú y asigna el id generado."""
        sql = "INSERT INTO items_menu (nombre, precio_base, tiempo_preparacion, estacion_cocina) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql, (item.nombre, item.precio_base, item.tiempo_preparacion, item.estacion_cocina))
        item.id = self.cursor.lastrowid
        self.conexion.commit()

    def buscar(self, id_item: int) -> Optional[ItemMenu]:
        """Busca un ítem de menú por su ID."""
        sql = "SELECT id, nombre, precio_base, tiempo_preparacion, estacion_cocina FROM items_menu WHERE id = ?"
        self.cursor.execute(sql, (id_item,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        return ItemMenu(nombre=fila[1], precio_base=fila[2], tiempo_preparacion=fila[3], estacion_cocina=fila[4], id_item=fila[0])

    def listar(self) -> List[ItemMenu]:
        """Retorna todos los ítems de menú registrados en la base de datos."""
        sql = "SELECT id, nombre, precio_base, tiempo_preparacion, estacion_cocina FROM items_menu ORDER BY id ASC"
        self.cursor.execute(sql)
        items = []
        for fila in self.cursor.fetchall():
            items.append(ItemMenu(nombre=fila[1], precio_base=fila[2], tiempo_preparacion=fila[3], estacion_cocina=fila[4], id_item=fila[0]))
        return items

    def actualizar(self, item: ItemMenu) -> Optional[ItemMenu]:
        """Actualiza los datos de un ítem de menú existente."""
        sql = """
        UPDATE items_menu 
        SET nombre = ?, precio_base = ?, tiempo_preparacion = ?, estacion_cocina = ?
        WHERE id = ?
        """
        self.cursor.execute(sql, (item.nombre, item.precio_base, item.tiempo_preparacion, item.estacion_cocina, item.id))
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(item.id)

    def eliminar(self, id_item: int) -> bool:
        """Elimina un ítem de menú de la base de datos por su ID."""
        sql = "DELETE FROM items_menu WHERE id = ?"
        self.cursor.execute(sql, (id_item,))
        self.conexion.commit()
        return self.cursor.rowcount > 0
