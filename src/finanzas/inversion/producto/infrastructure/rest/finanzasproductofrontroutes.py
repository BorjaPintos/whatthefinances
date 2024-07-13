from flask import request, render_template
from flask_login import login_required

from src.finanzas.inversion.producto.infrastructure.rest import finanzasproductocontroller


def import_routes(rootpath, app):
    @app.route(rootpath + "producto.html", methods=['GET'])
    @login_required
    def productos():
        user = request.user
        lista_headers = ["Nombre", "ISIN", "Plataforma", "URL"]
        lista_plataformas, code = finanzasproductocontroller.list_plataformas()
        return render_template('/producto.html', username=user.get_name(),
                               title="Productos",
                               lista_headers=lista_headers,
                               lista_plataformas=lista_plataformas)
