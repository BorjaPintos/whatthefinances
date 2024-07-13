from loguru import logger

from src.finanzas.inversion.posiciones.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeletePosicion(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository
                 ):
        super().__init__([posicion_repository])
        self._posicion_repository = posicion_repository

    @transactional(readonly=False)
    def execute(self, id_posicion: int) -> bool:

        deleted = self._posicion_repository.delete(id_posicion)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
