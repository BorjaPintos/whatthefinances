from typing import List

from src.finanzas.monederos.domain.monedero import Monedero
from src.finanzas.monederos.domain.monederorepository import MonederoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, Order, OrderBy, OrderType
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListMonederos(TransactionalUseCase):

    def __init__(self, monedero_repository: MonederoRepository):
        super().__init__([monedero_repository])
        self._monedero_repository = monedero_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[Monedero]:
        criteria = Criteria(order=Order(OrderBy(params.get("order_property", "nombre")), OrderType(params.get("order_type", "asc"))),
                            filter=self._create_filters(params)
                            )
        cuentas = self._monedero_repository.list(criteria)
        return cuentas

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "nombre" in params and params["nombre"]:
            nombre_filter = SimpleFilter(
                "nombre", WhereOperator.LIKE, "%{}%".format(params["nombre"]))
            filter = combine_filters(filter, CompositeOperator.AND, nombre_filter)

        return filter
