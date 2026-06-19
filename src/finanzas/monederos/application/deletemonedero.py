from loguru import logger

from src.finanzas.monederos.domain.monederorepository import MonederoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class DeleteMonedero(TransactionalUseCase):

    def __init__(self, monedero_repository: MonederoRepository):
        super().__init__([monedero_repository])
        self._monedero_repository = monedero_repository

    @transactional(readonly=False)
    def execute(self, id_monedero: int) -> bool:
        if id_monedero is None:
            raise InvalidParamError("campo id no puede estar vacío")
        deleted = self._monedero_repository.delete(id_monedero)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
