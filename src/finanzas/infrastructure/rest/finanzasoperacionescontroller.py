from src.finanzas.infrastructure.persistence.movimientocuentarepositorysqlalchemy import \
    MovimientoCuentaRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.movimientomonederorepositorysqlalchemy import \
    MovimientoMonederoRepositorySQLAlchemy
from src.shared.utils.localeutils import apply_locale_date, apply_locale_float, apply_locale_int, \
    apply_locale_list_int
from src.shared.infraestructure.rest.pagination import Pagination

from typing import Any, Tuple
from loguru import logger
from src.finanzas.application.createoperacion import CreateOperacion
from src.finanzas.application.deleteoperacion import DeleteOperacion
from src.finanzas.application.getoperacion import GetOperacion
from src.finanzas.application.listoperaciones import ListOperaciones
from src.finanzas.application.updateoperacion import UpdateOperacion
from src.finanzas.infrastructure.persistence.cuentarepositorysqlalchemy import CuentaRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.monederorepositorysqlalchemy import MonederoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.operacionrepositorysqlalchemy import OperacionRepositorySQLAlchemy
from src.shared.domain.exceptions.messageerror import MessageError

cuenta_repository = CuentaRepositorySQLAlchemy()
movimiento_cuenta_repository = MovimientoCuentaRepositorySQLAlchemy()
monedero_repository = MonederoRepositorySQLAlchemy()
movimiento_monedero_repository = MovimientoMonederoRepositorySQLAlchemy()
operacion_repository = OperacionRepositorySQLAlchemy()

list_operaciones_use_case = ListOperaciones(operacion_repository=operacion_repository)
get_operacion_use_case = GetOperacion(operacion_repository=operacion_repository)
create_operacion_use_case = CreateOperacion(operacion_repository=operacion_repository,
                                            monedero_repository=monedero_repository,
                                            movimiento_monedero_repository=movimiento_monedero_repository,
                                            cuenta_repository=cuenta_repository,
                                            movimiento_cuenta_repository=movimiento_cuenta_repository)
update_operacion_use_case = UpdateOperacion(operacion_repository=operacion_repository,
                                            monedero_repository=monedero_repository,
                                            movimiento_monedero_repository=movimiento_monedero_repository,
                                            cuenta_repository=cuenta_repository,
                                            movimiento_cuenta_repository=movimiento_cuenta_repository)
delete_operacion_use_case = DeleteOperacion(operacion_repository=operacion_repository,
                                            monedero_repository=monedero_repository,
                                            movimiento_monedero_repository=movimiento_monedero_repository,
                                            cuenta_repository=cuenta_repository,
                                            movimiento_cuenta_repository=movimiento_cuenta_repository)


def list_operaciones(params: dict) -> Tuple[Pagination, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_operaciones_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params["offset"], params["count"], total_elements), code


def get_operacion(id_operacion: int) -> Tuple[Any, int]:
    code = 200
    operacion = get_operacion_use_case.execute(apply_locale_int(id_operacion))
    if operacion:
        response = operacion.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la operación con id {} y no da la excepción de not found".format(
                id_operacion))
        raise MessageError("No se ha podido obtener la operación con id: {}".format(id_operacion), code)
    return response, code


def create_operacion(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    created = create_operacion_use_case.execute(params)
    if created:
        response = {}
    else:
        code = 400
        logger.warning("Error al crear la operacion: {}".format(params.get("descripcion")))
        raise MessageError("Error al crear la operacion: {}".format(params.get("descripcion")), code)
    return response, code


def update_operacion(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    updated = update_operacion_use_case.execute(params)
    if updated:
        response = {}
    else:
        code = 400
        logger.warning("Error al actualizar la operación con id: {}".format(params.get("id")))
        raise MessageError("Error al actualizar la operación con id: {}".format(params.get("id")), code)
    return response, code


def delete_operacion(id_operacion: int) -> Tuple[Any, int]:
    code = 200
    operacion = delete_operacion_use_case.execute(apply_locale_int(id_operacion))
    if operacion:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar la operación con id: {}".format(id_operacion))
        raise MessageError("Error al eliminar la operación con id: {}".format(id_operacion), code)
    return response, code


def __cast_params(params: dict):
    if params.get("id") is not None:
        params["id"] = apply_locale_int(params["id"])
    if params.get("count") is not None:
        params["count"] = apply_locale_int(params["count"])
        if params["count"] <= 0:
            params["count"] = 1
    if params.get("offset") is not None:
        params["offset"] = apply_locale_int(params["offset"])
        if params["offset"] < 0:
            params["offset"] = 0

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

    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_date(params["fecha"])
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])
