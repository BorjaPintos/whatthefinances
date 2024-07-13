from flask import request
from flask_login import login_required


from src.finanzas.operaciones.infrastructure.rest import finanzasoperacionescontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_operaciones():
        params = {
            "order_property": request.args.get('order_property', 'fecha'),
            "order_type": request.args.get('order_type', 'desc'),
            "count": request.args.get('count', 30),
            "offset": request.args.get('offset', 0),
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
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
        return finanzasoperacionescontroller.list_operaciones(params)

    @app.route(rootpath + "/<id_operacion>", methods=['GET'])
    @login_required
    @serialize_response
    def get_operacion(id_operacion: int):
        return finanzasoperacionescontroller.get_operacion(id_operacion)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_operacion():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "fecha": request.json.get('fecha', None),
            "cantidad": request.json.get('cantidad', None),
            "id_monedero_cargo": request.json.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.json.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.json.get('id_monedero_abono', None),
            "id_cuenta_abono": request.json.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.json.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.json.get('id_categoria_ingreso', None),
        }
        return finanzasoperacionescontroller.create_operacion(params)

    @app.route(rootpath + "/<id_operacion>", methods=['POST'])
    @login_required
    @serialize_response
    def update_operacion(id_operacion: int):
        params = {
            "id": id_operacion,
            "descripcion": request.json.get('descripcion', None),
            "fecha": request.json.get('fecha', None),
            "cantidad": request.json.get('cantidad', None),
            "id_monedero_cargo": request.json.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.json.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.json.get('id_monedero_abono', None),
            "id_cuenta_abono": request.json.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.json.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.json.get('id_categoria_ingreso', None),
        }
        return finanzasoperacionescontroller.update_operacion(params)

    @app.route(rootpath + "/<id_operacion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_operacion(id_operacion: int):
        return finanzasoperacionescontroller.delete_operacion(id_operacion)
