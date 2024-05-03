from loguru import logger

from src.finanzas.domain.posicion import Posicion
from src.finanzas.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdatePosicion(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository):
        super().__init__([posicion_repository])
        self._posicion_repository = posicion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Posicion:
        self._validate_params(params)
        posicion = self._posicion_repository.get(params["id"])

        "El usuario puede cambiar todo salvo si es abierta o no, además en caso de ser posición cerrada también podrá modificar la comisión de venta"
        posicion.set_fecha_compra(params.get("fecha_compra"))
        posicion.set_isin(params.get("isin"))
        posicion.set_id_bolsa(params.get("id_bolsa"))
        posicion.set_id_broker(params.get("id_broker"))
        posicion.set_numero_participaciones(params.get("numero_participaciones"))
        posicion.set_precio_compra_sin_comision(params.get("precio_compra_sin_comision"))
        posicion.set_comision_compra(params.get("comision_compra"))
        posicion.set_otras_comisiones(params.get("otras_comisiones"))

        if not posicion.is_abierta():
            if "comision_venta" not in params or params["comision_venta"] is None:
                raise InvalidParamError("campo comision_venta obligatorio")
            if "fecha_venta" not in params or params["fecha_venta"] is None:
                raise InvalidParamError("campo fecha_venta obligatorio")
            if "precio_venta_sin_comision" not in params or params["precio_venta_sin_comision"] is None:
                raise InvalidParamError("campo precio_venta_sin_comision obligatorio")

            posicion.set_comision_venta(params.get("comision_venta"))
            posicion.set_fecha_venta(params.get("fecha_venta"))
            posicion.set_precio_venta_sin_comision(params.get("precio_venta_sin_comision"))

        updated = self._posicion_repository.update(posicion)
        if updated:
            try:
                self._session.flush()
                return posicion
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def _validate_params(self, params):
        if "isin" not in params or params["isin"] is None:
            raise InvalidParamError("campo isin obligatorio")
        if "fecha_compra" not in params or params["fecha_compra"] is None:
            raise InvalidParamError("campo fecha_compra obligatorio")
        if "numero_participaciones" not in params or params["numero_participaciones"] is None:
            raise InvalidParamError("campo numero_participaciones obligatorio")
        if "id_bolsa" not in params or params["id_bolsa"] is None:
            raise InvalidParamError("campo id_bolsa obligatorio")
        if "id_broker" not in params or params["id_broker"] is None:
            raise InvalidParamError("campo id_broker obligatorio")
        if "precio_compra_sin_comision" not in params or params["precio_compra_sin_comision"] is None:
            raise InvalidParamError("campo precio_compra_sin_comision obligatorio")
        if "comision_compra" not in params or params["comision_compra"] is None:
            raise InvalidParamError("campo comision_compra obligatorio")
        if "otras_comisiones" not in params or params["otras_comisiones"] is None:
            raise InvalidParamError("campo otras_comisiones obligatorio")
