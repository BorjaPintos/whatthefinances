class DividendoRango:

    def __init__(self, params: dict):
        self._isin = params.get("isin")
        self._dividendo = params.get("dividendo")
        self._retencion = params.get("retencion")

    def get_isin(self) -> int:
        return self._isin

    def get_dividendo(self) -> float:
        return self._dividendo

    def get_retencion(self) -> bool:
        return self._retencion

    def get_dto(self) -> dict:
        return {"isin": self._isin,
                "dividendo": self._dividendo,
                "retencion": self._retencion,
                "neto": self.get_dividendo() - self.get_retencion()
                }
