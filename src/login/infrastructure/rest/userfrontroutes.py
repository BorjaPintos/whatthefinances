from flask import render_template, request
from flask_login import login_required


def import_routes(rootpath, app):

    @app.route(rootpath + "change_password.html", methods=['GET'])
    @login_required
    def change_password_template():
        user = request.user
        return render_template('/change_password.html', username=user.get_name())

