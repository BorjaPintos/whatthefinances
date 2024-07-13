from src.finanzas.cuentas.domain.cuenta import Cuenta
from src.finanzas.cuentas.domain.cuentarepository import CuentaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase

class GetCuenta(TransactionalUseCase):

    def __init__(self, cuenta_repository: CuentaRepository):
        super().__init__([cuenta_repository])
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=True)
    def execute(self, id_cuenta: int) -> Cuenta:
        cuenta = self._cuenta_repository.get(id_cuenta)
        return cuenta
