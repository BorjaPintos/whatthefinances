from loguru import logger

from src.finanzas.monederos.domain.monederorepository import MonederoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class RestoreMonedero(TransactionalUseCase):

    def __init__(self, monedero_repository: MonederoRepository):
        super().__init__([monedero_repository])
        self._monedero_repository = monedero_repository

    @transactional(readonly=False)
    def execute(self, id_monedero: int) -> bool:
        if id_monedero is None:
            raise InvalidParamError("campo id no puede estar vacío")
        restored = self._monedero_repository.restore(id_monedero)
        if restored:
            try:
                self._session.flush()
                return restored
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la restauración", 500)
