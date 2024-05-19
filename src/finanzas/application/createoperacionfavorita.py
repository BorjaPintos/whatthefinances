from src.finanzas.domain.operacionfavoritarepository import OperacionFavoritaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateOperacionFavorita(TransactionalUseCase):

    def __init__(self, operacion_favorita_repository: OperacionFavoritaRepository):
        super().__init__([operacion_favorita_repository])
        self._operacion_favorita_repository = operacion_favorita_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> bool:
        self._validate_params(params)
        self._operacion_favorita_repository.new(params)
        return True

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
