from datetime import datetime
from typing import List

from src.finanzas.resumenes.domain.resumenrepository import ResumenRepository
from src.finanzas.resumenes.domain.resumenvalorparticipacion import ResumenValorParticipacion
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ResumenValoresParticipacionesMeses(TransactionalUseCase):

    def __init__(self, resumen_repository: ResumenRepository):
        super().__init__([resumen_repository])
        self._resumen_repository = resumen_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[ResumenValorParticipacion]:
        criteria = Criteria(filter=self._create_filters(params))
        resumen_totales = (self._resumen_repository.resumen_valor_participacion_meses(criteria))
        return resumen_totales

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "begin_fecha" in params and params["begin_fecha"]:
            fecha_filter = SimpleFilter(
                "begin_fecha", WhereOperator.GREATERTHANOREQUAL, datetime.combine(params["begin_fecha"], datetime.min.time()))
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha" in params and params["end_fecha"]:
            fecha_filter = SimpleFilter(
                "end_fecha", WhereOperator.LESSTHANOREQUAL,
                datetime.combine(params["end_fecha"], datetime.max.time()))
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)

        return filter
