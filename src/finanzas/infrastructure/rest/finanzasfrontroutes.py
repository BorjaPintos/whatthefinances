from flask import request, render_template
from flask_login import login_required

from src.finanzas.infrastructure.rest import finanzascontroller


def import_routes(rootpath, app):

    @app.route(rootpath + "home.html", methods=['GET'])
    @login_required
    def home():
        user = request.user
        return render_template('/home.html', username=user.get_name())

    @app.route(rootpath + "cuentas.html", methods=['GET'])
    @login_required
    def cuentas():
        user = request.user
        lista_cuentas, code = finanzascontroller.list_cuentas(request)
        lista_headers = ["Nombre", "Total", "Ponderación"]
        return render_template('/cuentas.html', username=user.get_name(),
                               title="Cuentas",
                               lista_headers=lista_headers,
                               lista=lista_cuentas)

    @app.route(rootpath + "monederos.html", methods=['GET'])
    @login_required
    def monederos():
        user = request.user
        lista_monederos, code = finanzascontroller.list_monederos(request)
        lista_headers = ["Nombre", "Total"]
        return render_template('/monederos.html', username=user.get_name(),
                               title="Monederos",
                               lista_headers=lista_headers,
                               lista=lista_monederos)
