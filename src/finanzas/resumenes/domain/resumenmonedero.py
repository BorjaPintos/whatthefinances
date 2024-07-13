class ResumenMonedero:

    def __init__(self, params: dict):
        self._año = params.get("año")
        self._mes = params.get("mes")
        self._total = params.get("total")
        self._id_monedero = params.get("id_monedero")
        self._nombre_monedero = params.get("nombre_monedero")

    def get_año(self) -> int:
        return self._año

    def get_mes(self) -> int:
        return self._mes

    def get_total(self) -> float:
        return self._total

    def get_id_monedero(self) -> int:
        return self._id_monedero

    def get_nombre_monedero(self) -> str:
        return self._nombre_monedero

    def get_dto(self) -> dict:
        return {
            "año": self._año,
            "mes": self._mes,
            "total": self._total,
            "id_monedero": self._id_monedero,
            "nombre_monedero": self._nombre_monedero,
        }
