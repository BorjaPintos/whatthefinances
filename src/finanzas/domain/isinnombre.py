class IsinNombre:

    def __init__(self, params: dict):
        self._isin = params.get("isin")
        self._nombre = params.get("nombre")

    def get_isin(self) -> str:
        return self._isin

    def get_nombre(self) -> str:
        return self._nombre

    def get_dto(self) -> dict:
        return {"isin": self._isin,
                "nombre": self._nombre
                }
