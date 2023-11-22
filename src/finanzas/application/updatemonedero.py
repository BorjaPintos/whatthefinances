from loguru import logger
from src.finanzas.domain.monedero import Monedero
from src.finanzas.domain.monederorepository import MonederoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class UpdateMonedero(TransactionalUseCase):

    def __init__(self, monedero_repository: MonederoRepository):
        super().__init__([monedero_repository])
        self._monedero_repository = monedero_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Monedero:
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
        monedero = self._monedero_repository.update(params)
        try:
            self._session.flush()
            return monedero
        except Exception as e:
            logger.info(e)
        return None


