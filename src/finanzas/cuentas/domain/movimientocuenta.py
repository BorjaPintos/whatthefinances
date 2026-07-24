from datetime import date


class MovimientoCuenta:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._fecha = params.get("fecha")
        self._cantidad = params.get("cantidad")
        self._id_operacion = params.get("id_operacion")
        self._id_cuenta = params.get("id_cuenta")
        self._descripcion = params.get("descripcion")
        self._id_categoria_gasto = params.get("id_categoria_gasto")
        self._id_categoria_ingreso = params.get("id_categoria_ingreso")

    def get_id(self) -> int:
        return self._id

    def get_fecha(self) -> date:
        return self._fecha

    def get_cantidad(self) -> float:
        return self._cantidad

    def get_id_operacion(self) -> int:
        return self._id_operacion

    def get_id_cuenta(self) -> int:
        return self._id_cuenta

    def get_descripcion(self) -> str:
        return self._descripcion

    def get_id_categoria_gasto(self) -> int:
        return self._id_categoria_gasto

    def get_id_categoria_ingreso(self) -> int:
        return self._id_categoria_ingreso

    def get_dto(self) -> dict:
        return {"id": self._id,
                "fecha": self._fecha.strftime("%d/%m/%Y"),
                "cantidad": self._cantidad,
                "id_operacion": self._id_operacion,
                "id_cuenta": self._id_cuenta,
                "descripcion": self._descripcion,
                "id_categoria_gasto": self._id_categoria_gasto,
                "id_categoria_ingreso": self._id_categoria_ingreso,
                }
