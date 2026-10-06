class RestauranteException(Exception):
    """Excepción base para las reglas de negocio del Restaurante Sabores del Sur."""
    pass

class MesaOcupadaException(RestauranteException):
    """Lanzada cuando se intenta abrir o asignar una mesa que ya está ocupada."""
    pass

class StockInsuficienteException(RestauranteException):
    """Lanzada cuando no hay stock suficiente de ingredientes para preparar un ítem."""
    pass

class PedidoCerradoException(RestauranteException):
    """Lanzada cuando se intenta modificar o agregar ítems a un pedido ya cerrado."""
    pass

class RutInvalidoException(RestauranteException, ValueError):
    """Lanzada cuando el RUT de un cliente no cumple con el algoritmo Módulo 11."""
    pass
