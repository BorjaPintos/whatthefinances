import locale

from src.shared.infraestructure.rest.response import serialize_response

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
from flask import request, render_template
from flask_login import login_required
from src.finanzas.infrastructure.rest import finanzascontroller
import datetime


def import_routes(rootpath, app):
    @app.template_filter()
    def formato_decimal(value):
        return locale.str(value)

    @app.template_filter()
    def formato_fecha(value):
        date = datetime.datetime.fromtimestamp(value)
        return date.strftime("%Y-%m-%d")

    @app.route(rootpath + "resumen-general.html", methods=['GET'])
    @login_required
    def resumen_general():
        user = request.user
        return render_template('/resumen-general.html', username=user.get_name())

    @app.route(rootpath + "resumen-cuentas.html", methods=['GET'])
    @login_required
    def resumen_cuentas():
        user = request.user
        return render_template('/resumen-cuentas.html', username=user.get_name())

    @app.route(rootpath + "resumen-monederos.html", methods=['GET'])
    @login_required
    def resumen_monederos():
        user = request.user
        return render_template('/resumen-monederos.html', username=user.get_name())

    @app.route(rootpath + "resumen-categorias.html", methods=['GET'])
    @login_required
    def resumen_categorias():
        user = request.user
        return render_template('/resumen-categorias.html', username=user.get_name())

    @app.route(rootpath + "cuentas.html", methods=['GET'])
    @login_required
    def cuentas():
        user = request.user
        lista_headers = ["tipo_row", "Nombre", "Ponderación", "Capital Inicial", "Diferencia", "Total"]
        return render_template('/cuentas.html', username=user.get_name(),
                               title="Cuentas",
                               lista_headers=lista_headers)

    @app.route(rootpath + "monederos.html", methods=['GET'])
    @login_required
    def monederos():
        user = request.user
        lista_headers = ["tipo_row", "Nombre", "Capital Inicial", "Diferencia", "Total"]
        return render_template('/monederos.html', username=user.get_name(),
                               title="Monederos",
                               lista_headers=lista_headers)

    @app.route(rootpath + "categorias-ingreso.html", methods=['GET'])
    @login_required
    def categorias_ingreso():
        user = request.user
        lista_cuentas, code = finanzascontroller.list_cuentas({})
        lista_monederos, code = finanzascontroller.list_monederos({})
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
        lista_cuentas, code = finanzascontroller.list_cuentas({})
        lista_monederos, code = finanzascontroller.list_monederos({})
        lista_headers = ["Descripción", "Cuenta cargo por defecto", "Monedero cargo por defecto"]
        return render_template('/categorias_gasto.html', username=user.get_name(),
                               title="Categorias Gasto",
                               lista_headers=lista_headers,
                               lista_cuentas=lista_cuentas,
                               lista_monederos=lista_monederos)

    @app.route(rootpath + "operaciones.html", methods=['GET'])
    @login_required
    def operaciones():
        user = request.user
        lista_categorias_gasto, code = finanzascontroller.list_categorias_gasto({})
        lista_categorias_ingreso, code = finanzascontroller.list_categorias_ingreso({})
        lista_cuentas, code = finanzascontroller.list_cuentas({})
        lista_monederos, code = finanzascontroller.list_monederos({})
        lista_headers = ["Fecha", "Cantidad", "Descripcion",
                         "Categoría Gasto", "Categoría Ingreso",
                         "Cuenta Cargo", "Cuenta Abono",
                         "Monedero Cargo", "Monedero abono"]

        return render_template('/operaciones.html', username=user.get_name(),
                               title="Operaciones",
                               lista_headers=lista_headers,
                               lista_categorias_gasto=lista_categorias_gasto,
                               lista_categorias_ingreso=lista_categorias_ingreso,
                               lista_cuentas=lista_cuentas,
                               lista_monederos=lista_monederos,
                               )
