from loguru import logger

from src.finanzas.inversion.producto.domain.plataformaproductoenum import PlataformaProductoEnum
from src.finanzas.inversion.producto.domain.producto import Producto
from src.finanzas.inversion.producto.domain.productorepository import ProductoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateProducto(TransactionalUseCase):

    def __init__(self, producto_repository: ProductoRepository):
        super().__init__([producto_repository])
        self._producto_repository = producto_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Producto:
        self.__validate_params(params)

        producto = self._producto_repository.get(params["id"])
        """El usuario puede cambiar todo"""
        producto.set_nombre(params.get("nombre"))
        producto.set_isin(params.get("isin"))
        producto.set_plataforma(PlataformaProductoEnum.get_enum_from_value(params.get("id_plataforma")))
        producto.set_url(params.get("url"))
        updated = self._producto_repository.update(producto)
        if updated:
            try:
                self._session.flush()
                return producto
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def __validate_params(self, params: dict):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id no puede estar vacío")
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre obligatorio")
        if "isin" not in params or params["isin"] is None:
            raise InvalidParamError("campo isin obligatorio")
