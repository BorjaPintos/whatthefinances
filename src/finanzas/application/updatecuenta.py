from loguru import logger
from src.finanzas.domain.cuenta import Cuenta
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class UpdateCuenta(TransactionalUseCase):

    def __init__(self, cuenta_repository: CuentaRepository):
        super().__init__([cuenta_repository])
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Cuenta:
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
        cuenta = self._cuenta_repository.update(params)
        try:
            self._session.flush()
            return cuenta
        except Exception as e:
            logger.info(e)
        return None


