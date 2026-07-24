from typing import List, Tuple, Union, Any

from src.finanzas.cuentas.domain.movimientocuenta import MovimientoCuenta
from src.finanzas.cuentas.domain.movimientocuentarepository import MovimientoCuentaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, Order, OrderBy, OrderType
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListMovimientosCuenta(TransactionalUseCase):

    def __init__(self, movimiento_cuenta_repository: MovimientoCuentaRepository):
        super().__init__([movimiento_cuenta_repository])
        self._movimiento_cuenta_repository = movimiento_cuenta_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> Tuple[List[MovimientoCuenta], Union[bool, Any]]:
        criteria = Criteria(
            order=Order(
                OrderBy(params.get("order_property", "fecha")),
                OrderType(params.get("order_type", "desc"))
            ),
            filter=self._create_filters(params),
            offset=params.get("offset", 0),
            limit=params.get("count", 30)
        )
        return self._movimiento_cuenta_repository.list(criteria)

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None

        if "id_cuenta" in params and params["id_cuenta"]:
            cuenta_filter = SimpleFilter(
                "id_cuenta", WhereOperator.IS, params["id_cuenta"])
            filter = combine_filters(filter, CompositeOperator.AND, cuenta_filter)

        if "begin_fecha" in params and params["begin_fecha"]:
            fecha_filter = SimpleFilter(
                "begin_fecha", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)

        if "end_fecha" in params and params["end_fecha"]:
            fecha_filter = SimpleFilter(
                "end_fecha", WhereOperator.LESSTHANOREQUAL, params["end_fecha"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)

        if "id_categoria_gasto" in params and params["id_categoria_gasto"]:
            categoria_filter = SimpleFilter(
                "id_categoria_gasto", WhereOperator.IS, params["id_categoria_gasto"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)

        if "id_categoria_ingreso" in params and params["id_categoria_ingreso"]:
            categoria_filter = SimpleFilter(
                "id_categoria_ingreso", WhereOperator.IS, params["id_categoria_ingreso"])
            filter = combine_filters(filter, CompositeOperator.AND, categoria_filter)

        return filter
