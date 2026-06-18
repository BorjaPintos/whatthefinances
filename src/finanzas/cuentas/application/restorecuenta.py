from loguru import logger

from src.finanzas.cuentas.domain.cuentarepository import CuentaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class RestoreCuenta(TransactionalUseCase):

    def __init__(self, cuenta_repository: CuentaRepository):
        super().__init__([cuenta_repository])
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=False)
    def execute(self, id_cuenta: int) -> bool:
        if id_cuenta is None:
            raise InvalidParamError("campo id no puede estar vacío")
        restored = self._cuenta_repository.restore(id_cuenta)
        if restored:
            try:
                self._session.flush()
                return restored
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la restauración", 500)
