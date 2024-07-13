from src.finanzas.inversion.posiciones.domain.posicion import Posicion
from src.finanzas.inversion.posiciones.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreatePosicion(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository):
        super().__init__([posicion_repository])
        self._posicion_repository = posicion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Posicion:
        self._validate_params(params)
        params["abierta"] = True
        params["comision_venta"] = 0.0
        params["fecha_venta"] = None
        params["precio_venta_sin_comision"] = None
        posicion = self._posicion_repository.new(params)
        return posicion

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
