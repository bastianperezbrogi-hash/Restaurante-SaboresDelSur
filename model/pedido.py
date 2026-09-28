from typing import List, Optional
from datetime import datetime
from model.mesa import Mesa
from model.itemmenu import ItemMenu
from model.detallepedido import DetallePedido
from model.boleta import Boleta

class Pedido:
    """
    Representa una comanda o pedido en el restaurante.
    Posee relación de composición con DetallePedido, y asociaciones con Mesa, Mesero y Boleta.
    """
    def __init__(self, numero_pedido: int, mesa: Mesa, mesero=None, id_pedido: int = None):
        self._id = id_pedido
        self._numero_pedido = numero_pedido
        self._fecha_hora = datetime.now()
        self._estado = "Abierto"
        self._mesa = mesa
        self._mesero = mesero
        self._boleta: Optional[Boleta] = None
        self._detalles: List[DetallePedido] = []

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, valor: int):
        self._id = valor

    @property
    def numero_pedido(self) -> int:
        return self._numero_pedido

    @property
    def fecha_hora(self) -> datetime:
        return self._fecha_hora

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def mesa(self) -> Mesa:
        return self._mesa

    @property
    def mesero(self):
        return self._mesero

    @property
    def boleta(self) -> Optional[Boleta]:
        return self._boleta

    @boleta.setter
    def boleta(self, b: Boleta):
        self._boleta = b

    @property
    def detalles(self) -> List[DetallePedido]:
        return self._detalles

    def agregar_detalle(self, item: ItemMenu, cant: int, obs: str = "") -> bool:
        """
        Agrega una línea de detalle al pedido (Composición) y descuenta insumos.
        """
        if self._estado == "Abierto" and item.verificar_stock_ingredientes():
            for ing in item.ingredientes:
                ing.descontar_stock(cant)
            detalle = DetallePedido(item_menu=item, cantidad=cant, observacion=obs)
            self._detalles.append(detalle)
            return True
        return False

    def calcular_total(self) -> int:
        """Calcula el total sumando el subtotal de cada línea de detalle."""
        return sum(detalle.calcular_subtotal() for detalle in self._detalles)

    def cerrar_pedido(self, rut_cliente: str = "12345678-5") -> Optional[Boleta]:
        """Cierra el pedido, genera y asocia la Boleta y libera la mesa."""
        if self._estado == "Abierto":
            self._estado = "Cerrado"
            total = self.calcular_total()
            self._boleta = Boleta(numero_boleta=self._numero_pedido + 1000, rut_cliente=rut_cliente, monto_total=total)
            if self._mesa:
                self._mesa.cerrar_mesa()
            return self._boleta
        return None
