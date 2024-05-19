from loguru import logger

from src.finanzas.domain.operacionFavorita import OperacionFavorita
from src.finanzas.domain.operacionfavoritarepository import OperacionFavoritaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateOperacionFavorita(TransactionalUseCase):

    def __init__(self, operacion_favorita_repository: OperacionFavoritaRepository):
        super().__init__([operacion_favorita_repository])
        self._operacion_favorita_repository = operacion_favorita_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> OperacionFavorita:
        self._validate_params(params)

        operacion_favorita = self._operacion_favorita_repository.get(params["id"])

        "El usuario puede cambiar todo"
        operacion_favorita.set_nombre(params.get("nombre"))
        operacion_favorita.set_descripcion(params.get("descripcion"))
        operacion_favorita.set_id_cuenta_abono(params.get("id_cuenta_abono"))
        operacion_favorita.set_id_monedero_abono(params.get("id_monedero_abono"))
        operacion_favorita.set_id_categoria_ingreso(params.get("id_categoria_ingreso"))
        operacion_favorita.set_id_cuenta_cargo(params.get("id_cuenta_cargo"))
        operacion_favorita.set_id_monedero_cargo(params.get("id_monedero_cargo"))
        operacion_favorita.set_id_categoria_gasto(params.get("id_categoria_gasto"))
        operacion_favorita.set_cantidad(params.get("cantidad"))

        updated = self._operacion_favorita_repository.update(operacion_favorita)

        if updated:
            try:
                self._session.flush()
                return operacion_favorita
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    @staticmethod
    def _validate_params(params: dict):
        if "descripcion" not in params or params["descripcion"] is None:
            raise InvalidParamError("campo descripcion obligatorio")

        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")

        if "cantidad" not in params or params["cantidad"] is None:
            raise InvalidParamError("campo cantidad obligatorio")
        elif params["cantidad"] <= 0:
            raise InvalidParamError(
                "Cantidad debe ser un número positivo (>0) (ya se ocupará la categoría de sumar o restar")

        if ("id_categoria_gasto" not in params or params["id_categoria_gasto"] is None) \
                and ("id_categoria_ingreso" not in params or params["id_categoria_ingreso"] is None):
            raise InvalidParamError("campo id_categoria_gasto o id_categoria_ingreso obligatorio (o ambos)")
