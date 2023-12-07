import locale

from src.shared.infraestructure.rest.pagefront import PageFront
from src.shared.infraestructure.rest.response import serialize_response
from src.shared.utils.frontutils import calculate_pages_front

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

    @app.route(rootpath + "home.html", methods=['GET'])
    @login_required
    def home():
        user = request.user
        return render_template('/home.html', username=user.get_name())

    @app.route(rootpath + "cuentas.html", methods=['GET'])
    @login_required
    def cuentas():
        user = request.user
        lista_headers = ["Nombre", "Ponderación", "Capital Inicial", "Diferencia", "Total"]
        return render_template('/cuentas.html', username=user.get_name(),
                               title="Cuentas",
                               lista_headers=lista_headers)

    @app.route(rootpath + "monederos.html", methods=['GET'])
    @login_required
    def monederos():
        user = request.user
        lista_headers = ["Nombre", "Capital Inicial", "Diferencia", "Total"]
        return render_template('/monederos.html', username=user.get_name(),
                               title="Monederos",
                               lista_headers=lista_headers)

    @app.route(rootpath + "categorias-ingreso.html", methods=['GET'])
    @login_required
    def categorias_ingreso():
        user = request.user
        lista_cuentas, code = finanzascontroller.list_cuentas(request)
        lista_monederos, code = finanzascontroller.list_monederos(request)
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
        lista_cuentas, code = finanzascontroller.list_cuentas(request)
        lista_monederos, code = finanzascontroller.list_monederos(request)
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
        lista_categorias_gasto, code = finanzascontroller.list_categorias_gasto(request)
        lista_categorias_ingreso, code = finanzascontroller.list_categorias_ingreso(request)
        lista_cuentas, code = finanzascontroller.list_cuentas(request)
        lista_monederos, code = finanzascontroller.list_monederos(request)
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

    @app.route(rootpath + "/finanzas/front-operacion", methods=['GET'])
    @login_required
    @serialize_response
    def list_front_operaciones():
        operaciones_paginadas, code = finanzascontroller.list_operaciones(request)
        for element in operaciones_paginadas.get_elements():
            if element.get("id_categoria_ingreso") is not None and element.get("id_categoria_gasto") is not None:
                element["DT_RowClass"] = "transferencia"
            elif element.get("id_categoria_ingreso") is not None:
                element["DT_RowClass"] = "ingreso"
            else:
                element["DT_RowClass"] = "gasto"

        return operaciones_paginadas, code

    @app.route(rootpath + "operaciones2.html", methods=['GET'])
    @login_required
    def operaciones2():
        user = request.user
        lista_categorias_gasto, code = finanzascontroller.list_categorias_gasto(request)
        lista_categorias_ingreso, code = finanzascontroller.list_categorias_ingreso(request)
        lista_cuentas, code = finanzascontroller.list_cuentas(request)
        lista_monederos, code = finanzascontroller.list_monederos(request)
        lista_paginada_operaciones, code = finanzascontroller.list_operaciones(request)
        lista_headers = ["Fecha", "Cantidad", "Descripcion",
                         "Categoría Gasto", "Categoría Ingreso",
                         "Cuenta Cargo", "Cuenta Abono",
                         "Monedero Cargo", "Monedero abono"]

        offset = lista_paginada_operaciones.get_offset()
        pagination_size = lista_paginada_operaciones.get_pagination_size()
        total_elements = lista_paginada_operaciones.total_elements

        paginas = calculate_pages_front(offset, pagination_size, total_elements, 20)

        return render_template('/operaciones2.html', username=user.get_name(),
                               title="Operaciones",
                               lista_headers=lista_headers,
                               lista=lista_paginada_operaciones.get_elements(),
                               lista_categorias_gasto=lista_categorias_gasto,
                               lista_categorias_ingreso=lista_categorias_ingreso,
                               lista_cuentas=lista_cuentas,
                               lista_monederos=lista_monederos,
                               paginas=paginas
                               )
