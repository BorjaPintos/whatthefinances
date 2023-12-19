from typing import List

from src.finanzas.domain.broker import Broker
from src.finanzas.domain.brokerrepository import BrokerRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListBroker(TransactionalUseCase):

    def __init__(self, broker_repository: BrokerRepository):
        super().__init__([broker_repository])
        self._broker_repository = broker_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[Broker]:

        criteria = Criteria(order=Order(OrderBy(params.get("order_property", "nombre")), OrderType(params.get("order_type", "asc"))),
                            filter=self._create_filters(params)
                            )
        brokers = self._broker_repository.list(criteria)
        return brokers

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "nombre" in params and params["nombre"]:
            nombre_filter = SimpleFilter(
                "nombre", WhereOperator.ILIKE, "%{}%".format(params["nombre"]))
            filter = combine_filters(filter, CompositeOperator.AND, nombre_filter)
        return filter
