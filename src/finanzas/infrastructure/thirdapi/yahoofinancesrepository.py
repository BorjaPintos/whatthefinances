import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import json

from src.finanzas.domain.thirdapivalueproducts import ThirdApiValueProducts
from src.shared.utils.localeutils import apply_locale_float


class YahooFinancesRepository(ThirdApiValueProducts):

    @staticmethod
    def get_last_price(url: str) -> (float, datetime):
        value = None
        time = None
        try:
            pass
            # TODO
        except:
            traceback.print_exc()

        return value, time
