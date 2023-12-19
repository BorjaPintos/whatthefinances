from loguru import logger

from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class CerrarPosicionAccion(TransactionalUseCase):

    def __init__(self, posicion_accion_repository: PosicionAccionRepository):
        super().__init__([posicion_accion_repository])
        self._posicion_accion_repository_repository = posicion_accion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> PosicionAccion:
        self._validate_params(params)
        posicion_accion = self._posicion_accion_repository_repository.get(params["id"])

        posicion_accion.set_fecha_venta(params.get("fecha_venta"))
        posicion_accion.set_abierta(False)
        posicion_accion.set_comision_venta(params.get("comision_venta"))

        updated = self._posicion_accion_repository_repository.update(posicion_accion)

        if updated:
            try:
                self._session.flush()
                return posicion_accion
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el cierre de posicion", 500)

    def _validate_params(self, params):
        if "fecha_venta" not in params or params["fecha_venta"] is None:
            raise InvalidParamError("campo fecha_venta obligatorio")
        if "comision_venta" not in params or params["comision_venta"] is None:
            raise InvalidParamError("campo comision_venta obligatorio")
