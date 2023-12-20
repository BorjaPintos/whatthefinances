from loguru import logger

from src.finanzas.domain.valoraccionrepository import ValorAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeleteValorAccion(TransactionalUseCase):

    def __init__(self, valor_accion_repository: ValorAccionRepository):
        super().__init__([valor_accion_repository])
        self._valor_accion_repository = valor_accion_repository

    @transactional(readonly=False)
    def execute(self, id_valor_accion: int) -> bool:

        deleted = self._valor_accion_repository.delete(id_valor_accion)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
