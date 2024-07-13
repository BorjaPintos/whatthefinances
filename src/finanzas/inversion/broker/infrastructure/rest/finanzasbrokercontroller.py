from typing import Any, Tuple
from loguru import logger

from src.finanzas.inversion.broker.application.createbroker import CreateBroker
from src.finanzas.inversion.broker.application.getbroker import GetBroker
from src.finanzas.inversion.broker.application.listbroker import ListBroker
from src.finanzas.inversion.broker.application.updatebroker import UpdateBroker
from src.finanzas.inversion.broker.infrastructure.persistence.brokerrepositorysqlalchemy import \
    BrokerRepositorySQLAlchemy
from src.shared.infraestructure.rest.commoncastparams import common_cast_params
from src.shared.utils.localeutils import apply_locale_int, apply_locale_bool
from src.shared.domain.exceptions.messageerror import MessageError

broker_repository = BrokerRepositorySQLAlchemy()

list_brokers_use_case = ListBroker(broker_repository=broker_repository)
get_broker_use_case = GetBroker(broker_repository=broker_repository)
create_broker_use_case = CreateBroker(broker_repository=broker_repository)
update_broker_use_case = UpdateBroker(broker_repository=broker_repository)


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


def __cast_params(params: dict):
    common_cast_params(params)

    if params.get("extranjero") is not None:
        params["extranjero"] = apply_locale_bool(params["extranjero"])



