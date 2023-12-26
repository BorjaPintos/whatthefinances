from loguru import logger
from src.finanzas.domain.dividendorepository import DividendoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeleteDividendo(TransactionalUseCase):

    def __init__(self, dividendo_repository: DividendoRepository
                 ):
        super().__init__([dividendo_repository])
        self._dividendo_repository = dividendo_repository

    @transactional(readonly=False)
    def execute(self, id_dividendo: int) -> bool:

        deleted = self._dividendo_repository.delete(id_dividendo)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
