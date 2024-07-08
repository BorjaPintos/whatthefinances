import traceback
from typing import List

from src.finanzas.application.createvalorparticipacion import CreateValorParticipacion
from src.finanzas.application.getthirdapivalueproduct import GetThirdApiValueProduct
from src.finanzas.domain.productorepository import ProductoRepository
from src.finanzas.domain.valorparticipacionrepository import ValorParticipacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.filtercomposite import CompositeOperator
from src.persistence.domain.filterutils import combine_filters
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class AutoCreateValorParticipacion(TransactionalUseCase):
    def __init__(self, producto_repository: ProductoRepository,
                 valor_participacion_repository: ValorParticipacionRepository,
                 third_api_value_product_use_case: GetThirdApiValueProduct):
        super().__init__([producto_repository])
        self._producto_repository = producto_repository
        self._create_use_case = CreateValorParticipacion(valor_participacion_repository)
        self._third_api_value_product_use_case = third_api_value_product_use_case

    @transactional(readonly=False)
    def execute(self, isin_list: List[str] = None) -> [dict]:
        filter = SimpleFilter("plataforma", WhereOperator.NOTEQUAL, 0)
        if isin_list:
            isin_filter = SimpleFilter("isin", WhereOperator.IN, isin_list)
            filter = combine_filters(filter, CompositeOperator.AND, isin_filter)

        criteria = Criteria(filter=filter)

        products = self._producto_repository.list(criteria)
        returned_list = []
        for product in products:
            try:
                value, time = self._third_api_value_product_use_case.execute(product)
                params = {
                    "fecha": time,
                    "isin": product.get_isin(),
                    "valor": value
                }
                self._create_use_case.execute(params)
                params["fecha"] = params["fecha"].strftime("%d/%m/%Y %H:%M:%S") if params["fecha"] is not None else ""
                returned_list.append(params)
            except:
                traceback.print_exc()
                "como es un proceso automático, no enviamos excepciones hacia arriba"
        return returned_list
