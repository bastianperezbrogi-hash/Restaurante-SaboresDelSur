import sys
import os
from typing import List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dao.dao import Dao
from model.mesa import Mesa


class MesaDao(Dao):
    """
    Data Access Object para la entidad Mesa.
    Proporciona operaciones CRUD completas y persistencia en SQLite.
    """
    def crear_tabla(self):
        """Crea la tabla 'mesas' si no existe en la base de datos."""
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
        """Inserta o reemplaza una mesa en la base de datos."""
        sql = "INSERT OR REPLACE INTO mesas (numero, estado, tiene_pedido_abierto) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (mesa.numero, mesa.estado, 1 if mesa.tiene_pedido_abierto else 0))
        self.conexion.commit()

    def buscar(self, numero: int) -> Optional[Mesa]:
        """Busca una mesa por su número identificador."""
        sql = "SELECT numero, estado, tiene_pedido_abierto FROM mesas WHERE numero = ?"
        self.cursor.execute(sql, (numero,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        return Mesa(numero=fila[0], estado=fila[1], tiene_pedido_abierto=bool(fila[2]))

    def listar(self) -> List[Mesa]:
        """Retorna todas las mesas registradas."""
        sql = "SELECT numero, estado, tiene_pedido_abierto FROM mesas ORDER BY numero ASC"
        self.cursor.execute(sql)
        mesas = []
        for fila in self.cursor.fetchall():
            mesas.append(Mesa(numero=fila[0], estado=fila[1], tiene_pedido_abierto=bool(fila[2])))
        return mesas

    def actualizar(self, mesa: Mesa) -> Optional[Mesa]:
        """Actualiza el estado y condición de pedido de una mesa existente."""
        sql = "UPDATE mesas SET estado = ?, tiene_pedido_abierto = ? WHERE numero = ?"
        self.cursor.execute(sql, (mesa.estado, 1 if mesa.tiene_pedido_abierto else 0, mesa.numero))
        self.conexion.commit()
        if self.cursor.rowcount == 0:
            return None
        return self.buscar(mesa.numero)

    def eliminar(self, numero: int) -> bool:
        """Elimina una mesa de la base de datos por su número."""
        sql = "DELETE FROM mesas WHERE numero = ?"
        self.cursor.execute(sql, (numero,))
        self.conexion.commit()
        return self.cursor.rowcount > 0
