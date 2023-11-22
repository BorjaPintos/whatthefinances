from flask import request
from flask_login import login_required
from loguru import logger

from src.finanzas.application.createcategoriagasto import CreateCategoriaGasto
from src.finanzas.application.createcategoriaingreso import CreateCategoriaIngreso
from src.finanzas.application.createcuenta import CreateCuenta
from src.finanzas.application.createmonedero import CreateMonedero
from src.finanzas.application.createoperacion import CreateOperacion
from src.finanzas.application.deleteoperacion import DeleteOperacion
from src.finanzas.application.getcategoriagasto import GetCategoriaGasto
from src.finanzas.application.getcategoriaingreso import GetCategoriaIngreso
from src.finanzas.application.getcuenta import GetCuenta
from src.finanzas.application.getmonedero import GetMonedero
from src.finanzas.application.getoperacion import GetOperacion
from src.finanzas.application.listcategoriasgasto import ListCategoriasGasto
from src.finanzas.application.listcategoriasingreso import ListCategoriasIngreso
from src.finanzas.application.listcuentas import ListCuentas
from src.finanzas.application.listmonederos import ListMonederos
from src.finanzas.application.listoperaciones import ListOperaciones
from src.finanzas.application.updatecategoriagasto import UpdateCategoriaGasto
from src.finanzas.application.updatecategoriaingreso import UpdateCategoriaIngreso
from src.finanzas.application.updatecuenta import UpdateCuenta
from src.finanzas.application.updatemonedero import UpdateMonedero
from src.finanzas.application.updateoperacion import UpdateOperacion
from src.finanzas.infrastructure.persistence.categoriagastorepositorysqlalchemy import \
    CategoriaGastoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.categoriaingresorepositorysqlalchemy import \
    CategoriaIngresoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.cuentarepositorysqlalchemy import CuentaRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.monederorepositorysqlalchemy import MonederoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.operacionrepositorysqlalchemy import OperacionRepositorySQLAlchemy
from src.shared.infraestructure.rest.response import serialize_response
from src.shared.infraestructure.rest.responseerror import Error


def import_routes(rootpath, app):
    cuenta_repository = CuentaRepositorySQLAlchemy()
    monedero_repository = MonederoRepositorySQLAlchemy()
    categorias_ingreso_repository = CategoriaIngresoRepositorySQLAlchemy()
    categorias_gasto_repository = CategoriaGastoRepositorySQLAlchemy()
    operacion_repository = OperacionRepositorySQLAlchemy()

    list_cuentas_use_case = ListCuentas(cuenta_repository=cuenta_repository)
    get_cuenta_use_case = GetCuenta(cuenta_repository=cuenta_repository)
    create_cuenta_use_case = CreateCuenta(cuenta_repository=cuenta_repository)
    update_cuenta_use_case = UpdateCuenta(cuenta_repository=cuenta_repository)

    list_monederos_use_case = ListMonederos(monedero_repository=monedero_repository)
    get_monedero_use_case = GetMonedero(monedero_repository=monedero_repository)
    create_monedero_use_case = CreateMonedero(monedero_repository=monedero_repository)
    update_monedero_use_case = UpdateMonedero(monedero_repository=monedero_repository)

    list_categorias_ingreso_use_case = ListCategoriasIngreso(
        categoria_ingreso_repository=categorias_ingreso_repository)
    get_categoria_ingreso_use_case = GetCategoriaIngreso(categoria_ingreso_repository=categorias_ingreso_repository)
    create_categoria_ingreso_use_case = CreateCategoriaIngreso(
        categoria_ingreso_repository=categorias_ingreso_repository)
    update_categoria_ingreso_use_case = UpdateCategoriaIngreso(
        categoria_ingreso_repository=categorias_ingreso_repository)

    list_categorias_gasto_use_case = ListCategoriasGasto(categoria_gasto_repository=categorias_gasto_repository)
    get_categoria_gasto_use_case = GetCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)
    create_categoria_gasto_use_case = CreateCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)
    update_categoria_gasto_use_case = UpdateCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)

    list_operaciones_use_case = ListOperaciones(operacion_repository=operacion_repository)
    get_operacion_use_case = GetOperacion(operacion_repository=operacion_repository)
    create_operacion_use_case = CreateOperacion(operacion_repository=operacion_repository)
    update_operacion_use_case = UpdateOperacion(operacion_repository=operacion_repository)
    delete_operacion_use_case = DeleteOperacion(operacion_repository=operacion_repository)

    @app.route(rootpath + "/cuenta", methods=['GET'])
    @login_required
    @serialize_response
    def list_cuentas():
        code = 200
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        elements = list_cuentas_use_case.execute(params)
        response = []
        for element in elements:
            response.append(element.get_dto())
        return response, code

    @app.route(rootpath + "/cuenta/<id_cuenta>", methods=['GET'])
    @login_required
    @serialize_response
    def get_cuenta(id_cuenta: int):
        code = 200
        cuenta = get_cuenta_use_case.execute(id_cuenta)
        if cuenta:
            response = cuenta.get_dto()
        else:
            code = 404
            logger.warning(
                "Por alguna razón no devuelve la cuenta con id {} y no da la excepción de not found".format(id_cuenta))
            response = Error("No se ha podido obtener la cuenta con id: {}".format(id_cuenta), code)
        return response, code

    @app.route(rootpath + "/cuenta", methods=['POST'])
    @login_required
    @serialize_response
    def create_cuenta():
        code = 201
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_base": request.json.get('cantidad_base', 0.00),
            "diferencia": request.json.get('diferencia', 0.00),
            "ponderacion": request.json.get('ponderacion', 0.00),
        }
        cuenta = create_cuenta_use_case.execute(params)
        if cuenta:
            response = cuenta.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe una cuenta con ese nombre: {}".format(params.get("nombre")))
            response = Error("Parece que ya existe una cuenta con ese nombre: {}".format(params.get("nombre")), code)
            return response, code

    @app.route(rootpath + "/cuenta/<id_cuenta>", methods=['POST'])
    @login_required
    @serialize_response
    def update_cuenta(id_cuenta: int):
        code = 200
        params = {
            "id": id_cuenta,
            "nombre": request.json.get('nombre', None),
            "cantidad_base": request.json.get('cantidad_base', None),
            "ponderacion": request.json.get('ponderacion', None),
        }
        cuenta = update_cuenta_use_case.execute(params)
        if cuenta:
            response = cuenta.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe una cuenta con ese nombre: {}".format(params.get("nombre")))
            response = Error("Parece que ya existe una cuenta con ese nombre: {}".format(params.get("nombre")), code)
            return response, code

    @app.route(rootpath + "/monedero", methods=['GET'])
    @login_required
    @serialize_response
    def list_monederos():
        code = 200
        params = {
            "order_property": request.args.get('order_property', 'nombre'),
            "order_type": request.args.get('order_type', 'asc'),
            "nombre": request.args.get('nombre', None)
        }
        elements = list_monederos_use_case.execute(params)
        response = []
        for element in elements:
            response.append(element.get_dto())
        return response, code

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['GET'])
    @login_required
    @serialize_response
    def get_monedero(id_monedero: int):
        code = 200
        monedero = get_monedero_use_case.execute(id_monedero)
        if monedero:
            response = monedero.get_dto()
        else:
            code = 404
            logger.warning(
                "Por alguna razón no devuelve el monedero con id {} y no da la excepción de not found".format(
                    id_monedero))
            response = Error("No se ha podido obtener el monedero con id: {}".format(id_monedero), code)
        return response, code

    @app.route(rootpath + "/monedero", methods=['POST'])
    @login_required
    @serialize_response
    def create_monedero():
        code = 201
        params = {
            "nombre": request.json.get('nombre'),
            "cantidad_base": request.json.get('cantidad_base', 0.00),
            "diferencia": request.json.get('diferencia', 0.00)
        }
        monedero = create_monedero_use_case.execute(params)
        if monedero:
            response = monedero.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe un monedero con ese nombre: {}".format(params.get("nombre")))
            response = Error("Parece que ya existe un monedero con ese nombre: {}".format(params.get("nombre")), code)
            return response, code

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['POST'])
    @login_required
    @serialize_response
    def update_monedero(id_monedero: int):
        code = 200
        params = {
            "id": id_monedero,
            "nombre": request.json.get('nombre', None),
            "cantidad_base": request.json.get('cantidad_base', None)
        }
        monedero = update_monedero_use_case.execute(params)
        if monedero:
            response = monedero.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe un monedero con ese nombre: {}".format(params.get("nombre")))
            response = Error("Parece que ya existe un monedero con ese nombre: {}".format(params.get("nombre")), code)
            return response, code

    @app.route(rootpath + "/categoria_ingreso", methods=['GET'])
    @login_required
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

    @app.route(rootpath + "/categoria_ingreso/<id_categoria_ingreso>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_ingreso(id_categoria_ingreso: int):
        code = 200
        categoria_ingreso = get_categoria_ingreso_use_case.execute(id_categoria_ingreso)
        if categoria_ingreso:
            response = categoria_ingreso.get_dto()
        else:
            code = 404
            logger.warning(
                "Por alguna razón no devuelve la categoría ingreso con id {} y no da la excepción de not found".format(
                    id_categoria_ingreso))
            response = Error("No se ha podido obtener la categoría ingreso con id: {}".format(id_categoria_ingreso),
                             code)
        return response, code

    @app.route(rootpath + "/categoria_ingreso", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_ingreso():
        code = 201
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_abono_defecto": request.json.get('id_cuenta_abono_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        categoria_ingreso = create_categoria_ingreso_use_case.execute(params)
        if categoria_ingreso:
            response = categoria_ingreso.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")))
            response = Error(
                "Parece que ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")),
                code)
            return response, code

    @app.route(rootpath + "/categoria_ingreso/<id_categoria_ingreso>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_ingreso(id_categoria_ingreso: int):
        code = 200
        params = {
            "id": id_categoria_ingreso,
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_abono_defecto": request.json.get('id_cuenta_abono_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        categoria_ingreso = update_categoria_ingreso_use_case.execute(params)
        if categoria_ingreso:
            response = categoria_ingreso.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")))
            response = Error(
                "Parece que ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")),
                code)
            return response, code

    @app.route(rootpath + "/categoria_gasto", methods=['GET'])
    @login_required
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

    @app.route(rootpath + "/categoria_gasto/<id_categoria_gasto>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_gasto(id_categoria_gasto: int):
        code = 200
        categoria_gasto = get_categoria_gasto_use_case.execute(id_categoria_gasto)
        if categoria_gasto:
            response = categoria_gasto.get_dto()
        else:
            code = 404
            logger.warning(
                "Por alguna razón no devuelve la categoría gasto con id {} y no da la excepción de not found".format(
                    id_categoria_gasto))
            response = Error("No se ha podido obtener la categoría gasto con id: {}".format(id_categoria_gasto), code)
        return response, code

    @app.route(rootpath + "/categoria_gasto", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_gasto():
        code = 201
        params = {
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_cargo_defecto": request.json.get('id_cuenta_cargo_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        categoria_gasto = create_categoria_gasto_use_case.execute(params)
        if categoria_gasto:
            response = categoria_gasto.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")))
            response = Error(
                "Parece que ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")),
                code)
            return response, code

    @app.route(rootpath + "/categoria_gasto/<id_categoria_gasto>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_gasto(id_categoria_gasto: int):
        code = 200
        params = {
            "id": id_categoria_gasto,
            "descripcion": request.json.get('descripcion', None),
            "id_cuenta_cargo_defecto": request.json.get('id_cuenta_cargo_defecto', None),
            "id_monedero_defecto": request.json.get('id_monedero_defecto', None)
        }
        categoria_gasto = update_categoria_gasto_use_case.execute(params)
        if categoria_gasto:
            response = categoria_gasto.get_dto()
            return response, code
        else:
            code = 409
            logger.warning("Ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")))
            response = Error(
                "Parece que ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")),
                code)
            return response, code

    @app.route(rootpath + "/operacion", methods=['GET'])
    @login_required
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

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['GET'])
    @login_required
    @serialize_response
    def get_operacion(id_operacion: int):
        code = 200
        operacion = get_operacion_use_case.execute(id_operacion)
        if operacion:
            response = operacion.get_dto()
        else:
            code = 404
            logger.warning(
                "Por alguna razón no devuelve la operación con id {} y no da la excepción de not found".format(
                    id_operacion))
            response = Error("No se ha podido obtener la operación con id: {}".format(id_operacion), code)
        return response, code

    @app.route(rootpath + "/operacion", methods=['POST'])
    @login_required
    @serialize_response
    def create_operacion():
        code = 201
        params = {
            "descripcion": request.json.get('descripcion', None),
            "fecha": request.json.get('begin_fecha', None),
            "cantidad": request.json.get('begin_cantidad', None),
            "id_monedero_cargo": request.json.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.json.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.json.get('id_monedero_abono', None),
            "id_cuenta_abono": request.json.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.json.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.json.get('id_categoria_ingreso', None),
        }
        operacion = create_operacion_use_case.execute(params)
        if operacion:
            response = operacion.get_dto()
            return response, code
        else:
            code = 400
            logger.warning("Error al crear la operacion: {}".format(params.get("descripcion")))
            response = Error("Error al crear la operacion: {}".format(params.get("descripcion")), code)
            return response, code

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['POST'])
    @login_required
    @serialize_response
    def update_operacion(id_operacion: int):
        code = 200
        params = {
            "id": id_operacion,
            "descripcion": request.json.get('descripcion', None),
            "fecha": request.json.get('begin_fecha', None),
            "cantidad": request.json.get('begin_cantidad', None),
            "id_monedero_cargo": request.json.get('id_monedero_cargo', None),
            "id_cuenta_cargo": request.json.get('id_cuenta_cargo', None),
            "id_monedero_abono": request.json.get('id_monedero_abono', None),
            "id_cuenta_abono": request.json.get('id_cuenta_abono', None),
            "id_categoria_gasto": request.json.get('id_categoria_gasto', None),
            "id_categoria_ingreso": request.json.get('id_categoria_ingreso', None),
        }
        operacion = update_operacion_use_case.execute(params)
        if operacion:
            response = operacion.get_dto()
            return response, code
        else:
            code = 400
            logger.warning("Error al actualizar la operacion con id: {}".format(id_operacion))
            response = Error("Error al actualizar la operacion con id: {}".format(id_operacion), code)
            return response, code

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_operacion(id_operacion: int):
        code = 200
        operacion = delete_operacion_use_case.execute(id_operacion)
        if operacion:
            return {}, code
        else:
            code = 400
            logger.warning("Error al eliminar la operacion con id: {}".format(id_operacion))
            response = Error("Error al eliminar la operacion con id: {}".format(id_operacion), code)
            return response, code
