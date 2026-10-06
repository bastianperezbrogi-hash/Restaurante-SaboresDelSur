import os
import sys

_dir_padre = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _dir_padre not in sys.path:
    sys.path.insert(0, _dir_padre)

try:
    from model.bebida import Bebida
except ImportError:
    from bebida import Bebida


class BebidaImportada(Bebida):
    """
    Subclase de Bebida que representa una bebida/licor importado.
    Permite cotizar y calcular el precio en pesos según el tipo de cambio del dólar.
    """
    def __init__(self, nombre: str, precio_usd: float, id_item: int = None):
        super().__init__(nombre, precio_base=0, id_item=id_item)
        self._precio_usd = float(precio_usd)
        self._valor_dolar_dia = 950.0  # Valor por defecto

    @property
    def precio_usd(self) -> float:
        return self._precio_usd

    @precio_usd.setter
    def precio_usd(self, valor: float):
        self._precio_usd = float(valor)

    @property
    def valor_dolar_dia(self) -> float:
        return self._valor_dolar_dia

    def cotizar_segun_dolar(self, valor_dolar_dia: float) -> int:
        """Actualiza la cotización del día y retorna el precio en CLP."""
        self._valor_dolar_dia = float(valor_dolar_dia)
        self._precio_base = int(round(self._precio_usd * self._valor_dolar_dia))
        return self._precio_base

    def calcular_precio(self) -> int:
        """
        Sobrescribe polimórficamente calcular_precio() retornando el precio
        convertido a moneda nacional según el dólar.
        """
        return int(round(self._precio_usd * self._valor_dolar_dia))
