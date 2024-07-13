from src.finanzas.categorias.infrastructure.rest import finanzascategoriasgastocontroller, \
    finanzascategoriasingresocontroller
from src.finanzas.monederos.infrastructure.rest import finanzasmonederoscontroller
from src.finanzas.cuentas.infrastructure.rest import finanzascuentascontroller

from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):

    @app.route(rootpath + "operaciones.html", methods=['GET'])
    @login_required
    def operaciones():
        user = request.user
        lista_categorias_gasto, code = finanzascategoriasgastocontroller.list_categorias_gasto({})
        lista_categorias_ingreso, code = finanzascategoriasingresocontroller.list_categorias_ingreso({})
        lista_cuentas, code = finanzascuentascontroller.list_cuentas({})
        lista_monederos, code = finanzasmonederoscontroller.list_monederos({})
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
                               lista_monederos=lista_monederos
                               )

    @app.route(rootpath + "operaciones_favoritas.html", methods=['GET'])
    @login_required
    def operaciones_favoritas():
        user = request.user
        lista_categorias_gasto, code = finanzascategoriasgastocontroller.list_categorias_gasto({})
        lista_categorias_ingreso, code = finanzascategoriasingresocontroller.list_categorias_ingreso({})
        lista_cuentas, code = finanzascuentascontroller.list_cuentas({})
        lista_monederos, code = finanzasmonederoscontroller.list_monederos({})
        lista_headers = ["Nombre", "Cantidad", "Descripcion",
                         "Categoría Gasto", "Categoría Ingreso",
                         "Cuenta Cargo", "Cuenta Abono",
                         "Monedero Cargo", "Monedero abono"]

        return render_template('/operaciones-favoritas.html', username=user.get_name(),
                               title="Operaciones Favoritas",
                               lista_headers=lista_headers,
                               lista_categorias_gasto=lista_categorias_gasto,
                               lista_categorias_ingreso=lista_categorias_ingreso,
                               lista_cuentas=lista_cuentas,
                               lista_monederos=lista_monederos,
                               )
