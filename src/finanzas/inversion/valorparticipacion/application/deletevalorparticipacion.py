from loguru import logger

from src.finanzas.inversion.valorparticipacion.domain.valorparticipacionrepository import ValorParticipacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeleteValorParticipacion(TransactionalUseCase):

    def __init__(self, valor_participacion_repository: ValorParticipacionRepository):
        super().__init__([valor_participacion_repository])
        self._valor_participacion_repository = valor_participacion_repository

    @transactional(readonly=False)
    def execute(self, id_valor_participacion: int) -> bool:

        deleted = self._valor_participacion_repository.delete(id_valor_participacion)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
