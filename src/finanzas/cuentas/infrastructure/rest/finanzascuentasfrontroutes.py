import locale
import traceback

from loguru import logger

from finanzas.cuentas.domain.cuenta import Cuenta
from finanzas.cuentas.infrastructure.rest import finanzascuentascontroller
from shared.utils.localeutils import apply_locale_int

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

    @app.route(rootpath + "movimientos-cuenta.html", methods=['GET'])
    @login_required
    def movimientos_cuenta():
        user = request.user
        id_cuenta = request.args.get('id_cuenta', None)
        lista_headers = ["Fecha",  "Descripcion", "Cantidad","Saldo"]
        try:
            cuenta, error = finanzascuentascontroller.get_cuenta(apply_locale_int(id_cuenta))
        except:
            cuenta = {}
        return render_template('/movimientoscuenta.html', username=user.get_name(),
                               title=f"Movimientos Cuenta: {cuenta.get("nombre", "Desconocido")}",
                               lista_headers=lista_headers,
                               id_cuenta=id_cuenta)

