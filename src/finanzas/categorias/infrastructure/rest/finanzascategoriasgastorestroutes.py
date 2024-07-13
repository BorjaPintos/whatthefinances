from flask import request
from flask_login import login_required

from src.finanzas.categorias.infrastructure.rest import finanzascategoriasgastocontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_categorias_gasto():
        params = {
            "order_property": request.args.get('order_property', 'descripcion'),
            "order_type": request.args.get('order_type', 'asc'),
            "descripcion": request.args.get('descripcion', None),
            "id_monedero_defecto": request.args.get('id_monedero_defecto', None),
            "id_cuenta_cargo_defecto": request.args.get('id_cuenta_cargo_defecto', None),
        }
        return finanzascategoriasgastocontroller.list_categorias_gasto(params)

    @app.route(rootpath + "/<id_categoria_gasto>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_gasto(id_categoria_gasto: int):
        return finanzascategoriasgastocontroller.get_categoria_gasto(id_categoria_gasto)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_gasto():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_cargo_defecto": request.json.get('id_cuenta_cargo_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascategoriasgastocontroller.create_categoria_gasto(params)

    @app.route(rootpath + "/<id_categoria_gasto>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_gasto(id_categoria_gasto: int):
        params = {
            "id": id_categoria_gasto,
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_cargo_defecto": request.json.get('id_cuenta_cargo_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascategoriasgastocontroller.update_categoria_gasto(params)
