import requests

class MiIndicador:
    """
    Servicio para consumir la API pública de mindicador.cl.
    Permite obtener indicadores económicos de Chile actualizados en tiempo real:
    - dolar, uf, euro, utm, ipc, etc.
    """
    BASE_URL = "https://mindicador.cl/api/"

    def __init__(self, timeout: int = 5):
        self.__timeout = timeout

    def valor(self, codigo: str) -> float:
        """
        Consulta la API y retorna el valor numérico del indicador solicitado.
        :param codigo: Código del indicador ('dolar', 'uf', 'euro', 'utm', 'ipc', etc.)
        :return: Valor numérico actual del indicador
        """
        url = self.BASE_URL + codigo.strip().lower()
        respuesta = requests.get(url, timeout=self.__timeout)
        respuesta.raise_for_status()
        datos = respuesta.json()
        if "serie" in datos and len(datos["serie"]) > 0:
            return float(datos["serie"][0]["valor"])
        elif "valor" in datos:
            return float(datos["valor"])
        raise ValueError(f"No se pudo extraer el valor para el indicador '{codigo}'.")

