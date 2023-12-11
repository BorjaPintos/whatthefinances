from typing import List

from src.finanzas.domain.resumencuenta import ResumenCuenta
from src.finanzas.domain.resumengasto import ResumenGasto
from src.finanzas.domain.resumenrepository import ResumenRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, Order, OrderBy, OrderType
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ResumenCuentas(TransactionalUseCase):

    def __init__(self, resumen_repository: ResumenRepository):
        super().__init__([resumen_repository])
        self._resumen_repository = resumen_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[ResumenCuenta]:
        criteria = Criteria(filter=self._create_filters(params))
        resumen_cuentas = (self._resumen_repository.cuentas(criteria))
        return resumen_cuentas

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "tipo" in params and params["tipo"]:
            if params["tipo"] == "ingresos":
                filter_tipo = SimpleFilter("cantidad", WhereOperator.GREATER, 0)
            elif params["tipo"] == "gastos":
                filter_tipo = SimpleFilter("cantidad", WhereOperator.LESS, 0)
            filter = combine_filters(filter, CompositeOperator.AND, filter_tipo)
        if "begin_fecha" in params and params["begin_fecha"]:
            fecha_filter = SimpleFilter(
                "begin_fecha", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha" in params and params["end_fecha"]:
            fecha_filter = SimpleFilter(
                "end_fecha", WhereOperator.LESSTHANOREQUAL, params["end_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)

        return filter
