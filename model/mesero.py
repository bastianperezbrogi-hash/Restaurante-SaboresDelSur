from model.trabajador import Trabajador
from model.mesa import Mesa
from model.pedido import Pedido

class Mesero(Trabajador):
    """
    Subclase de Trabajador encargada de interactuar con el cliente, abrir mesas y tomar pedidos.
    """
    def __init__(self, rut: str, nombre: str):
        super().__init__(rut, nombre, "Mesero")

    def tomar_pedido(self, mesa: Mesa, numero_pedido: int = 1, cliente: str = "Cliente") -> Pedido:
        """Abre un nuevo pedido para la mesa dada si no está abierta ya."""
        if not mesa.tiene_pedido_abierto:
            mesa.abrir_mesa()
        return Pedido(numero_pedido=numero_pedido, mesa=mesa, mesero=self, cliente=cliente)


    def marcar_mesa(self, mesa: Mesa, estado: str) -> bool:
        """Actualiza el estado de una mesa."""
        mesa.estado = estado
        return True

