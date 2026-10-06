import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.itemmenu import ItemMenu


class Postre(ItemMenu):
    """
    Subclase de ItemMenu que representa un postre.
    Sobrescribe calcular_precio() implementando polimorfismo.
    """
    def __init__(self, nombre: str, precio_base: int, id_item: int = None):
        super().__init__(nombre, precio_base, tiempo_preparacion=5, estacion_cocina="Repostería", id_item=id_item)

    def calcular_precio(self) -> int:
        """Calcula el precio del postre."""
        return self._precio_base
