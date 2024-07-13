from flask import request
from flask_login import login_required

from src.finanzas.inversion.dividendos.infrastructure.rest import finanzasdividendoscontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath + "/rango", methods=['GET'])
    @login_required
    @serialize_response
    def list_dividendo_rango():
        params = {
            "order_property": request.args.get('order_property', 'isin'),
            "order_type": request.args.get('order_type', 'asc'),
            "isin": request.args.get('isin', None),
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None)
        }
        return finanzasdividendoscontroller.list_dividendo_rango(params)

    @app.route(rootpath, methods=['GET'])
    @login_required
    @serialize_response
    def list_dividendos():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "isin": request.args.get('isin', None),
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None)
        }
        return finanzasdividendoscontroller.list_dividendos(params)

    @app.route(rootpath + "/<id_dividendo>", methods=['GET'])
    @login_required
    @serialize_response
    def get_dividendo(id_dividendo: int):
        return finanzasdividendoscontroller.get_dividendo(id_dividendo)

    @app.route(rootpath, methods=['POST'])
    @login_required
    @serialize_response
    def create_dividendo():
        params = {
            "isin": request.json.get('isin'),
            "fecha": request.json.get('fecha'),
            "dividendo_por_participacion": request.json.get('dividendo_por_participacion'),
            "retencion_por_participacion": request.json.get('retencion_por_participacion')
        }
        return finanzasdividendoscontroller.create_dividendo(params)

    @app.route(rootpath + "/<id_dividendo>", methods=['POST'])
    @login_required
    @serialize_response
    def update_dividendo(id_dividendo: int):
        params = {
            "id": id_dividendo,
            "isin": request.json.get('isin', None),
            "fecha": request.json.get('fecha', None),
            "dividendo_por_participacion": request.json.get('dividendo_por_participacion', None),
            "retencion_por_participacion": request.json.get('retencion_por_participacion', None)
        }
        return finanzasdividendoscontroller.update_dividendo(params)

    @app.route(rootpath + "/<id_dividendo>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_dividendo(id_dividendo: int):
        return finanzasdividendoscontroller.delete_dividendo(id_dividendo)
