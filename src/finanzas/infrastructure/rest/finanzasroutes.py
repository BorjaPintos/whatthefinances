from flask import request
from flask_login import login_required

from src.finanzas.application.listcategoriasgasto import ListCategoriasGasto
from src.finanzas.application.listcategoriasingreso import ListCategoriasIngreso
from src.finanzas.application.listcuentas import ListCuentas
from src.finanzas.application.listmonederos import ListMonederos
from src.finanzas.application.listoperaciones import ListOperaciones
from src.finanzas.infrastructure.persistence.categoriagastorepositorysqlalchemy import \
    CategoriaGastoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.categoriaingresorepositorysqlalchemy import \
    CategoriaIngresoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.cuentarepositorysqlalchemy import CuentaRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.monederorepositorysqlalchemy import MonederoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.operacionrepositorysqlalchemy import OperacionRepositorySQLAlchemy
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    list_cuentas_use_case = ListCuentas(cuenta_repository=CuentaRepositorySQLAlchemy())
    list_monederos_use_case = ListMonederos(monedero_repository=MonederoRepositorySQLAlchemy())
    list_categorias_ingreso_use_case = ListCategoriasIngreso(
        categorias_ingreso_repository=CategoriaIngresoRepositorySQLAlchemy())
    list_categorias_gasto_use_case = ListCategoriasGasto(
        categorias_gasto_repository=CategoriaGastoRepositorySQLAlchemy())

    list_operaciones_use_case = ListOperaciones(
        operacion_repository=OperacionRepositorySQLAlchemy())

    @app.route(rootpath + "/cuenta", methods=['GET'])
    # @login_required
    @serialize_response
    def list_cuentas():
        code = 200
        params = {
            "order_property": request.args.get('order_property', 'descripcion'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        elements = list_cuentas_use_case.execute(params)
        response = []
        for element in elements:
            response.append(element.get_dto())
        return response, code

    @app.route(rootpath + "/monedero", methods=['GET'])
    # @login_required
    @serialize_response
    def list_monederos():
        code = 200
        params = {
            "order_property": request.args.get('order_property', 'descripcion'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        elements = list_monederos_use_case.execute(params)
        response = []
        for element in elements:
            response.append(element.get_dto())
        return response, code

    @app.route(rootpath + "/categorias_ingreso", methods=['GET'])
    # @login_required
    @serialize_response
    def list_categorias_ingreso():
        code = 200
        params = {
            "order_property": request.args.get('order_property', 'descripcion'),
            "order_type": request.args.get('order_type', 'asc'),
            "descripcion": request.args.get('descripcion', None),
            "id_monedero_defecto": request.args.get('id_monedero_defecto', None),
            "id_cuenta_abono_defecto": request.args.get('id_cuenta_abono_defecto', None),
        }
        elements = list_categorias_ingreso_use_case.execute(params)
        response = []
        for element in elements:
            response.append(element.get_dto())
        return response, code

    @app.route(rootpath + "/categorias_gasto", methods=['GET'])
    # @login_required
    @serialize_response
    def list_categorias_gasto():
        code = 200
        params = {
            "order_property": request.args.get('order_property', 'descripcion'),
            "order_type": request.args.get('order_type', 'asc'),
            "descripcion": request.args.get('descripcion', None),
            "id_monedero_defecto": request.args.get('id_monedero_defecto', None),
            "id_cuenta_cargo_defecto": request.args.get('id_cuenta_cargo_defecto', None),
        }
        elements = list_categorias_gasto_use_case.execute(params)
        response = []
        for element in elements:
            response.append(element.get_dto())
        return response, code

    @app.route(rootpath + "/operacion", methods=['GET'])
    # @login_required
    @serialize_response
    def list_operaciones():
        code = 200
        params = {
            "order_property": request.args.get('order_property', 'fecha'),
            "order_type": request.args.get('order_type', 'asc'),
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
        elements = list_operaciones_use_case.execute(params)
        response = []
        for element in elements:
            response.append(element.get_dto())
        return response, code
