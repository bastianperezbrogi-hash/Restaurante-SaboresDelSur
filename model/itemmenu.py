from typing import List
from model.ingrediente import Ingrediente

class ItemMenu:
    """
    Superclase que representa un ítem del menú del restaurante.
    Aplica polimorfismo a través del método calcular_precio().
    """
    def __init__(self, nombre: str, precio_base: int, tiempo_preparacion: int, estacion_cocina: str, id_item: int = None):
        self._id = id_item
        self._nombre = nombre
        self._precio_base = precio_base
        self._tiempo_preparacion = tiempo_preparacion
        self._estacion_cocina = estacion_cocina
        self._ingredientes: List[Ingrediente] = []

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
    def precio_base(self) -> int:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: int):
        self._precio_base = valor

    @property
    def tiempo_preparacion(self) -> int:
        return self._tiempo_preparacion

    @tiempo_preparacion.setter
    def tiempo_preparacion(self, valor: int):
        self._tiempo_preparacion = valor

    @property
    def estacion_cocina(self) -> str:
        return self._estacion_cocina

    @estacion_cocina.setter
    def estacion_cocina(self, valor: str):
        self._estacion_cocina = valor

    @property
    def ingredientes(self) -> List[Ingrediente]:
        return self._ingredientes


    def agregar_ingrediente(self, ingrediente: Ingrediente):
        """Agrega un ingrediente a la lista de ingredientes del ítem."""
        self._ingredientes.append(ingrediente)

    def verificar_stock_ingredientes(self) -> bool:
        """Verifica que todos los ingredientes asociados cuenten con stock."""
        return all(ing.tiene_stock_suficiente() for ing in self._ingredientes)

    def obtener_tiempo_preparacion(self) -> int:
        """Retorna el tiempo de preparación en minutos."""
        return self._tiempo_preparacion

    def obtener_estacion_cocina(self) -> str:
        """Retorna la estación de cocina encargada de preparar el ítem."""
        return self._estacion_cocina

    def tratar_pedido(self) -> bool:
        """Realiza el tratamiento del ítem al prepararse."""
        return self.verificar_stock_ingredientes()

    def calcular_precio(self) -> int:
        """
        Método polimórfico base para calcular el precio final del ítem.
        Las subclases lo sobrescriben para aplicar recargos o conversiones específicas.
        """
        return self._precio_base
