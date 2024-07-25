
class ResumenPosicionAcumulada:

    def __init__(self, params: dict):
        self._isin = params.get("isin")
        self._año = params.get("año")
        self._mes = params.get("mes")
        self._precio_compra_mes = params.get("precio_compra_mes")
        self._participaciones_mes = params.get("participaciones_mes")
        self._participaciones_acumuladas = params.get("participaciones_acumuladas")
        self._precio_compra_acumulado = params.get("precio_compra_acumulado")

    def get_isin(self) -> str:
        return self._isin

    def get_año(self) -> int:
        return self._año

    def get_mes(self) -> int:
        return self._mes

    def get_precio_compra_mes(self) -> float:
        return self._precio_compra_mes

    def get_participaciones_mes(self) -> float:
        return self._participaciones_mes

    def get_precio_compra_acumulado(self) -> float:
        return self._precio_compra_acumulado

    def get_participaciones_acumuladas(self) -> float:
        return self._participaciones_acumuladas

    def get_dto(self) -> dict:
        return {
            "isin": self._isin,
            "año": self._año,
            "mes": self._mes,
            "precio_compra_mes": self._precio_compra_mes,
            "participaciones_mes": self._participaciones_mes,
            "participaciones_acumuladas": self._participaciones_acumuladas,
            "precio_compra_acumulado": self._precio_compra_acumulado,
        }
