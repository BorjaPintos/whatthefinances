from src.finanzas.domain.categoriaingreso import CategoriaIngreso
from src.finanzas.domain.categoriaingresorepository import CategoriaIngresoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetCategoriaIngreso(TransactionalUseCase):

    def __init__(self, categoria_ingreso_repository: CategoriaIngresoRepository):
        super().__init__([categoria_ingreso_repository])
        self._categoria_ingreso_repository = categoria_ingreso_repository

    @transactional(readonly=True)
    def execute(self, id_categoria_ingreso: int) -> CategoriaIngreso:
        categoria_ingreso = self._categoria_ingreso_repository.get(id_categoria_ingreso)
        return categoria_ingreso
