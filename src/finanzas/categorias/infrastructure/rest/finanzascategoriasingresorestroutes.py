from flask import request
from flask_login import login_required

from src.finanzas.categorias.infrastructure.rest import finanzascategoriasingresocontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_categorias_ingreso():
        params = {
            "order_property": request.args.get('order_property', 'descripcion'),
            "order_type": request.args.get('order_type', 'asc'),
            "descripcion": request.args.get('descripcion', None),
            "id_monedero_defecto": request.args.get('id_monedero_defecto', None),
            "id_cuenta_abono_defecto": request.args.get('id_cuenta_abono_defecto', None),
        }
        return finanzascategoriasingresocontroller.list_categorias_ingreso(params)

    @app.route(rootpath + "/<id_categoria_ingreso>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_ingreso(id_categoria_ingreso: int):
        return finanzascategoriasingresocontroller.get_categoria_ingreso(id_categoria_ingreso)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_ingreso():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_abono_defecto": request.json.get('id_cuenta_abono_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascategoriasingresocontroller.create_categoria_ingreso(params)

    @app.route(rootpath + "/<id_categoria_ingreso>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_ingreso(id_categoria_ingreso: int):
        params = {
            "id": id_categoria_ingreso,
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_abono_defecto": request.json.get('id_cuenta_abono_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascategoriasingresocontroller.update_categoria_ingreso(params)
