from loguru import logger

from src.finanzas.inversion.bolsa.domain.bolsa import Bolsa
from src.finanzas.inversion.bolsa.domain.bolsarepository import BolsaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateBolsa(TransactionalUseCase):

    def __init__(self, bolsa_repository: BolsaRepository):
        super().__init__([bolsa_repository])
        self._bolsa_repository = bolsa_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Bolsa:
        self.__validate_params(params)

        bolsa = self._bolsa_repository.get(params["id"])
        """El usuario solo puede cambiar nombre"""
        bolsa.set_nombre(params.get("nombre"))
        updated = self._bolsa_repository.update(bolsa)
        if updated:
            try:
                self._session.flush()
                return bolsa
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def __validate_params(self, params: dict):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id no puede estar vacío")
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
