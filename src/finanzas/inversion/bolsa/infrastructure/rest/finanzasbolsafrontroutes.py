from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):
    @app.route(rootpath + "bolsa.html", methods=['GET'])
    @login_required
    def bolsas():
        user = request.user
        lista_headers = ["Nombre"]
        return render_template('/bolsa.html', username=user.get_name(),
                               title="Bolsas",
                               lista_headers=lista_headers)
