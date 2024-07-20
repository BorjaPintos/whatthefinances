from datetime import datetime


class ResumenPosicion:

    def __init__(self, params: dict):
        self._año = params.get("año")
        self._mes = params.get("mes")
        self._dia = params.get("dia")
        self._fecha = params.get("fecha")
        self._valor = params.get("valor")
        self._suma_participaciones = params.get("suma_participaciones")
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

    def get_valor(self) -> float:
        return self._valor

    def get_suma_participaciones(self) -> float:
        return self._suma_participaciones

    def get_isin(self) -> str:
        return self._isin

    def get_dto(self) -> dict:
        return {
            "año": self._año,
            "mes": self._mes,
            "dia": self._dia,
            "fecha": self._fecha.strftime("%d/%m/%Y %H:%M"),
            "valor": self._valor,
            "suma_participaciones": self._suma_participaciones,
            "isin": self._isin,
        }
