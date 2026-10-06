import os
import sys

_dir_padre = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _dir_padre not in sys.path:
    sys.path.insert(0, _dir_padre)

try:
    from model.itemmenu import ItemMenu
except ImportError:
    from itemmenu import ItemMenu


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
