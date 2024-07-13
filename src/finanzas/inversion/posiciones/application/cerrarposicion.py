from loguru import logger

from src.finanzas.inversion.posiciones.domain.posicion import Posicion
from src.finanzas.inversion.posiciones.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class CerrarPosicion(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository):
        super().__init__([posicion_repository])
        self._posicion_repository_repository = posicion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Posicion:
        self._validate_params(params)
        posicion = self._posicion_repository_repository.get(params["id"])

        posicion.set_fecha_venta(params.get("fecha_venta"))
        posicion.set_abierta(False)
        posicion.set_comision_venta(params.get("comision_venta"))

        updated = self._posicion_repository_repository.update(posicion)

        if updated:
            try:
                self._session.flush()
                return posicion
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el cierre de posicion", 500)

    def _validate_params(self, params):
        if "fecha_venta" not in params or params["fecha_venta"] is None:
            raise InvalidParamError("campo fecha_venta obligatorio")
        if "comision_venta" not in params or params["comision_venta"] is None:
            raise InvalidParamError("campo comision_venta obligatorio")
