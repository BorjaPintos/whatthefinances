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

    @app.route(rootpath + "/finanzas/front-operacion", methods=['GET'])
    @login_required
    @serialize_response
    def list_front_operaciones():

        identificador = request.args.get("draw")
        request_params = request.args

        order_property = "fecha"
        order_type = "desc"
        for key, value in request_params.items():
            if key.startswith("order[") and key.endswith("][column]"):
                order_property = request_params["columns[{}][data]".format(value)]
            if key.startswith("order[") and key.endswith("][dir]"):
                order_type = value


        params = {
            "order_property": order_property,
            "order_type": order_type,
            "count": request.args.get('length', 30),
            "offset": request.args.get('start', 0),

            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
            "begin_cantidad": request.args.get('begin_cantidad', None),
            "end_cantidad": request.args.get('end_cantidad', None),
            "descripcion": request.args.get('descripcion', None),
            "id_monedero_cargo": request.args.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.args.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.args.get('id_monedero_abono', None),
            "id_cuenta_abono": request.args.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.args.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.args.get('id_categoria_ingreso', None),
        }

        operaciones_paginadas, code = finanzascontroller.list_operaciones(params)

        elements = []
        for element in operaciones_paginadas.get_elements():
            if element.get("id_categoria_ingreso") is not None and element.get("id_categoria_gasto") is not None:
                element["DT_RowClass"] = "transferencia"
            elif element.get("id_categoria_ingreso") is not None:
                element["DT_RowClass"] = "ingreso"
            else:
                element["DT_RowClass"] = "gasto"
            elements.append(element)

        dataTables_page_object = {
            "recordsTotal": operaciones_paginadas.get_total_elements(),
            "recordsFiltered": operaciones_paginadas.get_total_elements(),
            "elements": elements,
            "draw": identificador
        }

        return dataTables_page_object, code
