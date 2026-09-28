from model.itemmenu import ItemMenu

class DetallePedido:
    """
    Representa una línea de detalle dentro de un pedido (composición con Pedido).
    Contiene la cantidad solicitada, observaciones, estado y referencia a su ItemMenu.
    """
    def __init__(self, item_menu: ItemMenu, cantidad: int, observacion: str = "", esta_listo: bool = False, id_detalle: int = None):
        self._id = id_detalle
        self._item_menu = item_menu
        self._cantidad = cantidad
        self._observacion = observacion
        self._esta_listo = esta_listo

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, valor: int):
        self._id = valor

    @property
    def item_menu(self) -> ItemMenu:
        return self._item_menu

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def observacion(self) -> str:
        return self._observacion

    @property
    def esta_listo(self) -> bool:
        return self._esta_listo

    def marcar_como_listo(self) -> bool:
        """Marca la línea de detalle como preparada y lista para servir."""
        self._esta_listo = True
        return True

    def calcular_subtotal(self) -> int:
        """Calcula el subtotal multiplicando la cantidad por el precio polimórfico del ítem."""
        return self._cantidad * self._item_menu.calcular_precio()
