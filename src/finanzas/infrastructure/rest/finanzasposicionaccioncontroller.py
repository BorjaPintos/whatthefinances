from typing import Any, Tuple
from loguru import logger

from src.finanzas.application.cerrarposicionaccion import CerrarPosicionAccion
from src.finanzas.application.createbolsa import CreateBolsa
from src.finanzas.application.createbroker import CreateBroker
from src.finanzas.application.createposicionaccion import CreatePosicionAccion
from src.finanzas.application.createvaloraccion import CreateValorAccion
from src.finanzas.application.deleteposicionaccion import DeletePosicionAccion
from src.finanzas.application.deletevaloraccion import DeleteValorAccion
from src.finanzas.application.deshacercerrarposicionaccion import DeshacerCerrarPosicionAccion
from src.finanzas.application.getbolsa import GetBolsa
from src.finanzas.application.getbroker import GetBroker
from src.finanzas.application.getposicionaccion import GetPosicionAccion
from src.finanzas.application.listbolsa import ListBolsa
from src.finanzas.application.listbroker import ListBroker
from src.finanzas.application.listposicionaccion import ListPosicionAccion
from src.finanzas.application.listvaloraccion import ListValorAccion
from src.finanzas.application.updatebolsa import UpdateBolsa
from src.finanzas.application.updatebroker import UpdateBroker
from src.finanzas.application.updateposicionaccion import UpdatePosicionAccion
from src.finanzas.infrastructure.persistence.bolsarepositorysqlalchemy import BolsaRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.brokerrepositorysqlalchemy import BrokerRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.posicionaccionrepositorysqlalchemy import \
    PosicionAccionRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.valoraccionnrepositorysqlalchemy import ValorAccionRepositorySQLAlchemy
from src.finanzas.infrastructure.rest.localeutils import apply_locale_float, apply_locale_int, apply_locale_date, \
    apply_locale_bool
from src.shared.domain.exceptions.messageerror import MessageError
from src.shared.infraestructure.rest.pagination import Pagination

broker_repository = BrokerRepositorySQLAlchemy()

list_brokers_use_case = ListBroker(broker_repository=broker_repository)
get_broker_use_case = GetBroker(broker_repository=broker_repository)
create_broker_use_case = CreateBroker(broker_repository=broker_repository)
update_broker_use_case = UpdateBroker(broker_repository=broker_repository)

bolsa_repository = BolsaRepositorySQLAlchemy()

list_bolsas_use_case = ListBolsa(bolsa_repository=bolsa_repository)
get_bolsa_use_case = GetBolsa(bolsa_repository=bolsa_repository)
create_bolsa_use_case = CreateBolsa(bolsa_repository=bolsa_repository)
update_bolsa_use_case = UpdateBolsa(bolsa_repository=bolsa_repository)

valor_accion_repository = ValorAccionRepositorySQLAlchemy()
list_valor_accion_use_case = ListValorAccion(valor_accion_repository=valor_accion_repository)
create_valor_accion_use_case = CreateValorAccion(valor_accion_repository=valor_accion_repository)
delete_valor_accion_use_case = DeleteValorAccion(valor_accion_repository=valor_accion_repository)

posicion_accion_repository = PosicionAccionRepositorySQLAlchemy()

list_posicion_accion_use_case = ListPosicionAccion(posicion_accion_repository=posicion_accion_repository)
get_posicion_accion_use_case = GetPosicionAccion(posicion_accion_repository=posicion_accion_repository)
create_posicion_accion_use_case = CreatePosicionAccion(posicion_accion_repository=posicion_accion_repository)
update_posicion_accion_use_case = UpdatePosicionAccion(posicion_accion_repository=posicion_accion_repository)
delete_posicion_accion_use_case = DeletePosicionAccion(posicion_accion_repository=posicion_accion_repository)
cerrar_posicion_accion_use_case = CerrarPosicionAccion(posicion_accion_repository=posicion_accion_repository)
deshacer_cerrar_posicion_accion_use_case = DeshacerCerrarPosicionAccion(
    posicion_accion_repository=posicion_accion_repository)


def list_brokers(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_brokers_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_broker(id_broker: int) -> Tuple[Any, int]:
    code = 200
    broker = get_broker_use_case.execute(apply_locale_int(id_broker))
    if broker:
        response = broker.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve el broker con id {} y no da la excepción de not found".format(id_broker))
        raise MessageError("No se ha podido obtener el broker con id: {}".format(id_broker), code)
    return response, code


def create_broker(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    broker = create_broker_use_case.execute(params)
    if broker:
        response = broker.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un broker con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un broker con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def update_broker(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    broker = update_broker_use_case.execute(params)
    if broker:
        response = broker.get_dto()

    else:
        code = 409
        logger.warning("Ya existe un broker con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un broker con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def list_bolsas(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_bolsas_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_bolsa(id_bolsa: int) -> Tuple[Any, int]:
    code = 200
    bolsa = get_bolsa_use_case.execute(apply_locale_int(id_bolsa))
    if bolsa:
        response = bolsa.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la bolsa con id {} y no da la excepción de not found".format(id_bolsa))
        raise MessageError("No se ha podido obtener la bolsa con id: {}".format(id_bolsa), code)
    return response, code


def create_bolsa(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    bolsa = create_bolsa_use_case.execute(params)
    if bolsa:
        response = bolsa.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una bolsa con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una bolsa con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def update_bolsa(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    bolsa = update_bolsa_use_case.execute(params)
    if bolsa:
        response = bolsa.get_dto()

    else:
        code = 409
        logger.warning("Ya existe una bolsa con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una bolsa con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def list_valores_acciones(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_valor_accion_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params["offset"], params["count"], total_elements), code


def create_valor_accion(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    valor_accion = create_valor_accion_use_case.execute(params)
    if valor_accion:
        response = valor_accion.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un valor_accion con esa fecha: {}".format(params.get("fecha")))
        raise MessageError("Parece que ya existe una valor accion con esa fecha: {}".format(params.get("fecha")), code)
    return response, code


def delete_valor_accion(id_valor_accion: int) -> Tuple[Any, int]:
    code = 200
    deleted = delete_valor_accion_use_case.execute(apply_locale_int(id_valor_accion))
    if deleted:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar el valor acción con id: {}".format(id_valor_accion))
        raise MessageError("Error al eliminar el valor acción con id: {}".format(id_valor_accion), code)
    return response, code


def list_posiciones_acciones(params: dict) -> Tuple[Pagination, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_posicion_accion_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params["offset"], params["count"], total_elements), code


def get_posicion_accion(id_posicion_accion: int) -> Tuple[Any, int]:
    code = 200
    cuenta = get_posicion_accion_use_case.execute(apply_locale_int(id_posicion_accion))
    if cuenta:
        response = cuenta.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la posición acción con id {} y no da la excepción de not found".format(
                id_posicion_accion))
        raise MessageError("No se ha podido obtener la posición acción con id: {}".format(id_posicion_accion), code)
    return response, code


def create_posicion_accion(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    created = create_posicion_accion_use_case.execute(params)
    if created:
        response = {}
    else:
        code = 400
        logger.warning("Error al crear la posición acción: {}".format(params.get("nombre")))
        raise MessageError("Error al crear la posición acción: {}".format(params.get("nombre")), code)
    return response, code


def update_posicion_accion(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    posicion_accion = update_posicion_accion_use_case.execute(params)
    if posicion_accion:
        response = posicion_accion.get_dto()
    else:
        code = 400
        logger.warning("Error al actualizar la posición acción con id: {}".format(params.get("id")))
        raise MessageError("Error al actualizar la posición acción con id: {}".format(params.get("id")), code)
    return response, code


def delete_posicion_accion(id_posicion_accion: int) -> Tuple[Any, int]:
    code = 200
    operacion = delete_posicion_accion_use_case.execute(apply_locale_int(id_posicion_accion))
    if operacion:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar la posición acción con id: {}".format(id_posicion_accion))
        raise MessageError("Error al eliminar la posición acción con id: {}".format(id_posicion_accion), code)
    return response, code


def cerrar_posicion_accion(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    posicion_accion = cerrar_posicion_accion_use_case.execute(params)
    if posicion_accion:
        response = posicion_accion.get_dto()

    else:
        code = 400
        logger.warning("Error al cerrar la posición acción con id: {}".format(params.get("id")))
        raise MessageError("Error al cerrar la posición acción con id: {}".format(params.get("id")), code)
    return response, code


def deshacer_cerrar_posicion_accion(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    posicion_accion = deshacer_cerrar_posicion_accion_use_case.execute(params)
    if posicion_accion:
        response = posicion_accion.get_dto()
    else:
        code = 400
        logger.warning("Error al deshacer-cerrar la posición acción con id: {}".format(params.get("id")))
        raise MessageError("Error al deshacer-cerrar la posición acción con id: {}".format(params.get("id")), code)
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

    if params.get("numero_acciones") is not None:
        params["numero_acciones"] = apply_locale_int(params["numero_acciones"])
    if params.get("begin_numero_acciones") is not None:
        params["begin_numero_acciones"] = apply_locale_int(params["begin_numero_acciones"])
    if params.get("end_numero_acciones") is not None:
        params["end_numero_acciones"] = apply_locale_int(params["end_numero_acciones"])

    if params.get("precio_accion_sin_comision") is not None:
        params["precio_accion_sin_comision"] = apply_locale_float(params["precio_accion_sin_comision"])
    if params.get("begin_precio_accion_sin_comision") is not None:
        params["begin_precio_accion_sin_comision"] = apply_locale_float(params["begin_precio_accion_sin_comision"])
    if params.get("end_precio_accion_sin_comision") is not None:
        params["end_precio_accion_sin_comision"] = apply_locale_float(params["end_precio_accion_sin_comision"])

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
