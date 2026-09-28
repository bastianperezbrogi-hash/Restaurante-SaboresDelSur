from model.bebida import Bebida

class BebidaImportada(Bebida):
    """
    Subclase de Bebida que representa una bebida/licor importado.
    Permite cotizar y calcular el precio en pesos según el tipo de cambio del dólar.
    """
    def __init__(self, nombre: str, precio_usd: int, id_item: int = None):
        super().__init__(nombre, precio_base=0, id_item=id_item)
        self._precio_usd = precio_usd
        self._valor_dolar_dia = 950  # Valor por defecto

    @property
    def precio_usd(self) -> int:
        return self._precio_usd

    def cotizar_segun_dolar(self, valor_dolar_dia: int) -> int:
        """Actualiza la cotización del día y retorna el precio en CLP."""
        self._valor_dolar_dia = valor_dolar_dia
        return self._precio_usd * valor_dolar_dia

    def calcular_precio(self) -> int:
        """
        Sobrescribe polimórficamente calcular_precio() retornando el precio
        convertido a moneda nacional según el dólar.
        """
        return self._precio_usd * self._valor_dolar_dia
