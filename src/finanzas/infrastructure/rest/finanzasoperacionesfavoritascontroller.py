from src.finanzas.application.createoperacionfavorita import CreateOperacionFavorita
from src.finanzas.application.deleteoperacionfavorita import DeleteOperacionFavorita
from src.finanzas.application.getoperacionfavorita import GetOperacionFavorita
from src.finanzas.application.listoperacionesfavoritas import ListOperacionesFavoritas
from src.finanzas.application.updateoperacionfavorita import UpdateOperacionFavorita
from src.finanzas.infrastructure.persistence.operacionfavoritarepositorysqlalchemy import \
    OperacionFavoritaRepositorySQLAlchemy
from src.finanzas.infrastructure.rest.localeutils import apply_locale_float, apply_locale_int, \
    apply_locale_list_int
from typing import Any, Tuple
from loguru import logger
from src.shared.domain.exceptions.messageerror import MessageError

operacion_favorita_repository = OperacionFavoritaRepositorySQLAlchemy()

list_operaciones_favoritas_use_case = ListOperacionesFavoritas(
    operacion_favorita_repository=operacion_favorita_repository)
get_operacion_favorita_use_case = GetOperacionFavorita(operacion_favorita_repository=operacion_favorita_repository)
create_operacion_favorita_use_case = CreateOperacionFavorita(
    operacion_favorita_repository=operacion_favorita_repository)

update_operacion_favorita_use_case = UpdateOperacionFavorita(
    operacion_favorita_repository=operacion_favorita_repository)

delete_operacion_favorita_use_case = DeleteOperacionFavorita(
    operacion_favorita_repository=operacion_favorita_repository)


def list_operaciones_favoritas(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_operaciones_favoritas_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return response_elements, code

def get_operacion_favorita(id_operacion_favorita: int) -> Tuple[Any, int]:
    code = 200
    operacion_favorita = get_operacion_favorita_use_case.execute(apply_locale_int(id_operacion_favorita))
    if operacion_favorita:
        response = operacion_favorita.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la operación favorita con id {} y no da la excepción de not found".format(
                id_operacion_favorita))
        raise MessageError("No se ha podido obtener la operación favorita con id: {}".format(id_operacion_favorita), code)
    return response, code

def create_operacion_favorita(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    created = create_operacion_favorita_use_case.execute(params)
    if created:
        response = {}
    else:
        code = 409
        logger.warning("Ya existe una operacion favorita con ese nombre: {}".format(params.get("nombre")))
        raise MessageError(
            "Parece que ya existe una operacion favorita con ese nombre: {}".format(params.get("nombre")),
            code)
    return response, code

def update_operacion_favorita(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    updated = update_operacion_favorita_use_case.execute(params)
    if updated:
        response = {}
    else:
        code = 400
        logger.warning("Error al actualizar la operación favorita con id: {}".format(params.get("id")))
        raise MessageError("Error al actualizar la operación favorita con id: {}".format(params.get("id")), code)
    return response, code


def delete_operacion_favorita(id_operacion_favorita: int) -> Tuple[Any, int]:
    code = 200
    operacion_favorita = delete_operacion_favorita_use_case.execute(apply_locale_int(id_operacion_favorita))
    if operacion_favorita:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar la operación favorita con id: {}".format(id_operacion_favorita))
        raise MessageError("Error al eliminar la operación favorita con id: {}".format(id_operacion_favorita), code)
    return response, code


def __cast_params(params: dict):
    if params.get("id") is not None:
        params["id"] = apply_locale_int(params["id"])

    if params.get("id_monedero_cargo") is not None:
        params["id_monedero_cargo"] = apply_locale_int(params["id_monedero_cargo"])
    if params.get("id_cuenta_cargo") is not None:
        params["id_cuenta_cargo"] = apply_locale_int(params["id_cuenta_cargo"])

    if params.get("id_monedero_abono") is not None:
        params["id_monedero_abono"] = apply_locale_int(params["id_monedero_abono"])
    if params.get("id_cuenta_abono") is not None:
        params["id_cuenta_abono"] = apply_locale_int(params["id_cuenta_abono"])

    if params.get("id_categoria_gasto") is not None:
        params["id_categoria_gasto"] = apply_locale_int(params["id_categoria_gasto"])
    if params.get("list_id_categoria_gasto") is not None:
        params["list_id_categoria_gasto"] = apply_locale_list_int(params["list_id_categoria_gasto"])
    if params.get("id_categoria_ingreso") is not None:
        params["id_categoria_ingreso"] = apply_locale_int(params["id_categoria_ingreso"])
    if params.get("list_id_categoria_ingreso") is not None:
        params["list_id_categoria_ingreso"] = apply_locale_list_int(params["list_id_categoria_ingreso"])

    if params.get("cantidad") is not None:
        params["cantidad"] = apply_locale_float(params["cantidad"])
    if params.get("begin_cantidad") is not None:
        params["begin_cantidad"] = apply_locale_float(params["begin_cantidad"])
    if params.get("end_cantidad") is not None:
        params["end_cantidad"] = apply_locale_float(params["end_cantidad"])
