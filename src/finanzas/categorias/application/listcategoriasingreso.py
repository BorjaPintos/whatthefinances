from typing import List

from src.finanzas.categorias.domain.categoriaingreso import CategoriaIngreso
from src.finanzas.categorias.domain.categoriaingresorepository import CategoriaIngresoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, Order, OrderBy, OrderType
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import WhereOperator, SimpleFilter


class ListCategoriasIngreso(TransactionalUseCase):

    def __init__(self, categoria_ingreso_repository: CategoriaIngresoRepository):
        super().__init__([categoria_ingreso_repository])
        self._categoria_ingreso_repository = categoria_ingreso_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[CategoriaIngreso]:
        criteria = Criteria(order=Order(OrderBy(params.get("order_property", "descripcion")), OrderType(params.get("order_type", "asc"))),
                            filter=self._create_filters(params)
                            )
        cuentas = self._categoria_ingreso_repository.list(criteria)
        return cuentas

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "descripcion" in params and params["descripcion"]:
            description_filter = SimpleFilter(
                "descripcion", WhereOperator.LIKE, "%{}%".format(params["descripcion"]))
            filter = combine_filters(filter, CompositeOperator.AND, description_filter)
        if "id_monedero_defecto" in params and params["id_monedero_defecto"]:
            monedero_filter = SimpleFilter(
                "monedero_defecto", WhereOperator.IS, params["id_monedero_defecto"])
            filter = combine_filters(filter, CompositeOperator.AND, monedero_filter)
        if "id_cuenta_abono_defecto" in params and params["id_cuenta_abono_defecto"]:
            cuenta_filter = SimpleFilter(
                "cuenta_abono_defecto", WhereOperator.IS, params["id_cuenta_abono_defecto"])
            filter = combine_filters(filter, CompositeOperator.AND, cuenta_filter)

        return filter
