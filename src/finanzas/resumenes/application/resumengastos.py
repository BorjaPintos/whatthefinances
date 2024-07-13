from typing import List

from src.finanzas.resumenes.domain.resumengasto import ResumenGasto
from src.finanzas.resumenes.domain.resumenrepository import ResumenRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ResumenGastos(TransactionalUseCase):

    def __init__(self, resumen_repository: ResumenRepository):
        super().__init__([resumen_repository])
        self._resumen_repository = resumen_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[ResumenGasto]:
        criteria = Criteria(filter=self._create_filters(params))
        resumen_gastos = self._resumen_repository.gastos(criteria)
        return resumen_gastos

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = SimpleFilter("id_categoria_gasto", WhereOperator.NOTEQUAL, None)
        filter = combine_filters(filter, CompositeOperator.AND, SimpleFilter("id_categoria_ingreso", WhereOperator.IS, None))
        if "begin_fecha" in params and params["begin_fecha"]:
            fecha_filter = SimpleFilter(
                "begin_fecha", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha" in params and params["end_fecha"]:
            fecha_filter = SimpleFilter(
                "end_fecha", WhereOperator.LESSTHANOREQUAL, params["end_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)

        return filter
