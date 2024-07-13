from loguru import logger

from src.finanzas.categorias.domain.categoriaingreso import CategoriaIngreso
from src.finanzas.categorias.domain.categoriaingresorepository import CategoriaIngresoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateCategoriaIngreso(TransactionalUseCase):

    def __init__(self, categoria_ingreso_repository: CategoriaIngresoRepository):
        super().__init__([categoria_ingreso_repository])
        self._categoria_ingreso_repository = categoria_ingreso_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> CategoriaIngreso:
        self.__validate_params(params)
        categoria_ingreso = self._categoria_ingreso_repository.get(params["id"])
        """El usuario solo puede cambiar, descripcion,  id_monedero_defecto e id_cuenta_abono_defecto inicial"""
        categoria_ingreso.set_descripcion(params.get("descripcion"))
        categoria_ingreso.set_id_monedero_defecto(params.get("id_monedero_defecto"))
        categoria_ingreso.set_id_cuenta_abono_defecto(params.get("id_cuenta_abono_defecto"))
        updated = self._categoria_ingreso_repository.update(categoria_ingreso)
        if updated:
            try:
                self._session.flush()
                return categoria_ingreso
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def __validate_params(self, params: dict):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id no puede estar vacío")
        if "descripcion" not in params or params["descripcion"] is None:
            raise InvalidParamError("campo descripción obligatorio")
