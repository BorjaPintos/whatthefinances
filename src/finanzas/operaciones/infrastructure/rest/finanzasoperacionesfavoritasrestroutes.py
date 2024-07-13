from flask import request
from flask_login import login_required
from src.finanzas.operaciones.infrastructure.rest import finanzasoperacionesfavoritascontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_operaciones_favoritas():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None),
            "begin_cantidad": request.args.get('begin_cantidad', None),
            "end_cantidad": request.args.get('end_cantidad', None),
            "descripcion": request.args.get('descripcion', None),
            "id_monedero_cargo": request.args.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.args.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.args.get('id_monedero_abono', None),
            "id_cuenta_abono": request.args.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.args.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.args.get('id_categoria_ingreso', None),
            "list_id_categoria_gasto": request.args.get('list_id_categoria_gasto', None),
            "list_id_categoria_ingreso": request.args.get('list_id_categoria_ingreso', None)
        }
        return finanzasoperacionesfavoritascontroller.list_operaciones_favoritas(params)

    @app.route(rootpath + "/<id_operacion_favorita>", methods=['GET'])
    @login_required
    @serialize_response
    def get_operacion_favorita(id_operacion_favorita: int):
        return finanzasoperacionesfavoritascontroller.get_operacion_favorita(id_operacion_favorita)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_operacion_favorita():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "nombre": request.json.get('nombre', None),
            "cantidad": request.json.get('cantidad', None),
            "id_monedero_cargo": request.json.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.json.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.json.get('id_monedero_abono', None),
            "id_cuenta_abono": request.json.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.json.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.json.get('id_categoria_ingreso', None),
        }
        return finanzasoperacionesfavoritascontroller.create_operacion_favorita(params)

    @app.route(rootpath + "/<id_operacion_favorita>", methods=['POST'])
    @login_required
    @serialize_response
    def update_operacion_favorita(id_operacion_favorita: int):
        params = {
            "id": id_operacion_favorita,
            "descripcion": request.json.get('descripcion', None),
            "nombre": request.json.get('nombre', None),
            "cantidad": request.json.get('cantidad', None),
            "id_monedero_cargo": request.json.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.json.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.json.get('id_monedero_abono', None),
            "id_cuenta_abono": request.json.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.json.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.json.get('id_categoria_ingreso', None),
        }
        return finanzasoperacionesfavoritascontroller.update_operacion_favorita(params)

    @app.route(rootpath + "/<id_operacion_favorita>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_operacion_favorita(id_operacion_favorita: int):
        return finanzasoperacionesfavoritascontroller.delete_operacion_favorita(id_operacion_favorita)
