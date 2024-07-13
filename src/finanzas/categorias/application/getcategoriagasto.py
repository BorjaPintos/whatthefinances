from src.finanzas.categorias.domain.categoriagasto import CategoriaGasto
from src.finanzas.categorias.domain.categoriagastorepository import CategoriaGastoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetCategoriaGasto(TransactionalUseCase):

    def __init__(self, categoria_gasto_repository: CategoriaGastoRepository):
        super().__init__([categoria_gasto_repository])
        self._categoria_gasto_repository = categoria_gasto_repository

    @transactional(readonly=True)
    def execute(self, id_categoria_gasto: int) -> CategoriaGasto:
        categoria_gasto = self._categoria_gasto_repository.get(id_categoria_gasto)
        return categoria_gasto
