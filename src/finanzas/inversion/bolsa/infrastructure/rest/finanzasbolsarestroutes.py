from flask import request
from flask_login import login_required

from src.finanzas.inversion.bolsa.infrastructure.rest import finanzasbolsacontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_bolsas():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        return finanzasbolsacontroller.list_bolsas(params)

    @app.route(rootpath + "/<id_bolsa>", methods=['GET'])
    @login_required
    @serialize_response
    def get_bolsa(id_bolsa: int):
        return finanzasbolsacontroller.get_bolsa(id_bolsa)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_bolsa():
        params = {
            "nombre": request.json.get('nombre')
        }
        return finanzasbolsacontroller.create_bolsa(params)

    @app.route(rootpath + "/<id_bolsa>", methods=['POST'])
    @login_required
    @serialize_response
    def update_bolsa(id_bolsa: int):
        params = {
            "id": id_bolsa,
            "nombre": request.json.get('nombre', None)
        }
        return finanzasbolsacontroller.update_bolsa(params)
