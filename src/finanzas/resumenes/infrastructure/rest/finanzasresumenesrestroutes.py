from flask import request
from flask_login import login_required

from src.finanzas.resumenes.infrastructure.rest import finanzasresumencontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath + "/ingresos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_ingresos():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_ingresos(params)

    @app.route(rootpath + "/gastos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_gastos():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_gastos(params)

    @app.route(rootpath + "/cuentas-ingreso", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_ingreso():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_cuentas(params)

    @app.route(rootpath + "/cuentas-gasto", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_gasto():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_cuentas(params)

    @app.route(rootpath + "/cuentas-total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_cuentas(params)

    @app.route(rootpath + "/monederos-ingreso", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_ingreso():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_monederos(params)

    @app.route(rootpath + "/monederos-gasto", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_gasto():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_monederos(params)

    @app.route(rootpath + "/monederos-total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_monederos(params)

    @app.route(rootpath + "/total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_total(params)

    @app.route(rootpath + "/total-ingresos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total_ingresos():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_total(params)

    @app.route(rootpath + "/total-gastos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total_gastos():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_total(params)

    @app.route(rootpath + "/valores_participaciones_meses", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_valores_participaciones_meses():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_valores_participaciones_meses(params)

    @app.route(rootpath + "/valores_participaciones_dias", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_valores_participaciones_dias():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_valores_participaciones_dias(params)


    @app.route(rootpath + "/posiciones_meses", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_posiciones_meses():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_posiciones_meses(params)

    @app.route(rootpath + "/posiciones_dias", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_posiciones_dias():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_posiciones_dias(params)


    @app.route(rootpath + "/posiciones_meses_acumuladas", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_posiciones_meses_acumuladas():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_posiciones_meses_acumulada(params)