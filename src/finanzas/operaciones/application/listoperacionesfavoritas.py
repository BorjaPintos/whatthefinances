from typing import List
from src.finanzas.operaciones.domain.operacionfavorita import OperacionFavorita
from src.finanzas.operaciones.domain.operacionfavoritarepository import OperacionFavoritaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListOperacionesFavoritas(TransactionalUseCase):

    def __init__(self, operacion_favorita_repository: OperacionFavoritaRepository):
        super().__init__([operacion_favorita_repository])
        self._operacion_favorita_repository = operacion_favorita_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[OperacionFavorita]:

        criteria = Criteria(
            order=Order(OrderBy(params.get("order_property", "nombre")), OrderType(params.get("order_type", "asc"))),
            filter=self._create_filters(params)
        )
        return self._operacion_favorita_repository.list(criteria)

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "nombre" in params and params["nombre"]:
            nombre_filter = SimpleFilter(
                "nombre", WhereOperator.ILIKE, "%{}%".format(params["nombre"]))
            filter = combine_filters(filter, CompositeOperator.AND, nombre_filter)
        if "descripcion" in params and params["descripcion"]:
            description_filter = SimpleFilter(
                "descripcion", WhereOperator.ILIKE, "%{}%".format(params["descripcion"]))
            filter = combine_filters(filter, CompositeOperator.AND, description_filter)
        if "id_monedero_cargo" in params and params["id_monedero_cargo"]:
            monedero_filter = SimpleFilter(
                "id_monedero_cargo", WhereOperator.IS, params["id_monedero_cargo"])
            filter = combine_filters(filter, CompositeOperator.AND, monedero_filter)
        if "id_monedero_abono" in params and params["id_monedero_abono"]:
            monedero_filter = SimpleFilter(
                "id_monedero_abono", WhereOperator.IS, params["id_monedero_abono"])
            filter = combine_filters(filter, CompositeOperator.AND, monedero_filter)
        if "id_cuenta_cargo" in params and params["id_cuenta_cargo"]:
            cuenta_filter = SimpleFilter(
                "id_cuenta_cargo", WhereOperator.IS, params["id_cuenta_cargo"])
            filter = combine_filters(filter, CompositeOperator.AND, cuenta_filter)
        if "id_cuenta_abono" in params and params["id_cuenta_abono"]:
            cuenta_filter = SimpleFilter(
                "id_cuenta_abono", WhereOperator.IS, params["id_cuenta_abono"])
            filter = combine_filters(filter, CompositeOperator.AND, cuenta_filter)
        if "id_categoria_ingreso" in params and params["id_categoria_ingreso"]:
            categoria_filter = SimpleFilter(
                "id_categoria_ingreso", WhereOperator.IS, params["id_categoria_ingreso"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)
        if "list_id_categoria_ingreso" in params and params["list_id_categoria_ingreso"]:
            categoria_filter = SimpleFilter(
                "id_categoria_ingreso", WhereOperator.IN, params["list_id_categoria_ingreso"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)
        if "id_categoria_gasto" in params and params["id_categoria_gasto"]:
            categoria_filter = SimpleFilter(
                "id_categoria_gasto", WhereOperator.IS, params["id_categoria_gasto"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)
        if "list_id_categoria_gasto" in params and params["list_id_categoria_gasto"]:
            categoria_filter = SimpleFilter(
                "id_categoria_gasto", WhereOperator.IN, params["list_id_categoria_gasto"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)
        if "begin_cantidad" in params and params["begin_cantidad"]:
            cantidad_filter = SimpleFilter(
                "begin_cantidad", WhereOperator.GREATERTHANOREQUAL, params["begin_cantidad"])
            filter = combine_filters(filter, CompositeOperator.AND, cantidad_filter)
        if "end_cantidad" in params and params["end_cantidad"]:
            cantidad_filter = SimpleFilter(
                "end_cantidad", WhereOperator.LESSTHANOREQUAL, params["end_cantidad"])
            filter = combine_filters(filter, CompositeOperator.AND, cantidad_filter)

        return filter
