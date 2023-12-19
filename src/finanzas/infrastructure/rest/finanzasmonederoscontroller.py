from src.finanzas.infrastructure.rest.localeutils import apply_locale_int, apply_locale_float
from typing import Any, Tuple
from loguru import logger
from src.finanzas.application.createmonedero import CreateMonedero
from src.finanzas.application.getmonedero import GetMonedero
from src.finanzas.application.listmonederos import ListMonederos
from src.finanzas.application.updatemonedero import UpdateMonedero
from src.finanzas.infrastructure.persistence.monederorepositorysqlalchemy import MonederoRepositorySQLAlchemy
from src.shared.domain.exceptions.messageerror import MessageError

monedero_repository = MonederoRepositorySQLAlchemy()

list_monederos_use_case = ListMonederos(monedero_repository=monedero_repository)
get_monedero_use_case = GetMonedero(monedero_repository=monedero_repository)
create_monedero_use_case = CreateMonedero(monedero_repository=monedero_repository)
update_monedero_use_case = UpdateMonedero(monedero_repository=monedero_repository)


def list_monederos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_monederos_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_monedero(id_monedero: int) -> Tuple[Any, int]:
    code = 200
    monedero = get_monedero_use_case.execute(apply_locale_int(id_monedero))
    if monedero:
        response = monedero.get_dto()
    else:
        logger.warning(
            "Por alguna razón no devuelve el monedero con id {} y no da la excepción de not found".format(
                id_monedero))
        raise MessageError("No se ha podido obtener el monedero con id: {}".format(id_monedero), code)
    return response, code


def create_monedero(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    monedero = create_monedero_use_case.execute(params)
    if monedero:
        response = monedero.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un monedero con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un monedero con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def update_monedero(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    monedero = update_monedero_use_case.execute(params)
    if monedero:
        response = monedero.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un monedero con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un monedero con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def __cast_params(params: dict):
    if params.get("id") is not None:
        params["id"] = apply_locale_int(params["id"])

    if params.get("cantidad_inicial") is not None:
        params["cantidad_inicial"] = apply_locale_float(params["cantidad_inicial"])

    if params.get("cantidad") is not None:
        params["cantidad"] = apply_locale_float(params["cantidad"])
    if params.get("begin_cantidad") is not None:
        params["begin_cantidad"] = apply_locale_float(params["begin_cantidad"])
    if params.get("end_cantidad") is not None:
        params["end_cantidad"] = apply_locale_float(params["end_cantidad"])
