from flask import request
from flask_login import login_required

from src.finanzas.infrastructure.rest import finanzascuentascontroller, finanzasmonederoscontroller, \
    finanzascategoriasingresocontroller, finanzascategoriasgastocontroller, finanzasoperacionescontroller, \
    finanzasresumencontroller, finanzasposicionaccioncontroller
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
        return finanzascuentascontroller.list_cuentas(params)

    @app.route(rootpath + "/cuenta/<id_cuenta>", methods=['GET'])
    @login_required
    @serialize_response
    def get_cuenta(id_cuenta: int):
        return finanzascuentascontroller.get_cuenta(id_cuenta)

    @app.route(rootpath + "/cuenta", methods=['POST'])
    @login_required
    @serialize_response
    def create_cuenta():
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_inicial": request.json.get('cantidad_inicial', 0.00),
            "ponderacion": request.json.get('ponderacion', 0.00),
        }
        return finanzascuentascontroller.create_cuenta(params)

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
        return finanzascuentascontroller.update_cuenta(params)

    @app.route(rootpath + "/monedero", methods=['GET'])
    @login_required
    @serialize_response
    def list_monederos():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        return finanzasmonederoscontroller.list_monederos(params)

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['GET'])
    @login_required
    @serialize_response
    def get_monedero(id_monedero: int):
        return finanzasmonederoscontroller.get_monedero(id_monedero)

    @app.route(rootpath + "/monedero", methods=['POST'])
    @login_required
    @serialize_response
    def create_monedero():
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_inicial": request.json.get('cantidad_inicial', 0.00)
        }
        return finanzasmonederoscontroller.create_monedero(params)

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['POST'])
    @login_required
    @serialize_response
    def update_monedero(id_monedero: int):
        params = {
            "id": id_monedero,
            "nombre": request.json.get('nombre', None),
            "cantidad_inicial": request.json.get('cantidad_inicial', None)
        }
        return finanzasmonederoscontroller.update_monedero(params)

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
        return finanzascategoriasingresocontroller.list_categorias_ingreso(params)

    @app.route(rootpath + "/categoria_ingreso/<id_categoria_ingreso>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_ingreso(id_categoria_ingreso: int):
        return finanzascategoriasingresocontroller.get_categoria_ingreso(id_categoria_ingreso)

    @app.route(rootpath + "/categoria_ingreso", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_ingreso():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_abono_defecto": request.json.get('id_cuenta_abono_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascategoriasingresocontroller.create_categoria_ingreso(params)

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
        return finanzascategoriasingresocontroller.update_categoria_ingreso(params)

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
        return finanzascategoriasgastocontroller.list_categorias_gasto(params)

    @app.route(rootpath + "/categoria_gasto/<id_categoria_gasto>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_gasto(id_categoria_gasto: int):
        return finanzascategoriasgastocontroller.get_categoria_gasto(id_categoria_gasto)

    @app.route(rootpath + "/categoria_gasto", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_gasto():
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_cargo_defecto": request.json.get('id_cuenta_cargo_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        return finanzascategoriasgastocontroller.create_categoria_gasto(params)

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
        return finanzascategoriasgastocontroller.update_categoria_gasto(params)

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
        return finanzasoperacionescontroller.list_operaciones(params)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['GET'])
    @login_required
    @serialize_response
    def get_operacion(id_operacion: int):
        return finanzasoperacionescontroller.get_operacion(id_operacion)

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
        return finanzasoperacionescontroller.create_operacion(params)

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
        return finanzasoperacionescontroller.update_operacion(params)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_operacion(id_operacion: int):
        return finanzasoperacionescontroller.delete_operacion(id_operacion)

    @app.route(rootpath + "/broker", methods=['GET'])
    @login_required
    @serialize_response
    def list_brokers():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None),
            "extrangero": request.args.get('extrangero', None)
        }
        return finanzasposicionaccioncontroller.list_brokers(params)

    @app.route(rootpath + "/broker/<id_broker>", methods=['GET'])
    @login_required
    @serialize_response
    def get_broker(id_broker: int):
        return finanzasposicionaccioncontroller.get_broker(id_broker)

    @app.route(rootpath + "/broker", methods=['POST'])
    @login_required
    @serialize_response
    def create_broker():
        params = {
            "nombre": request.json.get('nombre'),
            "extrangero": request.json.get('extrangero')
        }
        return finanzasposicionaccioncontroller.create_broker(params)

    @app.route(rootpath + "/broker/<id_broker>", methods=['POST'])
    @login_required
    @serialize_response
    def update_broker(id_broker: int):
        params = {
            "id": id_broker,
            "nombre": request.json.get('nombre', None),
            "extrangero": request.json.get('extrangero', None)
        }
        return finanzasposicionaccioncontroller.update_broker(params)

    @app.route(rootpath + "/bolsa", methods=['GET'])
    @login_required
    @serialize_response
    def list_bolsas():
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        return finanzasposicionaccioncontroller.list_bolsas(params)

    @app.route(rootpath + "/bolsa/<id_bolsa>", methods=['GET'])
    @login_required
    @serialize_response
    def get_bolsa(id_bolsa: int):
        return finanzasposicionaccioncontroller.get_bolsa(id_bolsa)

    @app.route(rootpath + "/bolsa", methods=['POST'])
    @login_required
    @serialize_response
    def create_bolsa():
        params = {
            "nombre": request.json.get('nombre')
        }
        return finanzasposicionaccioncontroller.create_bolsa(params)

    @app.route(rootpath + "/bolsa/<id_bolsa>", methods=['POST'])
    @login_required
    @serialize_response
    def update_bolsa(id_bolsa: int):
        params = {
            "id": id_bolsa,
            "nombre": request.json.get('nombre', None)
        }
        return finanzasposicionaccioncontroller.update_bolsa(params)

    @app.route(rootpath + "/valoraccion", methods=['GET'])
    @login_required
    @serialize_response
    def list_valor_accion():
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
        return finanzasposicionaccioncontroller.list_valores_acciones(params)

    @app.route(rootpath + "/valoraccion", methods=['POST'])
    @login_required
    @serialize_response
    def create_valor_accion():
        params = {
            "isin": request.json.get('isin', None),
            "fecha": request.json.get('fecha', None),
            "valor": request.json.get('valor', None)
        }
        return finanzasposicionaccioncontroller.create_valor_accion(params)

    @app.route(rootpath + "/valoraccion/<id_valor_accion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_valor_accion(id_valor_accion: int):
        return finanzasposicionaccioncontroller.delete_valor_accion(id_valor_accion)

    @app.route(rootpath + "/posicionaccion", methods=['GET'])
    @login_required
    @serialize_response
    def list_posicion_accion():
        params = {
            "order_property": request.args.get('order_property', 'fecha'),
            "order_type": request.args.get('order_type', 'desc'),
            "count": request.args.get('count', 30),
            "offset": request.args.get('offset', 0),
            "nombre": request.args.get('nombre', None),
            "isin": request.args.get('isin', None),
            "id_bolsa": request.args.get('id_bolsa', None),
            "id_broker": request.args.get('id_broker', None),
            "begin_fecha_compra": request.args.get('begin_fecha_compra', None),
            "end_fecha_compra": request.args.get('end_fecha_compra', None),
            "begin_fecha_venta": request.args.get('begin_fecha_venta', None),
            "end_fecha_venta": request.args.get('end_fecha_venta', None),
            "begin_numero_acciones": request.args.get('begin_numero_acciones', None),
            "end_numero_acciones": request.args.get('end_numero_acciones', None),
            "begin_precio_accion_sin_comision": request.args.get('begin_precio_accion_sin_comision', None),
            "end_precio_accion_sin_comision": request.args.get('end_precio_accion_sin_comision', None),
            "begin_comision_compra": request.args.get('begin_comision_compra', None),
            "end_comision_compra": request.args.get('end_comision_compra', None),
            "begin_otras_comisiones": request.args.get('begin_otras_comisiones', None),
            "end_otras_comisiones": request.args.get('end_otras_comisiones', None),
        }
        return finanzasposicionaccioncontroller.list_posiciones_acciones(params)

    @app.route(rootpath + "/posicionaccion/<id_posicion_accion>", methods=['GET'])
    @login_required
    @serialize_response
    def get_posicion_accion(id_posicion_accion: int):
        return finanzasposicionaccioncontroller.get_posicion_accion(id_posicion_accion)

    @app.route(rootpath + "/posicionaccion", methods=['POST'])
    @login_required
    @serialize_response
    def create_posicion_accion():
        params = {
            "nombre": request.json.get('nombre', None),
            "isin": request.json.get('isin', None),
            "id_bolsa": request.json.get('id_bolsa', None),
            "id_broker": request.json.get('id_broker', None),
            "fecha_compra": request.json.get('fecha_compra', None),
            "numero_acciones": request.json.get('numero_acciones', None),
            "precio_accion_sin_comision": request.json.get('precio_accion_sin_comision', None),
            "comision_compra": request.json.get('comision_compra', None),
            "otras_comisiones": request.json.get('otras_comisiones', None),
        }
        return finanzasposicionaccioncontroller.create_posicion_accion(params)

    @app.route(rootpath + "/posicionaccion/<id_posicion_accion>", methods=['POST'])
    @login_required
    @serialize_response
    def update_posicion_accion(id_posicion_accion: int):
        params = {
            "id": id_posicion_accion,
            "nombre": request.json.get('nombre', None),
            "isin": request.json.get('isin', None),
            "id_bolsa": request.json.get('id_bolsa', None),
            "id_broker": request.json.get('id_broker', None),
            "fecha_compra": request.json.get('fecha_compra', None),
            "fecha_venta": request.json.get('fecha_venta', None),
            "numero_acciones": request.json.get('numero_acciones', None),
            "precio_accion_sin_comision": request.json.get('precio_accion_sin_comision', None),
            "precio_venta_sin_comision": request.json.get('precio_venta_sin_comision', None),
            "comision_compra": request.json.get('comision_compra', None),
            "otras_comisiones": request.json.get('otras_comisiones', None),
        }
        return finanzasposicionaccioncontroller.update_posicion_accion(params)

    @app.route(rootpath + "/posicionaccion/cerrar/<id_posicion_accion>", methods=['POST'])
    @login_required
    @serialize_response
    def cerrar_posicion_accion(id_posicion_accion: int):
        params = {
            "id": id_posicion_accion,
            "fecha_venta": request.json.get('fecha_venta', None),
            "precio_venta_sin_comision": request.json.get('precio_venta_sin_comision', None)
        }
        return finanzasposicionaccioncontroller.cerrar_posicion_accion(params)

    @app.route(rootpath + "/posicionaccion/deshacer-cerrar/<id_posicion_accion>", methods=['POST'])
    @login_required
    @serialize_response
    def deshacer_cerrar_posicion_accion(id_posicion_accion: int):
        params = {
            "id": id_posicion_accion,
        }
        return finanzasposicionaccioncontroller.deshacer_cerrar_posicion_accion(params)

    @app.route(rootpath + "/posicionaccion/<id_posicion_accion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_posicion_accion(id_posicion_accion: int):
        return finanzasposicionaccioncontroller.delete_posicion_accion(id_posicion_accion)

    @app.route(rootpath + "/posicionaccion/isin", methods=['GET'])
    @login_required
    @serialize_response
    def get_isins():
        return finanzasposicionaccioncontroller.list_unique_posiciones_acciones_isins()

    @app.route(rootpath + "/resumen/ingresos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_ingresos():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_ingresos(params)

    @app.route(rootpath + "/resumen/gastos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_gastos():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_gastos(params)

    @app.route(rootpath + "/resumen/cuentas-ingreso", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_ingreso():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_cuentas(params)

    @app.route(rootpath + "/resumen/cuentas-gasto", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_gasto():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_cuentas(params)

    @app.route(rootpath + "/resumen/cuentas-total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_cuentas_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_cuentas(params)

    @app.route(rootpath + "/resumen/monederos-ingreso", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_ingreso():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_monederos(params)

    @app.route(rootpath + "/resumen/monederos-gasto", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_gasto():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_monederos(params)

    @app.route(rootpath + "/resumen/monederos-total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_monederos_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_monederos(params)

    @app.route(rootpath + "/resumen/total", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_total(params)

    @app.route(rootpath + "/resumen/total-ingresos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total_ingresos():
        params = {
            "tipo": "ingresos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_total(params)

    @app.route(rootpath + "/resumen/total-gastos", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_total_gastos():
        params = {
            "tipo": "gastos",
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_total(params)

    @app.route(rootpath + "/resumen/valores_acciones_meses", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_valores_acciones_meses():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_valores_acciones_meses(params)

    @app.route(rootpath + "/resumen/valores_acciones_dias", methods=['GET'])
    @login_required
    @serialize_response
    def resumen_valores_acciones_dias():
        params = {
            "begin_fecha": request.args.get('begin_fecha', None),
            "end_fecha": request.args.get('end_fecha', None),
        }
        return finanzasresumencontroller.resumen_valores_acciones_dias(params)
