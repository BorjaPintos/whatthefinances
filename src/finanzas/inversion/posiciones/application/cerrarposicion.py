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

        if not posicion.is_abierta():
            raise InvalidParamError("La posición ya está cerrada")

        if posicion.get_id_broker() != 1:
            oldest_open = self._posicion_repository_repository.get_oldest_open_by_isin_and_broker(
                posicion.get_isin(), posicion.get_id_broker())
            if oldest_open is not None and oldest_open.get_id() != posicion.get_id():
                raise InvalidParamError(
                    "Solo se puede cerrar la posición abierta más antigua de cada elemento en el mismo broker. "
                    "La posición más antigua abierta para el ISIN {} en el mismo broker tiene fecha de compra {}".format(
                        posicion.get_isin(), oldest_open.get_fecha_compra().strftime("%d/%m/%Y")))

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
