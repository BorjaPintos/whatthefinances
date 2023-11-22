from src.finanzas.domain.monedero import Monedero
from src.finanzas.domain.monederorepository import MonederoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetMonedero(TransactionalUseCase):

    def __init__(self, monedero_repository: MonederoRepository):
        super().__init__([monedero_repository])
        self._monedero_repository = monedero_repository

    @transactional(readonly=True)
    def execute(self, id_monedero: int) -> Monedero:
        monedero = self._monedero_repository.get(id_monedero)
        return monedero
