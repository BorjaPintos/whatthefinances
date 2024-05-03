from typing import Any, Tuple
from loguru import logger

from src.finanzas.application.cerrarposicion import CerrarPosicion
from src.finanzas.application.createbolsa import CreateBolsa
from src.finanzas.application.createbroker import CreateBroker
from src.finanzas.application.createdividendo import CreateDividendo
from src.finanzas.application.createposicion import CreatePosicion
from src.finanzas.application.createproducto import CreateProducto
from src.finanzas.application.createvalorparticipacion import CreateValorParticipacion
from src.finanzas.application.deletedividendo import DeleteDividendo
from src.finanzas.application.deleteposicion import DeletePosicion
from src.finanzas.application.deletevalorparticipacion import DeleteValorParticipacion
from src.finanzas.application.deshacercerrarposicion import DeshacerCerrarPosicion
from src.finanzas.application.getbolsa import GetBolsa
from src.finanzas.application.getbroker import GetBroker
from src.finanzas.application.getdividendo import GetDividendo
from src.finanzas.application.getposicion import GetPosicion
from src.finanzas.application.getproducto import GetProducto
from src.finanzas.application.listbolsa import ListBolsa
from src.finanzas.application.listbroker import ListBroker
from src.finanzas.application.listdividendorango import ListDividendoRango
from src.finanzas.application.listdividendos import ListDividendos
from src.finanzas.application.listposicion import ListPosicion
from src.finanzas.application.listproducto import ListProducto
from src.finanzas.application.listvalorparticipacion import ListValorParticipacion
from src.finanzas.application.updatebolsa import UpdateBolsa
from src.finanzas.application.updatebroker import UpdateBroker
from src.finanzas.application.updatedividendo import UpdateDividendo
from src.finanzas.application.updateposicion import UpdatePosicion
from src.finanzas.application.updateproducto import UpdateProducto
from src.finanzas.infrastructure.persistence.bolsarepositorysqlalchemy import BolsaRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.brokerrepositorysqlalchemy import BrokerRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.dividendorepositorysqlalchemy import DividendoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.posicionrepositorysqlalchemy import \
    PosicionRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.productorepositorysqlalchemy import ProductoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.valorparticipacionrepositorysqlalchemy import ValorParticipacionRepositorySQLAlchemy
from src.finanzas.infrastructure.rest.localeutils import apply_locale_float, apply_locale_int, apply_locale_date, \
    apply_locale_bool, apply_locale_datetime, apply_locale_list_int, apply_locale_list
from src.shared.domain.exceptions.messageerror import MessageError
from src.shared.infraestructure.rest.pagination import Pagination

producto_repository = ProductoRepositorySQLAlchemy()

list_productos_use_case = ListProducto(producto_repository=producto_repository)
get_producto_use_case = GetProducto(producto_repository=producto_repository)
create_producto_use_case = CreateProducto(producto_repository=producto_repository)
update_producto_use_case = UpdateProducto(producto_repository=producto_repository)

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

valor_participacion_repository = ValorParticipacionRepositorySQLAlchemy()
list_valor_participacion_use_case = ListValorParticipacion(valor_participacion_repository=valor_participacion_repository)
create_valor_participacion_use_case = CreateValorParticipacion(valor_participacion_repository=valor_participacion_repository)
delete_valor_participacion_use_case = DeleteValorParticipacion(valor_participacion_repository=valor_participacion_repository)

dividendo_repository = DividendoRepositorySQLAlchemy()
list_dividendos_use_case = ListDividendos(dividendo_repository=dividendo_repository)
create_dividendo_use_case = CreateDividendo(dividendo_repository=dividendo_repository)
get_dividendo_use_case = GetDividendo(dividendo_repository=dividendo_repository)
update_dividendo_use_case = UpdateDividendo(dividendo_repository=dividendo_repository)
delete_dividendo_use_case = DeleteDividendo(dividendo_repository=dividendo_repository)

posicion_repository = PosicionRepositorySQLAlchemy()

list_posicion_use_case = ListPosicion(posicion_repository=posicion_repository)
get_posicion_use_case = GetPosicion(posicion_repository=posicion_repository)
create_posicion_use_case = CreatePosicion(posicion_repository=posicion_repository)
update_posicion_use_case = UpdatePosicion(posicion_repository=posicion_repository)
delete_posicion_use_case = DeletePosicion(posicion_repository=posicion_repository)
cerrar_posicion_use_case = CerrarPosicion(posicion_repository=posicion_repository)
deshacer_cerrar_posicion_use_case = DeshacerCerrarPosicion(posicion_repository=posicion_repository)
list_dividendo_rango_use_case = ListDividendoRango(posicion_repository=posicion_repository)


def list_productos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_productos_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_producto(id_producto: int) -> Tuple[Any, int]:
    code = 200
    producto = get_producto_use_case.execute(apply_locale_int(id_producto))
    if producto:
        response = producto.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve el producto con id {} y no da la excepción de not found".format(id_producto))
        raise MessageError("No se ha podido obtener el producto con id: {}".format(id_producto), code)
    return response, code


def create_producto(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    producto = create_producto_use_case.execute(params)
    if producto:
        response = producto.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")),
                           code)
    return response, code


def update_producto(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    producto = update_producto_use_case.execute(params)
    if producto:
        response = producto.get_dto()

    else:
        code = 409
        logger.warning("Ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")),
                           code)
    return response, code


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
    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_datetime(params["fecha"])
    valor_participacion = create_valor_participacion_use_case.execute(params)
    if valor_participacion:
        response = valor_participacion.get_dto()
    else:
        logger.warning("Error al crear el valor participacón {}")
        raise MessageError("Error al crear el valor participación {}", code)
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


def list_dividendos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])
    elements = list_dividendos_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_dividendo(id_dividendo: int) -> Tuple[Any, int]:
    code = 200
    bolsa = get_dividendo_use_case.execute(apply_locale_int(id_dividendo))
    if bolsa:
        response = bolsa.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve el diviendo con id {} y no da la excepción de not found".format(id_dividendo))
        raise MessageError("No se ha podido obtener el diviendo con id: {}".format(id_dividendo), code)
    return response, code


def create_dividendo(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_date(params["fecha"])
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
    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_date(params["fecha"])
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
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])
    elements = list_dividendo_rango_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return response_elements, code


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

    if params.get("list_isin") is not None:
        params["list_isin"] = apply_locale_list(params["list_isin"])

    if params.get("list_id_broker") is not None:
        params["list_id_broker"] = apply_locale_list_int(params["list_id_broker"])
    if params.get("id_broker") is not None:
        params["id_broker"] = apply_locale_int(params["id_broker"])

    if params.get("extrangero") is not None:
        params["extrangero"] = apply_locale_bool(params["extrangero"])

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

    if params.get("valor") is not None:
        params["valor"] = apply_locale_float(params["valor"])
    if params.get("abierta") is not None:
        params["abierta"] = apply_locale_bool(params["abierta"])

    if params.get("dividendo_por_participacion") is not None:
        params["dividendo_por_participacion"] = apply_locale_float(params["dividendo_por_participacion"])
    if params.get("retencion_por_participacion") is not None:
        params["retencion_por_participacion"] = apply_locale_float(params["retencion_por_participacion"])
