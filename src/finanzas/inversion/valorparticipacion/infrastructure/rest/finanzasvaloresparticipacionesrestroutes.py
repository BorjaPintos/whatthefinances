from flask import request
from flask_login import login_required

from src.finanzas.inversion.valorparticipacion.infrastructure.rest import finanzasvaloresparticipacionescontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath + "/auto", methods=['POST'])
    @login_required
    @serialize_response
    def auto_create_valor_participacion():
        return finanzasvaloresparticipacionescontroller.auto_create_valor_participacion()

    @app.route(rootpath + "/auto/<isin>", methods=['POST'])
    @login_required
    @serialize_response
    def auto_create_valor_participacion_with_isin(isin: str):
        result, code = finanzasvaloresparticipacionescontroller.auto_create_valor_participacion([isin])
        check = result and result[0].get("valor", None) is not None
        code = 200 if check else 404
        return {"check": check}, code

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_valor_participacion():
        params = {
            "order_property": request.args.get('order_property', 'fecha'),
            "order_type": request.args.get('order_type', 'desc'),
            "count": request.args.get('count', 30),
            "offset": request.args.get('offset', 0),
            "isin": request.args.get('isin', None),
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
            "begin_valor": request.args.get('begin_valor', None),
            "end_valor": request.args.get('end_valor', None),
        }
        return finanzasvaloresparticipacionescontroller.list_valores_participaciones(params)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_valor_participacion():
        params = {
            "isin": request.json.get('isin', None),
            "fecha_hora": request.json.get('fecha_hora', None),
            "valor": request.json.get('valor', None)
        }
        return finanzasvaloresparticipacionescontroller.create_valor_participacion(params)

    @app.route(rootpath + "/<id_valor_participacion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_valor_participacion(id_valor_participacion: int):
        return finanzasvaloresparticipacionescontroller.delete_valor_participacion(id_valor_participacion)
