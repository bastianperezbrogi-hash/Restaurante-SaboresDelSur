import re

class Boleta:
    """
    Representa el comprobante tributario emitido al cerrar un pedido.
    Incluye validación formal del RUT chileno del cliente.
    """
    def __init__(self, numero_boleta: int, rut_cliente: str, monto_total: int, id_boleta: int = None):
        self._id = id_boleta
        self._numero_boleta = numero_boleta
        self._rut_cliente = rut_cliente
        self._monto_total = monto_total

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, valor: int):
        self._id = valor

    @property
    def numero_boleta(self) -> int:
        return self._numero_boleta

    @property
    def rut_cliente(self) -> str:
        return self._rut_cliente

    @property
    def monto_total(self) -> int:
        return self._monto_total

    @monto_total.setter
    def monto_total(self, valor: int):
        self._monto_total = valor

    def validar_rut(self, rut: str) -> bool:
        """
        Valida el RUT chileno mediante el algoritmo de Módulo 11.
        """
        rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()
        if len(rut_limpio) < 2:
            return False

        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]

        if not cuerpo.isdigit():
            return False

        suma = 0
        multiplicador = 2
        for d in reversed(cuerpo):
            suma += int(d) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = suma % 11
        dv_calculado = 11 - resto
        if dv_calculado == 11:
            dv_esperado = "0"
        elif dv_calculado == 10:
            dv_esperado = "K"
        else:
            dv_esperado = str(dv_calculado)

        return dv == dv_esperado

    def emitir_documento(self) -> bool:
        """Emite la boleta validando el RUT y el monto."""
        if self.validar_rut(self._rut_cliente) and self._monto_total > 0:
            return True
        return False
