class CategoriaIngreso:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._descripcion = params.get("descripcion")
        self._id_cuenta_abono_defecto = params.get("id_cuenta_abono_defecto")
        self._id_monedero_defecto = params.get("id_monedero_defecto")

    def get_id(self) -> int:
        return self._id

    def get_descripcion(self) -> str:
        return self._descripcion

    def get_id_cuenta_abono_defecto(self) -> int:
        return self._id_cuenta_abono_defecto

    def get_id_monedero_defecto(self) -> int:
        return self._id_monedero_defecto


    def get_dto(self) -> dict:
        return {"id": self._id,
                "descripcion": self._descripcion,
                "id_cuenta_abono_defecto": self._id_cuenta_abono_defecto,
                "id_monedero_defecto": self._id_monedero_defecto
                }
