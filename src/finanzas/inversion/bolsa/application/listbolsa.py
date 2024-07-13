from typing import List

from src.finanzas.inversion.bolsa.domain.bolsa import Bolsa
from src.finanzas.inversion.bolsa.domain.bolsarepository import BolsaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListBolsa(TransactionalUseCase):

    def __init__(self, bolsa_repository: BolsaRepository):
        super().__init__([bolsa_repository])
        self._bolsa_repository = bolsa_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[Bolsa]:

        criteria = Criteria(order=Order(OrderBy(params.get("order_property", "nombre")), OrderType(params.get("order_type", "asc"))),
                            filter=self._create_filters(params)
                            )
        bolsas = self._bolsa_repository.list(criteria)
        return bolsas

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "nombre" in params and params["nombre"]:
            nombre_filter = SimpleFilter(
                "nombre", WhereOperator.ILIKE, "%{}%".format(params["nombre"]))
            filter = combine_filters(filter, CompositeOperator.AND, nombre_filter)
        return filter
