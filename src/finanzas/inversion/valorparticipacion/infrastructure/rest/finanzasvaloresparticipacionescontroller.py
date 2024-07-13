from typing import Any, Tuple, List
from loguru import logger

from src.finanzas.inversion.valorparticipacion.application.autocreatevalorparticipacion import AutoCreateValorParticipacion
from src.finanzas.inversion.valorparticipacion.application.createvalorparticipacion import CreateValorParticipacion
from src.finanzas.inversion.valorparticipacion.application.deletevalorparticipacion import DeleteValorParticipacion
from src.finanzas.inversion.producto.application.getthirdapivalueproduct import GetThirdApiValueProduct
from src.finanzas.inversion.valorparticipacion.application.listvalorparticipacion import ListValorParticipacion
from src.finanzas.inversion.producto.infrastructure.persistence.productorepositorysqlalchemy import \
    ProductoRepositorySQLAlchemy
from src.finanzas.inversion.valorparticipacion.infrastructure.persistence.valorparticipacionrepositorysqlalchemy import \
    ValorParticipacionRepositorySQLAlchemy
from src.shared.infraestructure.rest.commoncastparams import common_cast_params
from src.shared.utils.localeutils import apply_locale_float, apply_locale_int, apply_locale_date
from src.shared.domain.exceptions.messageerror import MessageError
from src.shared.infraestructure.rest.pagination import Pagination

producto_repository = ProductoRepositorySQLAlchemy()

valor_participacion_repository = ValorParticipacionRepositorySQLAlchemy()
list_valor_participacion_use_case = ListValorParticipacion(
    valor_participacion_repository=valor_participacion_repository)
create_valor_participacion_use_case = CreateValorParticipacion(
    valor_participacion_repository=valor_participacion_repository)
delete_valor_participacion_use_case = DeleteValorParticipacion(
    valor_participacion_repository=valor_participacion_repository)

third_api_value_product_use_case = GetThirdApiValueProduct({})
auto_create_valor_participacion_use_case = AutoCreateValorParticipacion(producto_repository=producto_repository,
                                                                        valor_participacion_repository=valor_participacion_repository,
                                                                        third_api_value_product_use_case=third_api_value_product_use_case)


def list_valores_participaciones(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_valor_participacion_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params["offset"], params["count"], total_elements), code


def create_valor_participacion(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    valor_participacion = create_valor_participacion_use_case.execute(params)
    if valor_participacion:
        response = valor_participacion.get_dto()
    else:
        logger.warning("Error al crear el valor participacón {}")
        raise MessageError("Error al crear el valor participación {}", code)
    return response, code


def auto_create_valor_participacion(isin_list: List[str] = None) -> Tuple[Any, int]:
    code = 200
    response = auto_create_valor_participacion_use_case.execute(isin_list)
    return response, code


def delete_valor_participacion(id_valor_participacion: int) -> Tuple[Any, int]:
    code = 200
    deleted = delete_valor_participacion_use_case.execute(apply_locale_int(id_valor_participacion))
    if deleted:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar el valor participación con id: {}".format(id_valor_participacion))
        raise MessageError("Error al eliminar el valor participación con id: {}".format(id_valor_participacion), code)
    return response, code


def __cast_params(params: dict):
    common_cast_params(params)

    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_date(params["fecha"])
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])
    if params.get("valor") is not None:
        params["valor"] = apply_locale_float(params["valor"])
