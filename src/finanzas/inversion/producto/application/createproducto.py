from src.finanzas.inversion.producto.domain.producto import Producto
from src.finanzas.inversion.producto.domain.productorepository import ProductoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateProducto(TransactionalUseCase):

    def __init__(self, producto_repository: ProductoRepository):
        super().__init__([producto_repository])
        self._producto_repository = producto_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Producto:
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
        if "isin" not in params or params["isin"] is None:
            raise InvalidParamError("campo isin obligatorio")
        producto = self._producto_repository.new(params)
        return producto
