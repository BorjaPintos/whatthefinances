from datetime import date


class Operacion:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._fecha = params.get("fecha")
        self._cantidad = params.get("cantidad")
        self._descripcion = params.get("descripcion")
        self._id_categoria_gasto = params.get("id_categoria_gasto")
        self._descripcion_categoria_gasto = params.get("descripcion_categoria_gasto")
        self._id_cuenta_cargo = params.get("id_cuenta_cargo")
        self._nombre_cuenta_cargo = params.get("nombre_cuenta_cargo")
        self._id_monedero_cargo = params.get("id_monedero_cargo")
        self._nombre_monedero_cargo = params.get("nombre_monedero_cargo")
        self._id_categoria_ingreso = params.get("id_categoria_ingreso")
        self._descripcion_categoria_ingreso = params.get("descripcion_categoria_ingreso")
        self._id_cuenta_abono = params.get("id_cuenta_abono")
        self._nombre_cuenta_abono = params.get("nombre_cuenta_abono")
        self._id_monedero_abono = params.get("id_monedero_abono")
        self._nombre_monedero_abono = params.get("nombre_monedero_abono")

    def get_id(self) -> int:
        return self._id

    def get_fecha(self) -> date:
        return self._fecha

    def set_fecha(self, fecha: date):
        self._fecha= fecha

    def get_cantidad(self) -> float:
        return self._cantidad

    def set_cantidad(self, cantidad: float):
        self._cantidad = cantidad

    def get_descripcion(self) -> str:
        return self._descripcion

    def set_descripcion(self, descripcion: str):
        self._descripcion = descripcion

    def get_id_categoria_gasto(self) -> int:
        return self._id_categoria_gasto

    def set_id_categoria_gasto(self, id_categoria_gasto: int):
        self._id_categoria_gasto = id_categoria_gasto

    def get_descripcion_categoria_gasto(self) -> str:
        return self._descripcion_categoria_gasto

    def get_id_cuenta_cargo(self) -> int:
        return self._id_cuenta_cargo

    def set_id_cuenta_cargo(self, id_cuenta_cargo: int):
        self._id_cuenta_cargo = id_cuenta_cargo

    def get_nombre_cuenta_cargo(self) -> str:
        return self._nombre_cuenta_cargo

    def get_id_monedero_cargo(self) -> int:
        return self._id_monedero_cargo

    def set_id_monedero_cargo(self, id_monedero_cargo: int):
        self._id_monedero_cargo = id_monedero_cargo

    def get_nombre_monedero_cargo(self) -> str:
        return self._nombre_monedero_cargo

    def get_id_categoria_ingreso(self) -> int:
        return self._id_categoria_ingreso

    def set_id_categoria_ingreso(self, id_categoria_ingreso: int):
        self._id_categoria_ingreso = id_categoria_ingreso

    def get_descripcion_categoria_ingreso(self) -> str:
        return self._descripcion_categoria_ingreso

    def get_id_cuenta_abono(self) -> int:
        return self._id_cuenta_abono

    def set_id_cuenta_abono(self, id_cuenta_abono: int):
        self._id_cuenta_abono = id_cuenta_abono

    def get_nombre_cuenta_abono(self) -> str:
        return self._nombre_cuenta_abono

    def get_id_monedero_abono(self) -> int:
        return self._id_monedero_abono

    def set_id_monedero_abono(self, id_monedero_abono: int):
        self._id_monedero_abono = id_monedero_abono

    def get_nombre_monedero_abono(self) -> str:
        return self._nombre_monedero_abono

    def get_dto(self) -> dict:
        return {"id": self._id,
                "fecha": self._fecha.strftime("%d/%m/%Y"),
                "cantidad": self._cantidad,
                "descripcion": self._descripcion,
                "id_categoria_gasto": self._id_categoria_gasto,
                "descripcion_categoria_gasto": self._descripcion_categoria_gasto,
                "id_cuenta_cargo": self._id_cuenta_cargo,
                "nombre_cuenta_cargo": self._nombre_cuenta_cargo,
                "id_monedero_cargo": self._id_monedero_cargo,
                "nombre_monedero_cargo": self._nombre_monedero_cargo,
                "id_categoria_ingreso": self._id_categoria_ingreso,
                "descripcion_categoria_ingreso": self._descripcion_categoria_ingreso,
                "id_cuenta_abono": self._id_cuenta_abono,
                "nombre_cuenta_abono": self._nombre_cuenta_abono,
                "id_monedero_abono": self._id_monedero_abono,
                "nombre_monedero_abono": self._nombre_monedero_abono
                }
