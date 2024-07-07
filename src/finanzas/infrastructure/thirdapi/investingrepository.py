import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import json

from src.finanzas.domain.thirdapivalueproducts import ThirdApiValueProducts
from src.shared.utils.localeutils import apply_locale_float


class InvestingRepository(ThirdApiValueProducts):

    @staticmethod
    def get_last_price(url: str) -> (float, datetime):
        value = None
        time = None
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features="lxml")
            if "funds" in url:
                # esta funciona distinto
                last = soup.find(id="last_last")
                value = apply_locale_float(last.text)
                classess = last.get("class")
                pidclass = classess[2].replace("last", "")
                time_text = soup.find_all("span", {"class": pidclass + "time"})[0].text
                now = datetime.now()
                time_without_year = datetime.strptime(time_text, "%d/%m")
                time = now.replace(month=time_without_year.month, day=time_without_year.day)
            else:
                script_element = soup.find(id="__NEXT_DATA__")
                data_json = json.loads(script_element.text)
                store = None
                if "etfs" in url:
                    store = 'etfStore'
                elif "equities" in url:
                    store = 'equityStore'
                elif "commodities" in url:
                    store = 'commodityStore'
                elif "rates-bonds" in url:
                    store = 'bondStore'
                elif "indices" in url:
                    store = 'indexStore'
                elif "currencies" in url:
                    store = 'currencyStore'
                elif "crypto" in url:
                    # esta no suele funcionar porque sale el captcha
                    store = 'currencyStore'
                if store:
                    value = float(data_json["props"]['pageProps']['state'][store]['instrument']['price']['last'])
                    time = datetime.fromtimestamp(
                        float(data_json["props"]['pageProps']['state'][store]['instrument']['price']['lastUpdateTime'][:-3]))
                    # el [:-3] es para quitarle los últimos 3 ceros
        except:
            traceback.print_exc()

        return value, time
