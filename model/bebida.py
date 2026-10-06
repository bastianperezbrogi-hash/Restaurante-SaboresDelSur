import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.itemmenu import ItemMenu


class Bebida(ItemMenu):
    """
    Subclase de ItemMenu que representa una bebida estándar.
    Sobrescribe calcular_precio() implementando polimorfismo.
    """
    def __init__(self, nombre: str, precio_base: int, id_item: int = None):
        super().__init__(nombre, precio_base, tiempo_preparacion=2, estacion_cocina="Barra", id_item=id_item)

    def calcular_precio(self) -> int:
        """Calcula el precio de la bebida."""
        return self._precio_base
