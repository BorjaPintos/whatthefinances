class Broker:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._nombre = params.get("nombre")
        self._extranjero = params.get("extranjero")

    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def set_nombre(self, nombre: str):
        self._nombre = nombre

    def is_extranjero(self) -> bool:
        return self._extranjero

    def set_extranjero(self, extranjero: bool):
        self._extranjero = extranjero

    def get_dto(self) -> dict:
        return {"id": self._id,
                "nombre": self._nombre,
                "extranjero": self._extranjero
                }
