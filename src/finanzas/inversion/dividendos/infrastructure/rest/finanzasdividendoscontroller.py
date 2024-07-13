from typing import Any, Tuple
from loguru import logger

from src.finanzas.inversion.dividendos.application.createdividendo import CreateDividendo
from src.finanzas.inversion.dividendos.application.deletedividendo import DeleteDividendo
from src.finanzas.inversion.dividendos.application.getdividendo import GetDividendo
from src.finanzas.inversion.dividendos.application.listdividendorango import ListDividendoRango
from src.finanzas.inversion.dividendos.application.listdividendos import ListDividendos
from src.finanzas.inversion.dividendos.application.updatedividendo import UpdateDividendo
from src.finanzas.inversion.dividendos.infrastructure.persistence.dividendorepositorysqlalchemy import \
    DividendoRepositorySQLAlchemy
from src.finanzas.inversion.posiciones.infrastructure.persistence.posicionrepositorysqlalchemy import \
    PosicionRepositorySQLAlchemy
from src.shared.infraestructure.rest.commoncastparams import common_cast_params
from src.shared.utils.localeutils import apply_locale_float, apply_locale_int, apply_locale_date
from src.shared.domain.exceptions.messageerror import MessageError

dividendo_repository = DividendoRepositorySQLAlchemy()
list_dividendos_use_case = ListDividendos(dividendo_repository=dividendo_repository)
create_dividendo_use_case = CreateDividendo(dividendo_repository=dividendo_repository)
get_dividendo_use_case = GetDividendo(dividendo_repository=dividendo_repository)
update_dividendo_use_case = UpdateDividendo(dividendo_repository=dividendo_repository)
delete_dividendo_use_case = DeleteDividendo(dividendo_repository=dividendo_repository)

posicion_repository = PosicionRepositorySQLAlchemy()
list_dividendo_rango_use_case = ListDividendoRango(posicion_repository=posicion_repository)


def list_dividendos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_dividendos_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_dividendo(id_dividendo: int) -> Tuple[Any, int]:
    code = 200
    dividendo = get_dividendo_use_case.execute(apply_locale_int(id_dividendo))
    if dividendo:
        response = dividendo.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve el diviendo con id {} y no da la excepción de not found".format(id_dividendo))
        raise MessageError("No se ha podido obtener el diviendo con id: {}".format(id_dividendo), code)
    return response, code


def create_dividendo(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    dividendo = create_dividendo_use_case.execute(params)
    if dividendo:
        response = dividendo.get_dto()
    else:
        code = 400
        logger.warning("Error al crear el dividendo: {}".format(params.get("isin")))
        raise MessageError("Error al crear el dividendo: {}".format(params.get("isin")), code)
    return response, code


def update_dividendo(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)

    dividendo = update_dividendo_use_case.execute(params)
    if dividendo:
        response = dividendo.get_dto()
    else:
        code = 400
        logger.warning("Error al actualizar el dividendo: {}".format(params.get("isin")))
        raise MessageError("Error al actualizar el dividendo: {}".format(params.get("isin")), code)
    return response, code


def delete_dividendo(id_dividendo: int) -> Tuple[Any, int]:
    code = 200
    deleted = delete_dividendo_use_case.execute(apply_locale_int(id_dividendo))
    if deleted:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar el dividendo con id: {}".format(id_dividendo))
        raise MessageError("Error al eliminar el dividendo con id: {}".format(id_dividendo), code)
    return response, code


def list_dividendo_rango(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)

    elements = list_dividendo_rango_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return response_elements, code


def __cast_params(params: dict):
    common_cast_params(params)

    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_date(params["fecha"])
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])
    if params.get("dividendo_por_participacion") is not None:
        params["dividendo_por_participacion"] = apply_locale_float(params["dividendo_por_participacion"])
    if params.get("retencion_por_participacion") is not None:
        params["retencion_por_participacion"] = apply_locale_float(params["retencion_por_participacion"])

