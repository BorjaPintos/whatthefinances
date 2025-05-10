import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time


class MyRequestsSelenium:

    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # Elimina si quieres ver el navegador
        options.add_argument("--disable-blink-features=AutomationControlled")

        self._driver = webdriver.Chrome(options=options)

    def get_json(self, url:str):
        try:
            self._driver.get(url)
            time.sleep(2)
            json_text = self._driver.find_element("tag name", "pre").text
            return json.loads(json_text)
        except:
            traceback.print_exc()
            return None