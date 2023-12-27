from typing import List

from src.finanzas.domain.producto import Producto
from src.finanzas.domain.productorepository import ProductoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListProducto(TransactionalUseCase):

    def __init__(self, producto_repository: ProductoRepository):
        super().__init__([producto_repository])
        self._producto_repository = producto_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[Producto]:

        criteria = Criteria(order=Order(OrderBy(params.get("order_property", "nombre")), OrderType(params.get("order_type", "asc"))),
                            filter=self._create_filters(params)
                            )
        productos = self._producto_repository.list(criteria)
        return productos

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "nombre" in params and params["nombre"]:
            nombre_filter = SimpleFilter(
                "nombre", WhereOperator.ILIKE, "%{}%".format(params["nombre"]))
            filter = combine_filters(filter, CompositeOperator.AND, nombre_filter)
        if "isin" in params and params["isin"]:
            isin_filter = SimpleFilter(
                "isin", WhereOperator.ILIKE, "%{}%".format(params["isin"]))
            filter = combine_filters(filter, CompositeOperator.AND, isin_filter)
        return filter
