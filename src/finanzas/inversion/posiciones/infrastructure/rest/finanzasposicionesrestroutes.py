from flask import request
from flask_login import login_required

from src.finanzas.inversion.posiciones.infrastructure.rest import finanzasposicionescontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_posicion():
        params = {
            "order_property": request.args.get('order_property', 'fecha_compra'),
            "order_type": request.args.get('order_type', 'desc'),
            "count": request.args.get('count', 30),
            "offset": request.args.get('offset', 0),
            "nombre": request.args.get('nombre', None),
            "isin": request.args.get('isin', None),
            "id_bolsa": request.args.get('id_bolsa', None),
            "list_id_broker": request.args.get('list_id_broker', None),
            "id_broker": request.args.get('id_broker', None),
            "abierta": request.args.get('abierta', None),
            "begin_fecha_compra": request.args.get('begin_fecha_compra', None),
            "end_fecha_compra": request.args.get('end_fecha_compra', None),
            "begin_fecha_venta": request.args.get('begin_fecha_venta', None),
            "end_fecha_venta": request.args.get('end_fecha_venta', None),
            "begin_numero_participaciones": request.args.get('begin_numero_participaciones', None),
            "end_numero_participaciones": request.args.get('end_numero_participaciones', None),
            "begin_precio_compra_sin_comision": request.args.get('begin_precio_compra_sin_comision', None),
            "end_precio_compra_sin_comision": request.args.get('end_precio_compra_sin_comision', None),
            "begin_comision_compra": request.args.get('begin_comision_compra', None),
            "end_comision_compra": request.args.get('end_comision_compra', None),
            "begin_otras_comisiones": request.args.get('begin_otras_comisiones', None),
            "end_otras_comisiones": request.args.get('end_otras_comisiones', None),
        }
        return finanzasposicionescontroller.list_posiciones(params)

    @app.route(rootpath + "/<id_posicion>", methods=['GET'])
    @login_required
    @serialize_response
    def get_posicion(id_posicion: int):
        return finanzasposicionescontroller.get_posicion(id_posicion)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_posicion():
        params = {
            "nombre": request.json.get('nombre', None),
            "isin": request.json.get('isin', None),
            "id_bolsa": request.json.get('id_bolsa', None),
            "id_broker": request.json.get('id_broker', None),
            "fecha_compra": request.json.get('fecha_compra', None),
            "numero_participaciones": request.json.get('numero_participaciones', None),
            "precio_compra_sin_comision": request.json.get('precio_compra_sin_comision', None),
            "comision_compra": request.json.get('comision_compra', None),
            "otras_comisiones": request.json.get('otras_comisiones', None),
        }
        return finanzasposicionescontroller.create_posicion(params)

    @app.route(rootpath + "/<id_posicion>", methods=['POST'])
    @login_required
    @serialize_response
    def update_posicion(id_posicion: int):
        params = {
            "id": id_posicion,
            "nombre": request.json.get('nombre', None),
            "isin": request.json.get('isin', None),
            "id_bolsa": request.json.get('id_bolsa', None),
            "id_broker": request.json.get('id_broker', None),
            "fecha_compra": request.json.get('fecha_compra', None),
            "fecha_venta": request.json.get('fecha_venta', None),
            "numero_participaciones": request.json.get('numero_participaciones', None),
            "precio_compra_sin_comision": request.json.get('precio_compra_sin_comision', None),
            "precio_venta_sin_comision": request.json.get('precio_venta_sin_comision', None),
            "comision_compra": request.json.get('comision_compra', None),
            "otras_comisiones": request.json.get('otras_comisiones', None),
        }
        return finanzasposicionescontroller.update_posicion(params)

    @app.route(rootpath + "/cerrar/<id_posicion>", methods=['POST'])
    @login_required
    @serialize_response
    def cerrar_posicion(id_posicion: int):
        params = {
            "id": id_posicion,
            "fecha_venta": request.json.get('fecha_venta', None),
            "precio_venta_sin_comision": request.json.get('precio_venta_sin_comision', None)
        }
        return finanzasposicionescontroller.cerrar_posicion(params)

    @app.route(rootpath + "/deshacer-cerrar/<id_posicion>", methods=['POST'])
    @login_required
    @serialize_response
    def deshacer_cerrar_posicion(id_posicion: int):
        params = {
            "id": id_posicion,
        }
        return finanzasposicionescontroller.deshacer_cerrar_posicion(params)

    @app.route(rootpath + "/<id_posicion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_posicion(id_posicion: int):
        return finanzasposicionescontroller.delete_posicion(id_posicion)
