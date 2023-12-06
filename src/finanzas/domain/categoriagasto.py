class CategoriaGasto:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._descripcion = params.get("descripcion")
        self._id_cuenta_cargo_defecto = params.get("id_cuenta_cargo_defecto")
        self._nombre_cuenta_cargo_defecto = params.get("nombre_cuenta_cargo_defecto")
        self._id_monedero_defecto = params.get("id_monedero_defecto")
        self._nombre_monedero_defecto = params.get("nombre_monedero_defecto")

    def get_id(self) -> int:
        return self._id

    def get_descripcion(self) -> str:
        return self._descripcion

    def set_descripcion(self, descripcion: str):
        self._descripcion = descripcion

    def get_id_cuenta_cargo_defecto(self) -> int:
        return self._id_cuenta_cargo_defecto

    def set_id_cuenta_cargo_defecto(self, id_cuenta_cargo_defecto: int):
        self._id_cuenta_cargo_defecto = id_cuenta_cargo_defecto

    def get_nombre_cuenta_cargo_defecto(self) -> str:
        return self._nombre_cuenta_cargo_defecto

    def get_id_monedero_defecto(self) -> int:
        return self._id_monedero_defecto

    def set_id_monedero_defecto(self, id_monedero_defecto: int):
        self._id_monedero_defecto = id_monedero_defecto

    def get_nombre_monedero_defecto(self) -> str:
        return self._nombre_monedero_defecto

    def get_dto(self) -> dict:
        return {"id": self._id,
                "descripcion": self._descripcion,
                "id_cuenta_cargo_defecto": self._id_cuenta_cargo_defecto,
                "nombre_cuenta_cargo_defecto": self._nombre_cuenta_cargo_defecto,
                "id_monedero_defecto": self._id_monedero_defecto,
                "nombre_monedero_defecto": self._nombre_monedero_defecto,
                }
