class Producto:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._nombre = params.get("nombre")
        self._isin = params.get("isin")

    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def set_nombre(self, nombre: str):
        self._nombre = nombre

    def get_isin(self) -> str:
        return self._isin

    def set_isin(self, isin: str):
        self._isin = isin

    def get_dto(self) -> dict:
        return {"id": self._id,
                "nombre": self._nombre,
                "isin": self._isin
                }
