from loguru import logger

from src.finanzas.domain.categoriagasto import CategoriaGasto
from src.finanzas.domain.categoriagastorepository import CategoriaGastoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateCategoriaGasto(TransactionalUseCase):

    def __init__(self, categoria_gasto_repository: CategoriaGastoRepository):
        super().__init__([categoria_gasto_repository])
        self._categoria_gasto_repository = categoria_gasto_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> CategoriaGasto:
        self.__validate_params(params)

        categoria_gasto = self._categoria_gasto_repository.get(params["id"])
        """El usuario solo puede cambiar, descripcion,  id_monedero_defecto e id_cuenta_cargo_defecto inicial"""
        categoria_gasto.set_descripcion(params.get("descripcion"))
        categoria_gasto.set_id_monedero_defecto(params.get("id_monedero_defecto"))
        categoria_gasto.set_id_cuenta_cargo_defecto(params.get("id_cuenta_cargo_defecto"))
        updated = self._categoria_gasto_repository.update(categoria_gasto)
        if updated:
            try:
                self._session.flush()
                return categoria_gasto
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def __validate_params(self, params: dict):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id no puede estar vacío")
        if "descripcion" not in params or params["descripcion"] is None:
            raise InvalidParamError("campo descripción obligatorio")
