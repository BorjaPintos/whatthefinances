import locale
import traceback

from loguru import logger

try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except Exception:
    traceback.print_exc()
    logger.warning("No ha sido posible establecer el lenguaje local")
import datetime


def import_routes(rootpath, app):
    @app.template_filter()
    def formato_decimal(value):
        return locale.str(value)

    @app.template_filter()
    def formato_fecha(value):
        date = datetime.datetime.fromtimestamp(value)
        return date.strftime("%Y-%m-%d")
