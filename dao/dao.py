class Dao:
    """
    Clase base Data Access Object (DAO).
    Se encarga de inicializar y mantener la conexión a la base de datos y su cursor.
    """
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = self.conexion.cursor()
