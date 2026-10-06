import os
import sys

_dir_padre = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _dir_padre not in sys.path:
    sys.path.insert(0, _dir_padre)

try:
    from model.excepciones import MesaOcupadaException
except ImportError:
    from excepciones import MesaOcupadaException


class Mesa:
    """
    Representa una mesa del restaurante con su estado y control de apertura.
    """
    def __init__(self, numero: int, estado: str = "Disponible", tiene_pedido_abierto: bool = False):
        self._numero = numero
        self._estado = estado
        self._tiene_pedido_abierto = tiene_pedido_abierto

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: str):
        self._estado = nuevo_estado

    @property
    def tiene_pedido_abierto(self) -> bool:
        return self._tiene_pedido_abierto

    @tiene_pedido_abierto.setter
    def tiene_pedido_abierto(self, valor: bool):
        self._tiene_pedido_abierto = bool(valor)

    def verificar_pedido_abierto(self) -> bool:
        """Retorna si la mesa cuenta con un pedido actualmente en curso."""
        return self._tiene_pedido_abierto

    def abrir_mesa(self) -> bool:
        """
        Abre la mesa para nuevos clientes cambiando su estado a 'Ocupada'.
        Lanza MesaOcupadaException si la mesa ya está ocupada o tiene un pedido activo.
        """
        if self._tiene_pedido_abierto or self._estado == "Ocupada":
            raise MesaOcupadaException(f"Regla de Negocio: La Mesa #{self._numero} ya está ocupada.")
        self._tiene_pedido_abierto = True
        self._estado = "Ocupada"
        return True

    def cerrar_mesa(self) -> bool:
        """Cierra la mesa liberándola."""
        self._tiene_pedido_abierto = False
        self._estado = "Disponible"
        return True
