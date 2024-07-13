from src.finanzas.categorias.domain.categoriagasto import CategoriaGasto
from src.finanzas.categorias.domain.categoriagastorepository import CategoriaGastoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateCategoriaGasto(TransactionalUseCase):

    def __init__(self, categoria_gasto_repository: CategoriaGastoRepository):
        super().__init__([categoria_gasto_repository])
        self._categoria_gasto_repository = categoria_gasto_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> CategoriaGasto:
        if "descripcion" not in params or params["descripcion"] is None:
            raise InvalidParamError("campo descripción obligatorio")
        categoria_gasto = self._categoria_gasto_repository.new(params)
        return categoria_gasto
