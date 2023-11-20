from typing import List

from src.finanzas.domain.operacion import Operacion
from src.finanzas.domain.operacionresorepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListOperaciones(TransactionalUseCase):

    def __init__(self, operacion_repository: OperacionRepository):
        super().__init__([operacion_repository])
        self._operacion_repository = operacion_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[Operacion]:

        criteria = Criteria(order=Order(OrderBy(params["order_property"]), OrderType(params["order_type"])),
                            filter=self._create_filters(params)
                            )
        operaciones = self._operacion_repository.list(criteria)
        return operaciones

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "descripcion" in params and params["descripcion"]:
            description_filter = SimpleFilter(
                "descripcion", WhereOperator.LIKE, "%{}%".format(params["descripcion"]))
            filter = combine_filters(filter, CompositeOperator.AND, description_filter)
        if "id_monedero_cargo" in params and params["id_monedero_cargo"]:
            monedero_filter = SimpleFilter(
                "monedero_cargo", WhereOperator.IS, params["id_monedero_cargo"])
            filter = combine_filters(filter, CompositeOperator.AND, monedero_filter)
        if "id_monedero_abono" in params and params["id_monedero_abono"]:
            monedero_filter = SimpleFilter(
                "monedero_abono", WhereOperator.IS, params["id_monedero_abono"])
            filter = combine_filters(filter, CompositeOperator.AND, monedero_filter)
        if "id_cuenta_cargo" in params and params["id_cuenta_cargo"]:
            cuenta_filter = SimpleFilter(
                "cuenta_cargo", WhereOperator.IS, params["id_cuenta_cargo"])
            filter = combine_filters(filter, CompositeOperator.AND, cuenta_filter)
        if "id_cuenta_abono" in params and params["id_cuenta_abono"]:
            cuenta_filter = SimpleFilter(
                "cuenta_abono", WhereOperator.IS, params["id_cuenta_abono"])
            filter = combine_filters(filter, CompositeOperator.AND, cuenta_filter)
        if "id_categoria_ingreso" in params and params["id_categoria_ingreso"]:
            categoria_filter = SimpleFilter(
                "categoria_ingreso", WhereOperator.IS, params["id_categoria_ingreso"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)
        if "id_categoria_gasto" in params and params["id_categoria_gasto"]:
            categoria_filter = SimpleFilter(
                "categoria_gasto", WhereOperator.IS, params["id_categoria_gasto"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)
        if "begin_fecha" in params and params["begin_fecha"]:
            fecha_filter = SimpleFilter(
                "begin_fecha", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha" in params and params["end_fecha"]:
            fecha_filter = SimpleFilter(
                "end_fecha", WhereOperator.LESSTHANOREQUAL, params["end_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "begin_cantidad" in params and params["begin_cantidad"]:
            cantidad_filter = SimpleFilter(
                "begin_cantidad", WhereOperator.GREATERTHANOREQUAL, params["begin_cantidad"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_cantidad" in params and params["end_cantidad"]:
            cantidad_filter = SimpleFilter(
                "end_cantidad", WhereOperator.LESSTHANOREQUAL, params["end_cantidad"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)

        return filter
