from src.finanzas.application.resumencuentas import ResumenCuentas
from src.finanzas.application.resumengastos import ResumenGastos
from src.finanzas.application.resumeningresos import ResumenIngresos
from src.finanzas.application.resumenmonederos import ResumenMonederos
from src.finanzas.application.resumentotales import ResumenTotales
from src.finanzas.application.resumenvaloresaccionesdias import ResumenValoresAccionesDias
from src.finanzas.application.resumenvaloresaccionesmeses import ResumenValoresAccionesMeses
from src.finanzas.infrastructure.persistence.resumenrepositorysqlalchemy import ResumenRepositorySQLAlchemy
from src.finanzas.infrastructure.rest.localeutils import apply_locale_date, apply_locale_float, apply_locale_int
from src.shared.infraestructure.rest.pagination import Pagination
from typing import Any, Tuple
from loguru import logger
from src.shared.domain.exceptions.messageerror import MessageError

resumen_repository = ResumenRepositorySQLAlchemy()

resumen_ingresos_use_case = ResumenIngresos(resumen_repository=resumen_repository)
resumen_gastos_use_case = ResumenGastos(resumen_repository=resumen_repository)
resumen_cuentas_use_case = ResumenCuentas(resumen_repository=resumen_repository)
resumen_monederos_use_case = ResumenMonederos(resumen_repository=resumen_repository)
resumen_total_use_case = ResumenTotales(resumen_repository=resumen_repository)
resumen_valores_acciones_meses_use_case = ResumenValoresAccionesMeses(resumen_repository=resumen_repository)
resumen_valores_acciones_dias_use_case = ResumenValoresAccionesDias(resumen_repository=resumen_repository)


def resumen_ingresos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_ingresos_use_case.execute(params)
    response_elements = []
    for element in response:
        response_elements.append(element.get_dto())
    return response_elements, code


def resumen_gastos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_gastos_use_case.execute(params)
    response_elements = []
    for element in response:
        response_elements.append(element.get_dto())
    return response_elements, code


def resumen_cuentas(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_cuentas_use_case.execute(params)
    response_elements = []
    for element in response:
        response_elements.append(element.get_dto())
    return response_elements, code


def resumen_monederos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_monederos_use_case.execute(params)
    response_elements = []
    for element in response:
        response_elements.append(element.get_dto())
    return response_elements, code


def resumen_total(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_total_use_case.execute(params)
    response_elements = []
    for element in response:
        response_elements.append(element.get_dto())
    return response_elements, code


def resumen_valores_acciones_meses(params) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_valores_acciones_meses_use_case.execute(params)
    response_elements = []
    for element in response:
        response_elements.append(element.get_dto())
    return response_elements, code


def resumen_valores_acciones_dias(params) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_valores_acciones_meses_use_case.execute(params)
    response_elements = []
    for element in response:
        response_elements.append(element.get_dto())
    return response_elements, code


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

    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_date(params["fecha"])
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])
