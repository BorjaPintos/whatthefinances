from src.finanzas.inversion.bolsa.domain.bolsa import Bolsa
from src.finanzas.inversion.bolsa.domain.bolsarepository import BolsaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetBolsa(TransactionalUseCase):

    def __init__(self, bolsa_repository: BolsaRepository):
        super().__init__([bolsa_repository])
        self._bolsa_repository = bolsa_repository

    @transactional(readonly=True)
    def execute(self, id_bolsa: int) -> Bolsa:
        bolsa = self._bolsa_repository.get(id_bolsa)
        return bolsa
