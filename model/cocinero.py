from model.trabajador import Trabajador

class Cocinero(Trabajador):
    """
    Subclase de Trabajador encargada de preparar y despachar pedidos.
    """
    def __init__(self, rut: str, nombre: str, estacion_asignada: str = "Cocina Principal"):
        super().__init__(rut, nombre, "Cocinero")
        self._estacion_asignada = estacion_asignada

    @property
    def estacion_asignada(self) -> str:
        return self._estacion_asignada

    @estacion_asignada.setter
    def estacion_asignada(self, valor: str):
        self._estacion_asignada = valor

    def preparar_plato(self, detalle) -> bool:
        """Inicia la preparación de un plato en la estación asignada."""
        return True

    def marcar_listo(self, detalle) -> bool:
        """Marca una línea de detalle como lista."""
        return detalle.marcar_como_listo()

