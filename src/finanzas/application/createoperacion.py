from src.finanzas.domain.operacion import Operacion
from src.finanzas.domain.operacionrepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateOperacion(TransactionalUseCase):

    def __init__(self, operacion_repository: OperacionRepository):
        super().__init__([operacion_repository])
        self._operacion_repository = operacion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Operacion:

        self.__validate_params(params)
        operacion = self._operacion_repository.new(params)
        return operacion

    @staticmethod
    def __validate_params(params: dict):
        if "descripcion" not in params or params["descripcion"] is None:
            raise InvalidParamError("campo descripcion obligatorio")

        if "fecha" not in params or params["fecha"] is None:
            raise InvalidParamError("campo fecha obligatorio")

        if "cantidad" not in params or params["cantidad"] is None:
            raise InvalidParamError("campo cantidad obligatorio")

        if ("id_cuenta_cargo_defecto" not in params or params["id_cuenta_cargo_defecto"] is None) \
                and ("id_cuenta_abono" not in params or params["id_cuenta_abono"] is None):
            raise InvalidParamError("campo id_cuenta_cargo_defecto o id_cuenta_abono obligatorio (o ambos)")

        if ("id_monedero_cargo" not in params or params["id_monedero_cargo"] is None) \
                and ("id_monedero_abono" not in params or params["id_monedero_abono"] is None):
            raise InvalidParamError("campo id_monedero_cargo o id_monedero_abono obligatorio (o ambos)")

        if ("id_categoria_gasto" not in params or params["id_categoria_gasto"] is None) \
                and ("id_categoria_ingreso" not in params or params["id_categoria_ingreso"] is None):
            raise InvalidParamError("campo id_categoria_gasto o id_categoria_ingreso obligatorio (o ambos)")

        if ("id_categoria_gasto" not in params or params["id_categoria_gasto"] is None) \
                and ("id_categoria_ingreso" not in params or params["id_categoria_ingreso"] is None):
            raise InvalidParamError("campo id_categoria_gasto o id_categoria_ingreso obligatorio (o ambos)")

        gasto = []
        gasto.append(params.get("id_cuenta_cargo_defecto"))
        gasto.append(params.get("id_monedero_cargo"))
        gasto.append(params.get("id_categoria_gasto"))

        if any(gasto is None) and any(gasto is not None):
            raise InvalidParamError(
                "Se deben informar todos los campos de Gasto: id_cuenta_cargo_defecto, id_monedero_cargo, id_categoria_gasto")

        ingreso = []
        gasto.append(params.get("id_cuenta_abono"))
        gasto.append(params.get("id_monedero_abono"))
        gasto.append(params.get("id_categoria_ingreso"))

        if any(ingreso is None) and any(ingreso is not None):
            raise InvalidParamError(
                "Se deben informar todos los campos de Ingreso: id_cuenta_abono, id_monedero_abono, id_categoria_ingreso")
