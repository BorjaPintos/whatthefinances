from loguru import logger

from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdatePosicionAccion(TransactionalUseCase):

    def __init__(self, posicion_accion_repository: PosicionAccionRepository):
        super().__init__([posicion_accion_repository])
        self._posicion_accion_repository = posicion_accion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> PosicionAccion:
        self._validate_params(params)
        posicion_accion = self._posicion_accion_repository.get(params["id"])

        "El usuario puede cambiar todo salvo si es abierta o no, además en caso de ser posición cerrada también podrá modificar la comisión de venta"
        posicion_accion.set_fecha_compra(params.get("fecha_compra"))
        posicion_accion.set_nombre(params.get("nombre"))
        posicion_accion.set_isin(params.get("isin"))
        posicion_accion.set_id_bolsa(params.get("id_bolsa"))
        posicion_accion.set_id_broker(params.get("id_broker"))
        posicion_accion.set_numero_acciones(params.get("numero_acciones"))
        posicion_accion.set_precio_accion_sin_comision(params.get("precio_accion_sin_comision"))
        posicion_accion.set_comision_compra(params.get("comision_compra"))
        posicion_accion.set_otras_comisiones(params.get("otras_comisiones"))

        if not posicion_accion.is_abierta():
            if "comision_venta" not in params or params["comision_venta"] is None:
                raise InvalidParamError("campo comision_venta obligatorio")
            if "fecha_venta" not in params or params["fecha_venta"] is None:
                raise InvalidParamError("campo fecha_venta obligatorio")
            if "precio_venta_sin_comision" not in params or params["precio_venta_sin_comision"] is None:
                raise InvalidParamError("campo precio_venta_sin_comision obligatorio")

            posicion_accion.set_comision_venta(params.get("comision_venta"))
            posicion_accion.set_fecha_venta(params.get("fecha_venta"))
            posicion_accion.set_precio_venta_sin_comision(params.get("precio_venta_sin_comision"))

        updated = self._posicion_accion_repository.update(posicion_accion)
        if updated:
            try:
                self._session.flush()
                return posicion_accion
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def _validate_params(self, params):
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
        if "isin" not in params or params["isin"] is None:
            raise InvalidParamError("campo isin obligatorio")
        if "fecha_compra" not in params or params["fecha_compra"] is None:
            raise InvalidParamError("campo fecha_compra obligatorio")
        if "numero_acciones" not in params or params["numero_acciones"] is None:
            raise InvalidParamError("campo numero_acciones obligatorio")
        if "id_bolsa" not in params or params["id_bolsa"] is None:
            raise InvalidParamError("campo id_bolsa obligatorio")
        if "id_broker" not in params or params["id_broker"] is None:
            raise InvalidParamError("campo id_broker obligatorio")
        if "precio_accion_sin_comision" not in params or params["precio_accion_sin_comision"] is None:
            raise InvalidParamError("campo precio_accion_sin_comision obligatorio")
        if "comision_compra" not in params or params["comision_compra"] is None:
            raise InvalidParamError("campo comision_compra obligatorio")
        if "otras_comisiones" not in params or params["otras_comisiones"] is None:
            raise InvalidParamError("campo otras_comisiones obligatorio")
