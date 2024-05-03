from datetime import datetime


class ValorParticipacion:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._isin = params.get("isin")
        self._nombre = params.get("nombre")
        self._fecha = params.get("fecha")
        self._valor = params.get("valor")

    def get_id(self) -> int:
        return self._id

    def get_isin(self) -> str:
        return self._isin

    def get_nombre(self) -> str:
        return self._nombre

    def get_fecha(self) -> datetime:
        return self._fecha

    def get_valor(self) -> float:
        return self._valor

    def get_dto(self) -> dict:
        return {"id": self._id,
                "isin": self._isin,
                "nombre": self._nombre,
                "fecha": self._fecha.strftime("%d/%m/%Y %H:%M"),
                "valor": self._valor
                }
