class Cocinero:
    """
    Subclase de Trabajador (o clase Cocinero) encargada de preparar y despachar pedidos.
    """
    def __init__(self, rut: str, nombre: str, estacion_asignada: str = "Cocina Principal"):
        self._rut = rut
        self._nombre = nombre
        self._rol = "Cocinero"
        self._estacion_asignada = estacion_asignada

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def rol(self) -> str:
        return self._rol

    @property
    def estacion_asignada(self) -> str:
        return self._estacion_asignada

    def preparar_plato(self, detalle) -> bool:
        """Inicia la preparación de un plato en la estación asignada."""
        return True

    def marcar_listo(self, detalle) -> bool:
        """Marca una línea de detalle como lista."""
        return detalle.marcar_como_listo()
