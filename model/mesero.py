from model.mesa import Mesa
from model.pedido import Pedido

class Mesero:
    """
    Subclase de Trabajador encargada de interactuar con el cliente, abrir mesas y tomar pedidos.
    """
    def __init__(self, rut: str, nombre: str):
        self._rut = rut
        self._nombre = nombre
        self._rol = "Mesero"

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def rol(self) -> str:
        return self._rol

    def tomar_pedido(self, mesa: Mesa, numero_pedido: int = 1) -> Pedido:
        """Abre un nuevo pedido para la mesa dada."""
        mesa.abrir_mesa()
        return Pedido(numero_pedido=numero_pedido, mesa=mesa, mesero=self)

    def marcar_mesa(self, mesa: Mesa, estado: str) -> bool:
        """Actualiza el estado de una mesa."""
        mesa.estado = estado
        return True
