from src.finanzas.inversion.posiciones.domain.posicion import Posicion
from src.finanzas.inversion.posiciones.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetPosicion(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository):
        super().__init__([posicion_repository])
        self._posicion_repository = posicion_repository

    @transactional(readonly=True)
    def execute(self, id_posicion: int) -> Posicion:
        posicion = self._posicion_repository.get(id_posicion)
        return posicion
