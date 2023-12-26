class Broker:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._nombre = params.get("nombre")
        self._extrangero = params.get("extrangero")

    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def set_nombre(self, nombre: str):
        self._nombre = nombre

    def is_extrangero(self) -> bool:
        return self._extrangero

    def set_extrangero(self, extrangero: bool):
        self._extrangero = extrangero

    def get_dto(self) -> dict:
        return {"id": self._id,
                "nombre": self._nombre,
                "extrangero": self._extrangero
                }
