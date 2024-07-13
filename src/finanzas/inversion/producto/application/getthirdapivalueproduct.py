from datetime import datetime

from src.finanzas.inversion.producto.domain.plataformaproductoenum import PlataformaProductoEnum
from src.finanzas.inversion.producto.domain.producto import Producto
from src.finanzas.inversion.valorparticipacion.infrastructure.thirdapi.investingrepository import InvestingRepository
from src.finanzas.inversion.valorparticipacion.infrastructure.thirdapi.yahoofinancesrepository import YahooFinancesRepository


class GetThirdApiValueProduct:

    def __init__(self, config: dict):
        self._config = config
        self._switch_third = {
            PlataformaProductoEnum.Investing: InvestingRepository(config),
            PlataformaProductoEnum.Yahoo_Finances: YahooFinancesRepository(config),
        }

    def execute(self, product: Producto) -> (float, datetime):
        repo = self._switch_third.get(product.get_plataforma(), None)
        if repo is not None and product.get_url() is not None and product.get_url() != "":
            return repo.get_last_price(product.get_url())
        else:
            return None, None
