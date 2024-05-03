from loguru import logger

from src.finanzas.domain.posicion import Posicion
from src.finanzas.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeshacerCerrarPosicion(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository):
        super().__init__([posicion_repository])
        self._posicion_repository_repository = posicion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Posicion:

        posicion = self._posicion_repository_repository.get(params["id"])
        posicion.set_abierta(True)
        posicion.set_fecha_venta(None)
        posicion.set_comision_venta(0.0)

        updated = self._posicion_repository_repository.update(posicion)

        if updated:
            try:
                self._session.flush()
                return posicion
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el deshacer-cierre de posicion", 500)
