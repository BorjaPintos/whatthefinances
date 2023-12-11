from flask import request
from flask_login import login_required
from src.finanzas.infrastructure.rest import finanzascontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath + "/cuenta", methods=['GET'])
    @login_required
    @serialize_response
    def list_cuentas():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        return finanzascontroller.list_cuentas(params)

    @app.route(rootpath + "/cuenta/<id_cuenta>", methods=['GET'])
    @login_required
    @serialize_response
    def get_cuenta(id_cuenta: int):
        return finanzascontroller.get_cuenta(id_cuenta)

    @app.route(rootpath + "/cuenta", methods=['POST'])
    @login_required
    @serialize_response
    def create_cuenta():
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_inicial": request.json.get('cantidad_inicial', 0.00),
            "ponderacion": request.json.get('ponderacion', 0.00),
        }
        return finanzascontroller.create_cuenta(params)

    @app.route(rootpath + "/cuenta/<id_cuenta>", methods=['POST'])
    @login_required
    @serialize_response
    def update_cuenta(id_cuenta: int):
        params = {
            "id": id_cuenta,
            "nombre": request.json.get('nombre', None),
            "cantidad_inicial": request.json.get('cantidad_inicial', None),
            "ponderacion": request.json.get('ponderacion', None),
        }
        return finanzascontroller.update_cuenta(params)

    @app.route(rootpath + "/monedero", methods=['GET'])
    @login_required
    @serialize_response
    def list_monederos():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        return finanzascontroller.list_monederos(params)

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['GET'])
    @login_required
    @serialize_response
    def get_monedero(id_monedero: int):
        return finanzascontroller.get_monedero(id_monedero)

    @app.route(rootpath + "/monedero", methods=['POST'])
    @login_required
    @serialize_response
    def create_monedero():
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_inicial": request.json.get('cantidad_inicial', 0.00)
        }
        return finanzascontroller.create_monedero(params)

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['POST'])
    @login_required
    @serialize_response
    def update_monedero(id_monedero: int):
        params = {
            "id": id_monedero,
            "nombre": request.json.get('nombre', None),
            "cantidad_inicial": request.json.get('cantidad_inicial', None)
        }
        return finanzascontroller.update_monedero(params)

    @app.route(rootpath + "/categoria_ingreso", methods=['GET'])
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
        return finanzascontroller.list_categorias_ingreso(params)

    @app.route(rootpath + "/categoria_ingreso/<id_categoria_ingreso>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_ingreso(id_categoria_ingreso: int):
        return finanzascontroller.get_categoria_ingreso(id_categoria_ingreso)

    @app.route(rootpath + "/categoria_ingreso", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_ingreso():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_abono_defecto": request.json.get('id_cuenta_abono_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascontroller.create_categoria_ingreso(params)

    @app.route(rootpath + "/categoria_ingreso/<id_categoria_ingreso>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_ingreso(id_categoria_ingreso: int):
        params = {
            "id": id_categoria_ingreso,
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_abono_defecto": request.json.get('id_cuenta_abono_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascontroller.update_categoria_ingreso(params)

    @app.route(rootpath + "/categoria_gasto", methods=['GET'])
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
        return finanzascontroller.list_categorias_gasto(params)

    @app.route(rootpath + "/categoria_gasto/<id_categoria_gasto>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_gasto(id_categoria_gasto: int):
        return finanzascontroller.get_categoria_gasto(id_categoria_gasto)

    @app.route(rootpath + "/categoria_gasto", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_gasto():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_cargo_defecto": request.json.get('id_cuenta_cargo_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascontroller.create_categoria_gasto(params)

    @app.route(rootpath + "/categoria_gasto/<id_categoria_gasto>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_gasto(id_categoria_gasto: int):
        params = {
            "id": id_categoria_gasto,
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_cargo_defecto": request.json.get('id_cuenta_cargo_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascontroller.update_categoria_gasto(params)

    @app.route(rootpath + "/operacion", methods=['GET'])
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
        }
        return finanzascontroller.list_operaciones(params)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['GET'])
    @login_required
    @serialize_response
    def get_operacion(id_operacion: int):
        return finanzascontroller.get_operacion(id_operacion)

    @app.route(rootpath + "/operacion", methods=['POST'])
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
        return finanzascontroller.create_operacion(params)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['POST'])
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
        return finanzascontroller.update_operacion(params)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_operacion(id_operacion: int):
        return finanzascontroller.delete_operacion(id_operacion)

    @app.route(rootpath + "/resumen/ingresos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_ingresos():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_ingresos(params)

    @app.route(rootpath + "/resumen/gastos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_gastos():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_gastos(params)

    @app.route(rootpath + "/resumen/cuentas-ingreso", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_ingreso():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_cuentas(params)

    @app.route(rootpath + "/resumen/cuentas-gasto", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_gasto():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_cuentas(params)

    @app.route(rootpath + "/resumen/cuentas-total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_cuentas(params)

    @app.route(rootpath + "/resumen/monederos-ingreso", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_ingreso():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_monederos(params)

    @app.route(rootpath + "/resumen/monederos-gasto", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_gasto():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_monederos(params)

    @app.route(rootpath + "/resumen/monederos-total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_monederos(params)


    @app.route(rootpath + "/resumen/total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_total(params)

    @app.route(rootpath + "/resumen/total-ingresos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total_ingresos():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_total(params)

    @app.route(rootpath + "/resumen/total-gastos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total_gastos():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzascontroller.resumen_total(params)