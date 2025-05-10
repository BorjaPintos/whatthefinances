import re
import traceback
from datetime import datetime

from src.finanzas.inversion.producto.domain.thirdapivalueproducts import ThirdApiValueProducts
from src.shared.infraestructure.webscraping.myrequestsselenium import MyRequestsSelenium


class YahooFinancesRepository(ThirdApiValueProducts):
    query_last_price_url = "https://query1.finance.yahoo.com/v8/finance/chart/{}"
    simbol_re = re.compile("(?<=quote/).*(?=/)")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

    @staticmethod
    def get_last_price(url: str) -> (float, datetime):
        myrequests = MyRequestsSelenium()
        value = None
        time = None
        try:
            simbol_list = YahooFinancesRepository.simbol_re.findall(url)
            if simbol_list:
                simbol = simbol_list[0]
                chart = myrequests.get_json(YahooFinancesRepository.query_last_price_url.format(simbol))
                value = chart["chart"]["result"][0]["meta"]["regularMarketPrice"]
                time = datetime.fromtimestamp(chart["chart"]["result"][0]["meta"]["regularMarketTime"])
        except:
            traceback.print_exc()

        return value, time
