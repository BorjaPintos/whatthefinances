from typing import List, Tuple, Union, Any

from src.finanzas.domain.isinnombre import IsinNombre
from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListUniquePosicionAccionIsin(TransactionalUseCase):

    def __init__(self, posicion_accion_repository: PosicionAccionRepository):
        super().__init__([posicion_accion_repository])
        self._posicion_accion_repository = posicion_accion_repository

    @transactional(readonly=True)
    def execute(self) -> List[str]:
        criteria = Criteria(
            order=Order(OrderBy("isin"), OrderType("asc")),
            filter=SimpleFilter("abierta", WhereOperator.EQUAL, True)
        )
        return self._posicion_accion_repository.list_unique_isin(criteria)
