from src.finanzas.inversion.producto.domain.producto import Producto
from src.finanzas.inversion.producto.domain.productorepository import ProductoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetProducto(TransactionalUseCase):

    def __init__(self, producto_repository: ProductoRepository):
        super().__init__([producto_repository])
        self._producto_repository = producto_repository

    @transactional(readonly=True)
    def execute(self, id_producto: int) -> Producto:
        producto = self._producto_repository.get(id_producto)
        return producto
