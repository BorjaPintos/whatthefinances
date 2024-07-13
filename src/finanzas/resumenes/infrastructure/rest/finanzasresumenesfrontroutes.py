from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):
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
