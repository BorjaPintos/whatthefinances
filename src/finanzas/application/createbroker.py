from src.finanzas.domain.broker import Broker
from src.finanzas.domain.brokerrepository import BrokerRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateBroker(TransactionalUseCase):

    def __init__(self, broker_repository: BrokerRepository):
        super().__init__([broker_repository])
        self._broker_repository = broker_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Broker:
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
        if "extranjero" not in params or params["extranjero"] is None:
            raise InvalidParamError("campo extranjero obligatorio")
        broker = self._broker_repository.new(params)
        return broker
