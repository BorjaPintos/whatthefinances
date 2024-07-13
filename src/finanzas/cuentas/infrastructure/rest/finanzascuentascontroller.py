
from typing import Any, Tuple
from loguru import logger
from src.finanzas.cuentas.application.createcuenta import CreateCuenta
from src.finanzas.cuentas.application.getcuenta import GetCuenta
from src.finanzas.cuentas.application.listcuentas import ListCuentas
from src.finanzas.cuentas.application.updatecuenta import UpdateCuenta
from src.finanzas.cuentas.infrastructure.persistence.cuentarepositorysqlalchemy import CuentaRepositorySQLAlchemy
from src.shared.utils.localeutils import apply_locale_float, apply_locale_int
from src.shared.domain.exceptions.messageerror import MessageError


cuenta_repository = CuentaRepositorySQLAlchemy()

list_cuentas_use_case = ListCuentas(cuenta_repository=cuenta_repository)
get_cuenta_use_case = GetCuenta(cuenta_repository=cuenta_repository)
create_cuenta_use_case = CreateCuenta(cuenta_repository=cuenta_repository)
update_cuenta_use_case = UpdateCuenta(cuenta_repository=cuenta_repository)


def list_cuentas(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_cuentas_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_cuenta(id_cuenta: int) -> Tuple[Any, int]:
    code = 200
    cuenta = get_cuenta_use_case.execute(apply_locale_int(id_cuenta))
    if cuenta:
        response = cuenta.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la cuenta con id {} y no da la excepción de not found".format(id_cuenta))
        raise MessageError("No se ha podido obtener la cuenta con id: {}".format(id_cuenta), code)
    return response, code


def create_cuenta(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    cuenta = create_cuenta_use_case.execute(params)
    if cuenta:
        response = cuenta.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una cuenta con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una cuenta con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def update_cuenta(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    cuenta = update_cuenta_use_case.execute(params)
    if cuenta:
        response = cuenta.get_dto()

    else:
        code = 409
        logger.warning("Ya existe una cuenta con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una cuenta con ese nombre: {}".format(params.get("nombre")), code)
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
    if params.get("ponderacion") is not None:
        params["ponderacion"] = apply_locale_float(params["ponderacion"])



