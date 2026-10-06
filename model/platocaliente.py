import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.itemmenu import ItemMenu


class PlatoCaliente(ItemMenu):
    """
    Subclase de ItemMenu que representa un plato caliente.
    Sobrescribe calcular_precio() implementando polimorfismo.
    """
    def __init__(self, nombre: str, precio_base: int, tiempo_preparacion: int, id_item: int = None):
        super().__init__(nombre, precio_base, tiempo_preparacion, "Cocina Caliente", id_item)

    def calcular_precio(self) -> int:
        """Calcula el precio del plato caliente (precio base)."""
        return self._precio_base
