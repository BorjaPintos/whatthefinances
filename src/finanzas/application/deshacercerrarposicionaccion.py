from loguru import logger

from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeshacerCerrarPosicionAccion(TransactionalUseCase):

    def __init__(self, posicion_accion_repository: PosicionAccionRepository):
        super().__init__([posicion_accion_repository])
        self._posicion_accion_repository_repository = posicion_accion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> PosicionAccion:

        posicion_accion = self._posicion_accion_repository_repository.get(params["id"])
        posicion_accion.set_abierta(True)
        posicion_accion.set_fecha_venta(None)
        posicion_accion.set_comision_venta(0.0)

        updated = self._posicion_accion_repository_repository.update(posicion_accion)

        if updated:
            try:
                self._session.flush()
                return posicion_accion
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el deshacer-cierre de posicion", 500)
