from flask import request, render_template
from flask_login import login_required


def import_routes(rootpath, app):
    @app.route(rootpath + "hacienda.html", methods=['GET'])
    @login_required
    def hacienda():
        user = request.user
        title = "Hacienda Española"
        return render_template('/hacienda.html', username=user.get_name(),
                               title=title)
