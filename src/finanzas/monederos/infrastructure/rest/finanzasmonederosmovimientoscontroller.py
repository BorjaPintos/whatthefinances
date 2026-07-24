from src.shared.utils.localeutils import apply_locale_date, apply_locale_int
from src.shared.infraestructure.rest.pagination import Pagination

from typing import Any, Tuple

from src.finanzas.monederos.application.listmovimientosmonedero import ListMovimientosMonedero
from src.finanzas.monederos.infrastructure.persistence.movimientomonederorepositorysqlalchemy import \
    MovimientoMonederoRepositorySQLAlchemy
from src.finanzas.monederos.infrastructure.persistence.monederorepositorysqlalchemy import MonederoRepositorySQLAlchemy
from src.finanzas.monederos.application.getmonedero import GetMonedero

movimiento_monedero_repository = MovimientoMonederoRepositorySQLAlchemy()
monedero_repository = MonederoRepositorySQLAlchemy()

list_movimientos_monedero_use_case = ListMovimientosMonedero(
    movimiento_monedero_repository=movimiento_monedero_repository)



def list_movimientos_monedero(params: dict) -> Tuple[Pagination, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_movimientos_monedero_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params.get("offset", 0), params.get("count", 30), total_elements), code


def __cast_params(params: dict):
    if params.get("id_monedero") is not None:
        params["id_monedero"] = apply_locale_int(params["id_monedero"])
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
