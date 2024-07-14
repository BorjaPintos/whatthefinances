from typing import Any, Tuple
from loguru import logger

from src.finanzas.inversion.posiciones.application.cerrarposicion import CerrarPosicion
from src.finanzas.inversion.posiciones.application.createposicion import CreatePosicion
from src.finanzas.inversion.posiciones.application.deleteposicion import DeletePosicion
from src.finanzas.inversion.posiciones.application.deshacercerrarposicion import DeshacerCerrarPosicion
from src.finanzas.inversion.posiciones.application.getposicion import GetPosicion
from src.finanzas.inversion.posiciones.application.listposicion import ListPosicion
from src.finanzas.inversion.posiciones.application.updateposicion import UpdatePosicion
from src.finanzas.inversion.posiciones.infrastructure.persistence.posicionrepositorysqlalchemy import \
    PosicionRepositorySQLAlchemy
from src.shared.infraestructure.rest.commoncastparams import common_cast_params
from src.shared.utils.localeutils import apply_locale_float, apply_locale_int, apply_locale_date, \
    apply_locale_bool, apply_locale_list_int
from src.shared.domain.exceptions.messageerror import MessageError
from src.shared.infraestructure.rest.pagination import Pagination

posicion_repository = PosicionRepositorySQLAlchemy()

list_posicion_use_case = ListPosicion(posicion_repository=posicion_repository)
get_posicion_use_case = GetPosicion(posicion_repository=posicion_repository)
create_posicion_use_case = CreatePosicion(posicion_repository=posicion_repository)
update_posicion_use_case = UpdatePosicion(posicion_repository=posicion_repository)
delete_posicion_use_case = DeletePosicion(posicion_repository=posicion_repository)
cerrar_posicion_use_case = CerrarPosicion(posicion_repository=posicion_repository)
deshacer_cerrar_posicion_use_case = DeshacerCerrarPosicion(posicion_repository=posicion_repository)


def list_posiciones(params: dict) -> Tuple[Pagination, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_posicion_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params["offset"], params["count"], total_elements), code


def get_posicion(id_posicion: int) -> Tuple[Any, int]:
    code = 200
    cuenta = get_posicion_use_case.execute(apply_locale_int(id_posicion))
    if cuenta:
        response = cuenta.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la posición con id {} y no da la excepción de not found".format(
                id_posicion))
        raise MessageError("No se ha podido obtener la posición con id: {}".format(id_posicion), code)
    return response, code


def create_posicion(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    created = create_posicion_use_case.execute(params)
    if created:
        response = {}
    else:
        code = 400
        logger.warning("Error al crear la posición: {}".format(params.get("nombre")))
        raise MessageError("Error al crear la posición: {}".format(params.get("nombre")), code)
    return response, code


def update_posicion(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    posicion = update_posicion_use_case.execute(params)
    if posicion:
        response = posicion.get_dto()
    else:
        code = 400
        logger.warning("Error al actualizar la posición con id: {}".format(params.get("id")))
        raise MessageError("Error al actualizar la posición con id: {}".format(params.get("id")), code)
    return response, code


def delete_posicion(id_posicion: int) -> Tuple[Any, int]:
    code = 200
    deleted = delete_posicion_use_case.execute(apply_locale_int(id_posicion))
    if deleted:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar la posición con id: {}".format(id_posicion))
        raise MessageError("Error al eliminar la posición con id: {}".format(id_posicion), code)
    return response, code


def cerrar_posicion(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    posicion = cerrar_posicion_use_case.execute(params)
    if posicion:
        response = posicion.get_dto()

    else:
        code = 400
        logger.warning("Error al cerrar la posición con id: {}".format(params.get("id")))
        raise MessageError("Error al cerrar la posición con id: {}".format(params.get("id")), code)
    return response, code


def deshacer_cerrar_posicion(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    posicion = deshacer_cerrar_posicion_use_case.execute(params)
    if posicion:
        response = posicion.get_dto()
    else:
        code = 400
        logger.warning("Error al deshacer-cerrar la posición con id: {}".format(params.get("id")))
        raise MessageError("Error al deshacer-cerrar la posición con id: {}".format(params.get("id")), code)
    return response, code


def __cast_params(params: dict):
    common_cast_params(params)

    if params.get("list_id_broker") is not None:
        params["list_id_broker"] = apply_locale_list_int(params["list_id_broker"])
    if params.get("id_broker") is not None:
        params["id_broker"] = apply_locale_int(params["id_broker"])

    if params.get("id_bolsa") is not None:
        params["id_bolsa"] = apply_locale_int(params["id_bolsa"])

    if params.get("fecha_compra") is not None:
        params["fecha_compra"] = apply_locale_date(params["fecha_compra"])
    if params.get("begin_fecha_compra") is not None:
        params["begin_fecha_compra"] = apply_locale_date(params["begin_fecha_compra"])
    if params.get("end_fecha_compra") is not None:
        params["end_fecha_compra"] = apply_locale_date(params["end_fecha_compra"])

    if params.get("fecha_venta") is not None:
        params["fecha_venta"] = apply_locale_date(params["fecha_venta"])
    if params.get("begin_fecha_venta") is not None:
        params["begin_fecha_venta"] = apply_locale_date(params["begin_fecha_venta"])
    if params.get("end_fecha_venta") is not None:
        params["end_fecha_venta"] = apply_locale_date(params["end_fecha_venta"])

    if params.get("numero_participaciones") is not None:
        params["numero_participaciones"] = apply_locale_float(params["numero_participaciones"])
    if params.get("begin_numero_participaciones") is not None:
        params["begin_numero_participaciones"] = apply_locale_float(params["begin_numero_participaciones"])
    if params.get("end_numero_participaciones") is not None:
        params["end_numero_participaciones"] = apply_locale_float(params["end_numero_participaciones"])

    if params.get("precio_compra_sin_comision") is not None:
        params["precio_compra_sin_comision"] = apply_locale_float(params["precio_compra_sin_comision"])
    if params.get("begin_precio_compra_sin_comision") is not None:
        params["begin_precio_compra_sin_comision"] = apply_locale_float(params["begin_precio_compra_sin_comision"])
    if params.get("end_precio_compra_sin_comision") is not None:
        params["end_precio_compra_sin_comision"] = apply_locale_float(params["end_precio_compra_sin_comision"])

    if params.get("comision_compra") is not None:
        params["comision_compra"] = apply_locale_float(params["comision_compra"])
    if params.get("begin_comision_compra") is not None:
        params["begin_comision_compra"] = apply_locale_float(params["begin_comision_compra"])
    if params.get("end_comision_compra") is not None:
        params["end_comision_compra"] = apply_locale_float(params["end_comision_compra"])

    if params.get("comision_venta") is not None:
        params["comision_venta"] = apply_locale_float(params["comision_venta"])
    if params.get("begin_comision_venta") is not None:
        params["begin_comision_venta"] = apply_locale_float(params["begin_comision_venta"])
    if params.get("end_comision_venta") is not None:
        params["end_comision_venta"] = apply_locale_float(params["end_comision_venta"])

    if params.get("otras_comisiones") is not None:
        params["otras_comisiones"] = apply_locale_float(params["otras_comisiones"])
    if params.get("begin_otras_comisiones") is not None:
        params["begin_otras_comisiones"] = apply_locale_float(params["begin_otras_comisiones"])
    if params.get("end_otras_comisiones") is not None:
        params["end_otras_comisiones"] = apply_locale_float(params["end_otras_comisiones"])

    if params.get("abierta") is not None:
        params["abierta"] = apply_locale_bool(params["abierta"])
