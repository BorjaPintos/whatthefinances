import locale
import traceback

from loguru import logger

try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except Exception:
    traceback.print_exc()
    logger.warning("No ha sido posible establecer el lenguaje local")
from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):

    @app.route(rootpath + "cuentas.html", methods=['GET'])
    @login_required
    def cuentas():
        user = request.user
        lista_headers = ["tipo_row", "Nombre", "Ponderación", "Capital Inicial", "Diferencia", "Total"]
        return render_template('/cuentas.html', username=user.get_name(),
                               title="Cuentas",
                               lista_headers=lista_headers)

