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

    def verificar_pedido_abierto(self) -> bool:
        """Retorna si la mesa cuenta con un pedido actualmente en curso."""
        return self._tiene_pedido_abierto

    def abrir_mesa(self) -> bool:
        """Abre la mesa para nuevos clientes cambiando su estado."""
        if not self._tiene_pedido_abierto:
            self._tiene_pedido_abierto = True
            self._estado = "Ocupada"
            return True
        return False

    def cerrar_mesa(self) -> bool:
        """Cierra la mesa liberándola."""
        self._tiene_pedido_abierto = False
        self._estado = "Disponible"
        return True
