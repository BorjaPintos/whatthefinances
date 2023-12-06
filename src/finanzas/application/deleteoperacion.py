from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.operacion import Operacion
from src.finanzas.domain.operacionrepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class DeleteOperacion(TransactionalUseCase):

    def __init__(self, operacion_repository: OperacionRepository,
                 monedero_repository: MonederoRepository,
                 cuenta_repository: CuentaRepository):
        super().__init__([operacion_repository, monedero_repository, cuenta_repository])
        self._operacion_repository = operacion_repository
        self._monedero_repository = monedero_repository
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=True)
    def execute(self, id_operacion: int) -> bool:
        deleted = self._operacion_repository.delete(id_operacion)
        return deleted
