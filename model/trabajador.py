class Trabajador:
    """
    Superclase que representa a cualquier trabajador del restaurante.
    Contiene los datos comunes como RUT, nombre y rol.
    """
    def __init__(self, rut: str, nombre: str, rol: str):
        self._rut = rut  # RUT del trabajador
        self._nombre = nombre  # Nombre completo
        self._rol = rol  # Rol desempeñado

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def rol(self) -> str:
        return self._rol
