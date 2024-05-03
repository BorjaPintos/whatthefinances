from typing import List, Tuple, Union, Any

from src.finanzas.domain.dividendo_rango import DividendoRango
from src.finanzas.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListDividendoRango(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository):
        super().__init__([posicion_repository])
        self._posicion_repository = posicion_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[DividendoRango]:

        criteria = Criteria(
            order=Order(OrderBy(params.get("order_property", "isin")),
                        OrderType(params.get("order_type", "asc"))),
            filter=self._create_filters(params)
        )
        return self._posicion_repository.dividendo_rango(criteria)

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "isin" in params and params["isin"]:
            isin_filter = SimpleFilter(
                "isin", WhereOperator.ILIKE, "%{}%".format(params["isin"]))
            filter = combine_filters(filter, CompositeOperator.AND, isin_filter)
        if "list_isin" in params and params["isin"]:
            isin_filter = SimpleFilter(
                "isin", WhereOperator.IN, params["list_isin"])
            filter = combine_filters(filter, CompositeOperator.AND, isin_filter)
        if "begin_fecha" in params and params["begin_fecha"]:
            fecha_filter = SimpleFilter(
                "begin_fecha", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha" in params and params["end_fecha"]:
            fecha_filter = SimpleFilter(
                "end_fecha", WhereOperator.LESSTHANOREQUAL, params["end_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        return filter
