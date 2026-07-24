from src.shared.utils.localeutils import apply_locale_date, apply_locale_int
from src.shared.infraestructure.rest.pagination import Pagination

from typing import Any, Tuple

from src.finanzas.cuentas.application.getcuenta import GetCuenta
from src.finanzas.cuentas.application.listmovimientoscuenta import ListMovimientosCuenta
from src.finanzas.cuentas.infrastructure.persistence.movimientocuentarepositorysqlalchemy import \
    MovimientoCuentaRepositorySQLAlchemy
from src.finanzas.cuentas.infrastructure.persistence.cuentarepositorysqlalchemy import CuentaRepositorySQLAlchemy

movimiento_cuenta_repository = MovimientoCuentaRepositorySQLAlchemy()
cuenta_repository = CuentaRepositorySQLAlchemy()

list_movimientos_cuenta_use_case = ListMovimientosCuenta(
    movimiento_cuenta_repository=movimiento_cuenta_repository)
get_cuenta_use_case = GetCuenta(cuenta_repository=cuenta_repository)


def list_movimientos_cuenta(params: dict) -> Tuple[Pagination, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_movimientos_cuenta_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params.get("offset", 0), params.get("count", 30), total_elements), code


def __cast_params(params: dict):
    if params.get("id_cuenta") is not None:
        params["id_cuenta"] = apply_locale_int(params["id_cuenta"])
    if params.get("count") is not None:
        params["count"] = apply_locale_int(params["count"])
        if params["count"] <= 0:
            params["count"] = 1
    if params.get("offset") is not None:
        params["offset"] = apply_locale_int(params["offset"])
        if params["offset"] < 0:
            params["offset"] = 0
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])
    if params.get("id_categoria_gasto") is not None:
        params["id_categoria_gasto"] = apply_locale_int(params["id_categoria_gasto"])
    if params.get("id_categoria_ingreso") is not None:
        params["id_categoria_ingreso"] = apply_locale_int(params["id_categoria_ingreso"])
