from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetPosicionAccion(TransactionalUseCase):

    def __init__(self, posicion_accion_repository: PosicionAccionRepository):
        super().__init__([posicion_accion_repository])
        self._posicion_accion_repository = posicion_accion_repository

    @transactional(readonly=True)
    def execute(self, id_posicion_accion: int) -> PosicionAccion:
        posicion_accion = self._posicion_accion_repository.get(id_posicion_accion)
        return posicion_accion
