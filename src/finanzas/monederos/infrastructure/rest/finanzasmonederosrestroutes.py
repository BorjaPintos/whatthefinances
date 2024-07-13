from flask import request
from flask_login import login_required

from src.finanzas.monederos.infrastructure.rest import finanzasmonederoscontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_monederos():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        return finanzasmonederoscontroller.list_monederos(params)

    @app.route(rootpath + "/<id_monedero>", methods=['GET'])
    @login_required
    @serialize_response
    def get_monedero(id_monedero: int):
        return finanzasmonederoscontroller.get_monedero(id_monedero)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_monedero():
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_inicial": request.json.get('cantidad_inicial', 0.00)
        }
        return finanzasmonederoscontroller.create_monedero(params)

    @app.route(rootpath + "/<id_monedero>", methods=['POST'])
    @login_required
    @serialize_response
    def update_monedero(id_monedero: int):
        params = {
            "id": id_monedero,
            "nombre": request.json.get('nombre', None),
            "cantidad_inicial": request.json.get('cantidad_inicial', None)
        }
        return finanzasmonederoscontroller.update_monedero(params)
