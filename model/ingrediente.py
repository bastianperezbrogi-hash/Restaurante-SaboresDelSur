class Ingrediente:
    """
    Representa un ingrediente utilizado en las preparaciones del restaurante,
    con control de stock y clasificación de ingrediente crítico/clave.
    """
    def __init__(self, nombre: str, stock_actual: int, es_clave: bool = False, id_ingrediente: int = None):
        self._id = id_ingrediente
        self._nombre = nombre
        self._stock_actual = stock_actual
        self._es_clave = es_clave

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, valor: int):
        self._id = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = valor

    @property
    def stock_actual(self) -> int:
        return self._stock_actual

    @stock_actual.setter
    def stock_actual(self, valor: int):
        self._stock_actual = max(0, int(valor))

    @property
    def es_clave(self) -> bool:
        return self._es_clave

    @es_clave.setter
    def es_clave(self, valor: bool):
        self._es_clave = bool(valor)

    def tiene_stock_suficiente(self, cantidad_requerida: int = 1) -> bool:
        """Verifica si hay stock suficiente del ingrediente."""
        return self._stock_actual >= cantidad_requerida

    def descontar_stock(self, cantidad: int = 1) -> bool:
        """Descuenta del inventario la cantidad indicada si hay disponible."""
        if self.tiene_stock_suficiente(cantidad):
            self._stock_actual -= cantidad
            return True
        return False

