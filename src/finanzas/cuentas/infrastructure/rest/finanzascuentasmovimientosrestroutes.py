from flask import request
from flask_login import login_required

from finanzas.cuentas.infrastructure.rest import finanzascuentascontroller
from src.finanzas.cuentas.infrastructure.rest import finanzascuentasmovimientoscontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_movimientos_cuenta():
        params = {
            "order_property": request.args.get('order_property', 'fecha'),
            "order_type": request.args.get('order_type', 'desc'),
            "count": request.args.get('count', 30),
            "offset": request.args.get('offset', 0),
            "id_cuenta": request.args.get('id_cuenta', None),
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
            "id_categoria_gasto": request.args.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.args.get('id_categoria_ingreso', None),
        }
        return finanzascuentasmovimientoscontroller.list_movimientos_cuenta(params)

    @app.route(rootpath + "/<id_cuenta>", methods=['GET'])
    @login_required
    @serialize_response
    def get_cuenta_for_movimientos(id_cuenta: int):
        return finanzascuentascontroller.get_cuenta(id_cuenta)
