from flask import render_template


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    def get_login_template():
        return render_template('/index.html')



