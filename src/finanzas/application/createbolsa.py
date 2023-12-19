from src.finanzas.domain.bolsa import Bolsa
from src.finanzas.domain.bolsarepository import BolsaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateBolsa(TransactionalUseCase):

    def __init__(self, bolsa_repository: BolsaRepository):
        super().__init__([bolsa_repository])
        self._bolsa_repository = bolsa_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Bolsa:
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
        bolsa = self._bolsa_repository.new(params)
        return bolsa
