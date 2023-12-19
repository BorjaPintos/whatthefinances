from src.finanzas.domain.broker import Broker
from src.finanzas.domain.brokerrepository import BrokerRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetBroker(TransactionalUseCase):

    def __init__(self, broker_repository: BrokerRepository):
        super().__init__([broker_repository])
        self._broker_repository = broker_repository

    @transactional(readonly=True)
    def execute(self, id_broker: int) -> Broker:
        broker = self._broker_repository.get(id_broker)
        return broker
