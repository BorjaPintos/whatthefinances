from src.finanzas.domain.dividendo import Dividendo
from src.finanzas.domain.dividendorepository import DividendoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetDividendo(TransactionalUseCase):

    def __init__(self, dividendo_repository: DividendoRepository):
        super().__init__([dividendo_repository])
        self._dividendo_repository = dividendo_repository

    @transactional(readonly=True)
    def execute(self, id_dividendo: int) -> Dividendo:
        dividendo = self._dividendo_repository.get(id_dividendo)
        return dividendo
