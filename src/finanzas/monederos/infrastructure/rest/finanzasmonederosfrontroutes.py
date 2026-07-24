from flask import request, render_template
from flask_login import login_required

from finanzas.monederos.infrastructure.rest import finanzasmonederoscontroller
from shared.utils.localeutils import apply_locale_int


def import_routes(rootpath, app):
    @app.route(rootpath + "monederos.html", methods=['GET'])
    @login_required
    def monederos():
        user = request.user
        lista_headers = ["tipo_row", "Nombre", "Capital Inicial", "Diferencia", "Total"]
        return render_template('/monederos.html', username=user.get_name(),
                               title="Monederos",
                               lista_headers=lista_headers)

    @app.route(rootpath + "movimientos-monedero.html", methods=['GET'])
    @login_required
    def movimientos_monedero():
        user = request.user
        id_monedero = request.args.get('id_monedero', None)
        lista_headers = ["Fecha", "Descripcion", "Cantidad", "Saldo"]
        try:
            monedero, error = finanzasmonederoscontroller.get_monedero(apply_locale_int(id_monedero))
        except:
            monedero = {}
        return render_template('/movimientosmonedero.html', username=user.get_name(),
                               title=f"Movimientos Monedero: {monedero.get("nombre", "Desconocido")}",
                               lista_headers=lista_headers,
                               id_monedero=id_monedero)
