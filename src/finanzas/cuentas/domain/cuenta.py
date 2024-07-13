class Cuenta:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._nombre = params.get("nombre")
        self._cantidad_inicial = params.get("cantidad_inicial")
        self._diferencia = params.get("diferencia")
        self._ponderacion = params.get("ponderacion")

    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def set_nombre(self, nombre: str):
        self._nombre = nombre

    def get_cantidad_inicial(self) -> float:
        return self._cantidad_inicial

    def set_cantidad_inicial(self, cantidad_inicial: float):
        self._cantidad_inicial = cantidad_inicial

    def get_diferencia(self) -> float:
        return self._diferencia

    def set_diferencia(self, diferencia: float):
        self._diferencia = diferencia

    def get_total(self) -> float:
        return self._cantidad_inicial + self._diferencia

    def get_ponderacion(self) -> int:
        return self._ponderacion

    def set_ponderacion(self, ponderacion: float):
        self._ponderacion = ponderacion

    def get_dto(self) -> dict:
        return {"id": self._id,
                "nombre": self._nombre,
                "cantidad_inicial": self._cantidad_inicial,
                "diferencia": self._diferencia,
                "total": self.get_total(),
                "ponderacion": self._ponderacion
                }
