from typing import List

from src.finanzas.domain.categoriagasto import CategoriaGasto
from src.finanzas.domain.categoriagastorepository import CategoriaGastoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListCategoriasGasto(TransactionalUseCase):

    def __init__(self, categoria_gasto_repository: CategoriaGastoRepository):
        super().__init__([categoria_gasto_repository])
        self._categoria_gasto_repository = categoria_gasto_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[CategoriaGasto]:

        criteria = Criteria(order=Order(OrderBy(params["order_property"]), OrderType(params["order_type"])),
                            filter=self._create_filters(params)
                            )
        cuentas = self._categoria_gasto_repository.list(criteria)
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
        if "id_cuenta_cargo_defecto" in params and params["id_cuenta_cargo_defecto"]:
            cuenta_filter = SimpleFilter(
                "cuenta_cargo_defecto", WhereOperator.IS, params["id_cuenta_cargo_defecto"])
            filter = combine_filters(filter, CompositeOperator.AND, cuenta_filter)

        return filter
