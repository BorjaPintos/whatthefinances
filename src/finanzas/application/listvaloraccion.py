from typing import List, Tuple, Union, Any

from src.finanzas.domain.valoraccion import ValorAccion
from src.finanzas.domain.valoraccionrepository import ValorAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListValorAccion(TransactionalUseCase):

    def __init__(self, valor_accion_repository: ValorAccionRepository):
        super().__init__([valor_accion_repository])
        self._valor_accion_repository = valor_accion_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> Tuple[List[ValorAccion], Union[bool, Any]]:

        criteria = Criteria(
            order=Order(OrderBy(params.get("order_property", "fecha")), OrderType(params.get("order_type", "desc"))),
            filter=self._create_filters(params),
            offset=params["offset"],
            limit=params["count"]
            )
        return self._valor_accion_repository.list(criteria)

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "isin" in params and params["isin"]:
            isin_filter = SimpleFilter(
                "isin", WhereOperator.IS, params["isin"])
            filter = combine_filters(filter, CompositeOperator.AND, isin_filter)
        if "begin_fecha" in params and params["begin_fecha"]:
            fecha_filter = SimpleFilter(
                "begin_fecha", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha" in params and params["end_fecha"]:
            fecha_filter = SimpleFilter(
                "end_fecha", WhereOperator.LESSTHANOREQUAL, params["end_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "begin_valor" in params and params["begin_valor"]:
            valor_filter = SimpleFilter(
                "begin_valor", WhereOperator.GREATERTHANOREQUAL, params["begin_valor"])
            filter = combine_filters(filter, CompositeOperator.AND, valor_filter)
        if "end_valor" in params and params["end_valor"]:
            valor_filter = SimpleFilter(
                "end_valor", WhereOperator.LESSTHANOREQUAL, params["end_valor"])
            filter = combine_filters(filter, CompositeOperator.AND, valor_filter)

        return filter
