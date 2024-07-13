class ResumenTotal:

    def __init__(self, params: dict):
        self._año = params.get("año")
        self._mes = params.get("mes")
        self._total = params.get("total")

    def get_año(self) -> int:
        return self._año

    def get_mes(self) -> int:
        return self._mes

    def get_total(self) -> float:
        return self._total

    def get_dto(self) -> dict:
        return {
            "año": self._año,
            "mes": self._mes,
            "total": self._total
        }
