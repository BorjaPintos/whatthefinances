from src.finanzas.categorias.domain.categoriaingreso import CategoriaIngreso
from src.finanzas.categorias.domain.categoriaingresorepository import CategoriaIngresoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateCategoriaIngreso(TransactionalUseCase):

    def __init__(self, categoria_ingreso_repository: CategoriaIngresoRepository):
        super().__init__([categoria_ingreso_repository])
        self._categoria_ingreso_repository = categoria_ingreso_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> CategoriaIngreso:
        if "descripcion" not in params or params["descripcion"] is None:
            raise InvalidParamError("campo descripción obligatorio")
        categoria_ingreso = self._categoria_ingreso_repository.new(params)
        return categoria_ingreso
