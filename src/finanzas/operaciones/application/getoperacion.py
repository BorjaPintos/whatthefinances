from src.finanzas.operaciones.domain.operacion import Operacion
from src.finanzas.operaciones.domain.operacionrepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetOperacion(TransactionalUseCase):

    def __init__(self, operacion_repository: OperacionRepository):
        super().__init__([operacion_repository])
        self._operacion_repository = operacion_repository

    @transactional(readonly=True)
    def execute(self, id_operacion: int) -> Operacion:
        operacion = self._operacion_repository.get(id_operacion)
        return operacion
