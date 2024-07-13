from src.finanzas.inversion.producto.infrastructure.rest import finanzasproductocontroller

from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):
    @app.route(rootpath + "valores_participaciones.html", methods=['GET'])
    @login_required
    def valores_participaciones():
        user = request.user
        lista_productos, code = finanzasproductocontroller.list_productos({})
        return render_template('/valores_participaciones.html', username=user.get_name(),
                               title="Valores de Participaciones",
                               lista_productos=lista_productos
                               )
