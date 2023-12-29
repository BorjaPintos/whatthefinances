from flask import request
from flask_login import login_required
from src.login.infrastructure.rest import usercontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath + "/<id_user>", methods=['GET'])
    @login_required
    @serialize_response
    def get_user(id_user: int):
        return usercontroller.get_user(id_user)

    @app.route(rootpath + "/change_password", methods=['POST'])
    @login_required
    @serialize_response
    def change_password():
        params = {
            "id": request.user.get_id(),
            "password": request.json.get('password'),
            "new_password": request.json.get('new_password')
        }
        return usercontroller.change_password(params)
