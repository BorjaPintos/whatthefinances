from loguru import logger
from src.finanzas.domain.operacionfavoritarepository import OperacionFavoritaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeleteOperacionFavorita(TransactionalUseCase):

    def __init__(self, operacion_favorita_repository: OperacionFavoritaRepository):
        super().__init__([operacion_favorita_repository])
        self._operacion_favorita_repository = operacion_favorita_repository

    @transactional(readonly=False)
    def execute(self, id_operacion_favorita: int) -> bool:

        deleted = self._operacion_favorita_repository.delete(id_operacion_favorita)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
