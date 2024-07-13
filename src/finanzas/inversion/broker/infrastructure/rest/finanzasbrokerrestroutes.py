from flask import request
from flask_login import login_required

from src.finanzas.inversion.broker.infrastructure.rest import finanzasbrokercontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_brokers():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None),
            "extranjero": request.args.get('extranjero', None)
        }
        return finanzasbrokercontroller.list_brokers(params)

    @app.route(rootpath + "/<id_broker>", methods=['GET'])
    @login_required
    @serialize_response
    def get_broker(id_broker: int):
        return finanzasbrokercontroller.get_broker(id_broker)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_broker():
        params = {
            "nombre": request.json.get('nombre'),
            "extranjero": request.json.get('extranjero')
        }
        return finanzasbrokercontroller.create_broker(params)

    @app.route(rootpath + "/<id_broker>", methods=['POST'])
    @login_required
    @serialize_response
    def update_broker(id_broker: int):
        params = {
            "id": id_broker,
            "nombre": request.json.get('nombre', None),
            "extranjero": request.json.get('extranjero', None)
        }
        return finanzasbrokercontroller.update_broker(params)

