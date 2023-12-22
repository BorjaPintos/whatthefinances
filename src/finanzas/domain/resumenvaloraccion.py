from datetime import datetime


class ResumenValorAccion:

    def __init__(self, params: dict):
        self._año = params.get("año")
        self._mes = params.get("mes")
        self._dia = params.get("dia")
        self._fecha = params.get("fecha")
        self._ultimo_valor = params.get("ultimo_valor")
        self._isin = params.get("isin")

    def get_año(self) -> int:
        return self._año

    def get_mes(self) -> int:
        return self._mes

    def get_dia(self) -> int:
        if self._dia is None:
            return self._fecha.strftime("%d")
        return self._dia

    def get_fecha(self) -> datetime:
        return self._fecha

    def get_ultimo_valor(self) -> int:
        return self._ultimo_valor

    def get_isin(self) -> str:
        return self._isin

    def get_dto(self) -> dict:
        return {
            "año": self._año,
            "mes": self._mes,
            "dia": self._dia,
            "fecha": self._fecha.strftime("%d/%m/%Y %H:%M"),
            "ultimo_valor": self._ultimo_valor,
            "isin": self._isin,
        }
