from flask import request
from flask_login import login_required

from src.finanzas.monederos.infrastructure.rest import finanzasmonederosmovimientoscontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_movimientos_monedero():
        params = {
            "order_property": request.args.get('order_property', 'fecha'),
            "order_type": request.args.get('order_type', 'desc'),
            "count": request.args.get('count', 30),
            "offset": request.args.get('offset', 0),
            "id_monedero": request.args.get('id_monedero', None),
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
            "id_categoria_gasto": request.args.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.args.get('id_categoria_ingreso', None),
        }
        return finanzasmonederosmovimientoscontroller.list_movimientos_monedero(params)

    @app.route(rootpath + "/<id_monedero>", methods=['GET'])
    @login_required
    @serialize_response
    def get_monedero_for_movimientos(id_monedero: int):
        return finanzasmonederosmovimientoscontroller.get_monedero_for_movimientos(id_monedero)
