from flask import request
from flask_login import login_required

from src.finanzas.cuentas.infrastructure.rest import finanzascuentascontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_cuentas():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        return finanzascuentascontroller.list_cuentas(params)

    @app.route(rootpath + "/<id_cuenta>", methods=['GET'])
    @login_required
    @serialize_response
    def get_cuenta(id_cuenta: int):
        return finanzascuentascontroller.get_cuenta(id_cuenta)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_cuenta():
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_inicial": request.json.get('cantidad_inicial', 0.00),
            "ponderacion": request.json.get('ponderacion', 0.00),
        }
        return finanzascuentascontroller.create_cuenta(params)

    @app.route(rootpath + "/<id_cuenta>", methods=['POST'])
    @login_required
    @serialize_response
    def update_cuenta(id_cuenta: int):
        params = {
            "id": id_cuenta,
            "nombre": request.json.get('nombre', None),
            "cantidad_inicial": request.json.get('cantidad_inicial', None),
            "ponderacion": request.json.get('ponderacion', None),
        }
        return finanzascuentascontroller.update_cuenta(params)
