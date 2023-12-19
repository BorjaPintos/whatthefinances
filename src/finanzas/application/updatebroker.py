from loguru import logger

from src.finanzas.domain.broker import Broker
from src.finanzas.domain.brokerrepository import BrokerRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateBroker(TransactionalUseCase):

    def __init__(self, broker_repository: BrokerRepository):
        super().__init__([broker_repository])
        self._broker_repository = broker_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Broker:
        self.__validate_params(params)

        broker = self._broker_repository.get(params["id"])
        """El usuario solo puede cambiar nombre"""
        broker.set_nombre(params.get("nombre"))
        updated = self._broker_repository.update(broker)
        if updated:
            try:
                self._session.flush()
                return broker
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def __validate_params(self, params: dict):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id no puede estar vacío")
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
