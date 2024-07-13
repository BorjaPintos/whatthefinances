from flask import request, render_template
from flask_login import login_required



def import_routes(rootpath, app):


    @app.route(rootpath + "broker.html", methods=['GET'])
    @login_required
    def brokers():
        user = request.user
        lista_headers = ["Nombre", "Extranjero"]
        return render_template('/broker.html', username=user.get_name(),
                               title="Brokers",
                               lista_headers=lista_headers)

