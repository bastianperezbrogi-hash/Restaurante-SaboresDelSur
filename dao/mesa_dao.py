from dao.dao import Dao
from model.mesa import Mesa

class MesaDao(Dao):
    """
    Data Access Object para la entidad Mesa.
    """
    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS mesas (
            numero INTEGER PRIMARY KEY,
            estado TEXT NOT NULL,
            tiene_pedido_abierto INTEGER NOT NULL
        )
        """
        self.cursor.execute(sql)
        self.conexion.commit()

    def insertar(self, mesa: Mesa):
        sql = "INSERT OR REPLACE INTO mesas (numero, estado, tiene_pedido_abierto) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (mesa.numero, mesa.estado, 1 if mesa.tiene_pedido_abierto else 0))
        self.conexion.commit()
