import json
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

class MyRequestsSelenium:

    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")  # Versión moderna y más estable de headless
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
        "--log-level=3"
            )  # Silencia logs de Chrome (3 = Solo errores fatales)
        options.add_argument(
            "--disable-gcm-component"
        )  # Desactiva por completo el componente GCM que falla
        options.add_argument(f"--user-data-dir={tempfile.mkdtemp(prefix='chrome-profile-')}")

        # webdriver_manager descarga y gestiona el driver correcto según el SO de forma automática
        service = Service(ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=options)

    def get_json(self, url: str):
        try:
            self._driver.get(url)
            time.sleep(2)
            json_text = self._driver.find_element("tag name", "pre").text
            return json.loads(json_text)
        except Exception:
            traceback.print_exc()
            return None

    def close(self):
        """Buena práctica para cerrar el navegador al terminar"""
        if self._driver:
            self._driver.quit()
