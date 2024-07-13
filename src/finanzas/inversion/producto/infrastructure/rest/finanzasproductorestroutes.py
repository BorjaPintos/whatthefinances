from flask import request
from flask_login import login_required

from src.finanzas.inversion.producto.infrastructure.rest import finanzasproductocontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath + "/plataformas", methods=['GET'])
    @login_required
    @serialize_response
    def list_plataformas():
        return finanzasproductocontroller.list_plataformas()

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_productos():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None),
            "isin": request.args.get('isin', None)
        }
        return finanzasproductocontroller.list_productos(params)

    @app.route(rootpath + "/<id_producto>", methods=['GET'])
    @login_required
    @serialize_response
    def get_producto(id_producto: int):
        return finanzasproductocontroller.get_producto(id_producto)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_producto():
        params = {
            "nombre": request.json.get('nombre'),
            "isin": request.json.get('isin'),
            "id_plataforma": request.json.get('id_plataforma'),
            "url": request.json.get('url')
        }
        return finanzasproductocontroller.create_producto(params)

    @app.route(rootpath + "/<id_producto>", methods=['POST'])
    @login_required
    @serialize_response
    def update_producto(id_producto: int):
        params = {
            "id": id_producto,
            "nombre": request.json.get('nombre', None),
            "isin": request.json.get('isin', None),
            "id_plataforma": request.json.get('id_plataforma'),
            "url": request.json.get('url')
        }
        return finanzasproductocontroller.update_producto(params)
