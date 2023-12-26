from datetime import date


class Dividendo:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._fecha = params.get("fecha")
        self._isin = params.get("isin")
        self._dividendo_por_accion = params.get("dividendo_por_accion")
        self._retencion_por_accion = params.get("retencion_por_accion")

    def get_id(self) -> int:
        return self._id

    def get_fecha(self) -> date:
        return self._fecha

    def get_isin(self) -> str:
        return self._isin

    def get_dividendo_por_accion(self) -> float:
        return self._dividendo_por_accion

    def get_retencion_por_accion(self) -> float:
        return self._retencion_por_accion

    def set_fecha(self, fecha: date):
        self._fecha = fecha

    def set_isin(self, isin: str):
        self._isin = isin

    def set_dividendo_por_accion(self, dividendo_por_accion: float):
        self._dividendo_por_accion = dividendo_por_accion

    def set_retencion_por_accion(self, retencion_por_accion: float):
        self._retencion_por_accion = retencion_por_accion

    def get_dto(self) -> dict:
        return {"id": self._id,
                "isin": self._isin,
                "fecha": self._fecha.strftime("%d/%m/%Y"),
                "dividendo_por_accion": self._dividendo_por_accion,
                "retencion_por_accion": self._retencion_por_accion
                }
