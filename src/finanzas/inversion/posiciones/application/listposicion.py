from typing import List, Tuple, Union, Any

from src.finanzas.inversion.posiciones.domain.posicion import Posicion
from src.finanzas.inversion.posiciones.domain.posicionrepository import PosicionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria, OrderType, Order, OrderBy
from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class ListPosicion(TransactionalUseCase):

    def __init__(self, posicion_repository: PosicionRepository):
        super().__init__([posicion_repository])
        self._posicion_repository = posicion_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> Tuple[List[Posicion], Union[bool, Any]]:

        criteria = Criteria(
            order=Order(OrderBy(params.get("order_property", "fecha_compra")),
                        OrderType(params.get("order_type", "asc"))),
            filter=self._create_filters(params),
            offset=params["offset"],
            limit=params["count"]
        )
        return self._posicion_repository.list(criteria)

    @staticmethod
    def _create_filters(params: dict) -> Filter:
        filter = None
        if "abierta" in params and params["abierta"]:
            abierta_filter = SimpleFilter(
                "abierta", WhereOperator.IS, params["abierta_filter"])
            filter = combine_filters(filter, CompositeOperator.AND, abierta_filter)
        if "nombre" in params and params["nombre"]:
            nombre_filter = SimpleFilter(
                "nombre", WhereOperator.ILIKE, "%{}%".format(params["nombre"]))
            filter = combine_filters(filter, CompositeOperator.AND, nombre_filter)
        if "isin" in params and params["isin"]:
            isin_filter = SimpleFilter(
                "isin", WhereOperator.ILIKE, "%{}%".format(params["isin"]))
            filter = combine_filters(filter, CompositeOperator.AND, isin_filter)
        if "list_isin" in params and params["isin"]:
            isin_filter = SimpleFilter(
                "isin", WhereOperator.IN, params["list_isin"])
            filter = combine_filters(filter, CompositeOperator.AND, isin_filter)
        if "list_id_broker" in params and params["list_id_broker"]:
            broker_filter = SimpleFilter(
                "id_broker", WhereOperator.IN, params["list_id_broker"])
            filter = combine_filters(filter, CompositeOperator.AND, broker_filter)
        if "id_broker" in params and params["id_broker"]:
            broker_filter = SimpleFilter(
                "id_broker", WhereOperator.IS, params["id_broker"])
            filter = combine_filters(filter, CompositeOperator.AND, broker_filter)
        if "id_bolsa" in params and params["id_bolsa"]:
            bolsa_filter = SimpleFilter(
                "id_bolsa", WhereOperator.IS, params["id_bolsa"])
            filter = combine_filters(filter, CompositeOperator.AND, bolsa_filter)
        if "begin_fecha_compra" in params and params["begin_fecha_compra"]:
            fecha_filter = SimpleFilter(
                "begin_fecha_compra", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha_compra"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha_compra" in params and params["end_fecha_compra"]:
            fecha_filter = SimpleFilter(
                "end_fecha_compra", WhereOperator.LESSTHANOREQUAL, params["end_fecha_compra"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "begin_fecha_venta" in params and params["begin_fecha_venta"]:
            fecha_filter = SimpleFilter(
                "begin_fecha_venta", WhereOperator.GREATERTHANOREQUAL, params["begin_fecha_venta"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "end_fecha_venta" in params and params["end_fecha_venta"]:
            fecha_filter = SimpleFilter(
                "end_fecha_venta", WhereOperator.LESSTHANOREQUAL, params["end_fecha_venta"])
            filter = combine_filters(filter, CompositeOperator.AND, fecha_filter)
        if "begin_precio_compra_sin_comision" in params and params["begin_precio_compra_sin_comision"]:
            begin_precio_compra_sin_comision_filter = SimpleFilter(
                "begin_precio_compra_sin_comision", WhereOperator.LESSTHANOREQUAL,
                params["begin_precio_compra_sin_comision"])
            filter = combine_filters(filter, CompositeOperator.AND, begin_precio_compra_sin_comision_filter)
        if "end_precio_compra_sin_comision" in params and params["end_precio_compra_sin_comision"]:
            end_precio_compra_sin_comision_filter = SimpleFilter(
                "end_precio_compra_sin_comision", WhereOperator.LESSTHANOREQUAL,
                params["end_precio_compra_sin_comision"])
            filter = combine_filters(filter, CompositeOperator.AND, end_precio_compra_sin_comision_filter)
        if "begin_comision_compra" in params and params["begin_comision_compra"]:
            begin_comision_compra_filter = SimpleFilter(
                "begin_comision_compra", WhereOperator.LESSTHANOREQUAL,
                params["begin_comision_compra"])
            filter = combine_filters(filter, CompositeOperator.AND, begin_comision_compra_filter)
        if "end_comision_compra" in params and params["end_comision_compra"]:
            end_comision_compra_filter = SimpleFilter(
                "end_comision_compra", WhereOperator.LESSTHANOREQUAL,
                params["end_comision_compra"])
            filter = combine_filters(filter, CompositeOperator.AND, end_comision_compra_filter)
        if "begin_comision_venta" in params and params["begin_comision_venta"]:
            begin_comision_venta_filter = SimpleFilter(
                "begin_comision_venta", WhereOperator.LESSTHANOREQUAL,
                params["begin_comision_venta"])
            filter = combine_filters(filter, CompositeOperator.AND, begin_comision_venta_filter)
        if "end_comision_venta" in params and params["end_comision_venta"]:
            end_comision_venta_filter = SimpleFilter(
                "end_comision_venta", WhereOperator.LESSTHANOREQUAL,
                params["end_comision_venta"])
            filter = combine_filters(filter, CompositeOperator.AND, end_comision_venta_filter)
        if "begin_otras_comisiones" in params and params["begin_otras_comisiones"]:
            begin_otras_comisiones_filter = SimpleFilter(
                "begin_otras_comisiones", WhereOperator.LESSTHANOREQUAL,
                params["begin_otras_comisiones"])
            filter = combine_filters(filter, CompositeOperator.AND, begin_otras_comisiones_filter)
        if "end_otras_comisiones" in params and params["end_otras_comisiones"]:
            end_otras_comisiones_filter = SimpleFilter(
                "end_otras_comisiones", WhereOperator.LESSTHANOREQUAL,
                params["end_otras_comisiones"])
            filter = combine_filters(filter, CompositeOperator.AND, end_otras_comisiones_filter)

        if "begin_numero_participaciones" in params and params["begin_numero_participaciones"]:
            begin_numero_participaciones_filter = SimpleFilter(
                "begin_numero_participaciones", WhereOperator.LESSTHANOREQUAL,
                params["begin_numero_participaciones"])
            filter = combine_filters(filter, CompositeOperator.AND, begin_numero_participaciones_filter)

        if "end_numero_participaciones" in params and params["end_numero_participaciones"]:
            end_numero_participaciones_filter = SimpleFilter(
                "end_numero_participaciones", WhereOperator.LESSTHANOREQUAL,
                params["end_numero_participaciones"])
            filter = combine_filters(filter, CompositeOperator.AND, end_numero_participaciones_filter)

        return filter
