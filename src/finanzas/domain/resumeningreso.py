class ResumenIngreso:

    def __init__(self, params: dict):
        self._año = params.get("año")
        self._mes = params.get("mes")
        self._total = params.get("total")
        self._id_categoria_ingreso = params.get("id_categoria_ingreso")
        self._descripcion_categoria_ingreso = params.get("descripcion_categoria_ingreso")

    def get_año(self) -> int:
        return self._año

    def get_mes(self) -> int:
        return self._mes

    def get_total(self) -> float:
        return self._total

    def get_id_categoria_ingreso(self) -> int:
        return self._id_categoria_ingreso

    def get_descripcion_categoria_ingreso(self) -> str:
        return self._descripcion_categoria_ingreso

    def get_dto(self) -> dict:
        return {
            "año": self._año,
            "mes": self._mes,
            "total": self._total,
            "id_categoria_ingreso": self._id_categoria_ingreso,
            "descripcion_categoria_ingreso": self._descripcion_categoria_ingreso,
        }
