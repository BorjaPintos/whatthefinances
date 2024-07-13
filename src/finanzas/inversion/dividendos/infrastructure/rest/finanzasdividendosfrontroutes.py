from src.finanzas.inversion.producto.infrastructure.rest import finanzasproductocontroller

from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):

    @app.route(rootpath + "dividendos.html", methods=['GET'])
    @login_required
    def dividendos():
        user = request.user
        lista_productos, code = finanzasproductocontroller.list_productos({})
        lista_headers = ["Fecha", "Nombre", "Dividendo por Participación", "Retención por Participación"]
        return render_template('/dividendos.html', username=user.get_name(),
                               title="Dividendos",
                               lista_headers=lista_headers,
                               lista_productos=lista_productos
                               )