from flask import request, render_template
from flask_login import login_required

from src.finanzas.cuentas.infrastructure.rest import finanzascuentascontroller
from src.finanzas.monederos.infrastructure.rest import finanzasmonederoscontroller


def import_routes(rootpath, app):


    @app.route(rootpath + "categorias-ingreso.html", methods=['GET'])
    @login_required
    def categorias_ingreso():
        user = request.user
        lista_cuentas, code = finanzascuentascontroller.list_cuentas({})
        lista_monederos, code = finanzasmonederoscontroller.list_monederos({})
        lista_headers = ["Descripción", "Cuenta abono por defecto", "Monedero abono por defecto"]
        return render_template('/categorias_ingreso.html', username=user.get_name(),
                               title="Categorias Ingreso",
                               lista_headers=lista_headers,
                               lista_cuentas=lista_cuentas,
                               lista_monederos=lista_monederos)

    @app.route(rootpath + "categorias-gasto.html", methods=['GET'])
    @login_required
    def categorias_gasto():
        user = request.user
        lista_cuentas, code = finanzascuentascontroller.list_cuentas({})
        lista_monederos, code = finanzasmonederoscontroller.list_monederos({})
        lista_headers = ["Descripción", "Cuenta cargo por defecto", "Monedero cargo por defecto"]
        return render_template('/categorias_gasto.html', username=user.get_name(),
                               title="Categorias Gasto",
                               lista_headers=lista_headers,
                               lista_cuentas=lista_cuentas,
                               lista_monederos=lista_monederos)
