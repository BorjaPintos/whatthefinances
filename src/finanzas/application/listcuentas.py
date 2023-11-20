from typing import List

from src.finanzas.domain.cuenta import Cuenta
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, Order, OrderBy, OrderType
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import WhereOperator, SimpleFilter


class ListCuentas(TransactionalUseCase):

    def __init__(self, cuenta_repository: CuentaRepository):
        super().__init__([cuenta_repository])
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[Cuenta]:
        criteria = Criteria(order=Order(OrderBy(params["order_property"]), OrderType(params["order_type"])),
                            filter=self._create_filters(params)
                            )
        cuentas = self._cuenta_repository.list(criteria)
        return cuentas


    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "nombre" in params and params["nombre"]:
            nombre_filter = SimpleFilter(
                "nombre", WhereOperator.LIKE, "%{}%".format(params["nombre"]))
            filter = combine_filters(filter, CompositeOperator.AND, nombre_filter)

        return filter