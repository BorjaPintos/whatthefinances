class Cuenta:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._nombre = params.get("nombre")
        self._cantidad_base = params.get("cantidad_base")
        self._diferencia = params.get("diferencia")
        self._total = params.get("total")
        self._ponderacion = params.get("ponderacion")

    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def get_cantidad_base(self) -> float:
        return self._cantidad_base

    def get_diferencia(self) -> float:
        return self._diferencia

    def get_total(self) -> float:
        return self._total

    def get_ponderacion(self) -> int:
        return self._ponderacion

    def get_dto(self) -> dict:
        return {"id": self._id,
                "nombre": self._nombre,
                "cantidad_base": self._cantidad_base,
                "diferencia": self._diferencia,
                "total": self._total,
                "ponderacion": self._ponderacion
                }
