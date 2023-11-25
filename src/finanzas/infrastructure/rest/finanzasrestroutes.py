from flask import request
from flask_login import login_required
from src.finanzas.infrastructure.rest import finanzascontroller
from src.shared.infraestructure.rest.response import serialize_response


def import_routes(rootpath, app):
    @app.route(rootpath + "/cuenta", methods=['GET'])
    @login_required
    @serialize_response
    def list_cuentas():
        return finanzascontroller.list_cuentas(request)

    @app.route(rootpath + "/cuenta/<id_cuenta>", methods=['GET'])
    @login_required
    @serialize_response
    def get_cuenta(id_cuenta: int):
        return finanzascontroller.get_cuenta(request, id_cuenta)

    @app.route(rootpath + "/cuenta", methods=['POST'])
    @login_required
    @serialize_response
    def create_cuenta():
        return finanzascontroller.create_cuenta(request)

    @app.route(rootpath + "/cuenta/<id_cuenta>", methods=['POST'])
    @login_required
    @serialize_response
    def update_cuenta(id_cuenta: int):
        return finanzascontroller.update_cuenta(request, id_cuenta)

    @app.route(rootpath + "/monedero", methods=['GET'])
    @login_required
    @serialize_response
    def list_monederos():
        return finanzascontroller.list_monederos(request)

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['GET'])
    @login_required
    @serialize_response
    def get_monedero(id_monedero: int):
        return finanzascontroller.get_monedero(request, id_monedero)

    @app.route(rootpath + "/monedero", methods=['POST'])
    @login_required
    @serialize_response
    def create_monedero():
        return finanzascontroller.create_monedero(request)

    @app.route(rootpath + "/monedero/<id_monedero>", methods=['POST'])
    @login_required
    @serialize_response
    def update_monedero(id_monedero: int):
        return finanzascontroller.update_monedero(request, id_monedero)

    @app.route(rootpath + "/categoria_ingreso", methods=['GET'])
    @login_required
    @serialize_response
    def list_categorias_ingreso():
        return finanzascontroller.list_categorias_ingreso(request)

    @app.route(rootpath + "/categoria_ingreso/<id_categoria_ingreso>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_ingreso(id_categoria_ingreso: int):
        return finanzascontroller.get_categoria_ingreso(request, id_categoria_ingreso)

    @app.route(rootpath + "/categoria_ingreso", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_ingreso():
        return finanzascontroller.create_categoria_ingreso(request)

    @app.route(rootpath + "/categoria_ingreso/<id_categoria_ingreso>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_ingreso(id_categoria_ingreso: int):
        return finanzascontroller.update_categoria_ingreso(request, id_categoria_ingreso)

    @app.route(rootpath + "/categoria_gasto", methods=['GET'])
    @login_required
    @serialize_response
    def list_categorias_gasto():
        return finanzascontroller.list_categorias_gasto(request)

    @app.route(rootpath + "/categoria_gasto/<id_categoria_gasto>", methods=['GET'])
    @login_required
    @serialize_response
    def get_categoria_gasto(id_categoria_gasto: int):
        return finanzascontroller.get_categoria_gasto(request, id_categoria_gasto)

    @app.route(rootpath + "/categoria_gasto", methods=['POST'])
    @login_required
    @serialize_response
    def create_categoria_gasto():
        return finanzascontroller.create_categoria_gasto(request)

    @app.route(rootpath + "/categoria_gasto/<id_categoria_gasto>", methods=['POST'])
    @login_required
    @serialize_response
    def update_categoria_gasto(id_categoria_gasto: int):
        return finanzascontroller.update_categoria_gasto(request, id_categoria_gasto)

    @app.route(rootpath + "/operacion", methods=['GET'])
    @login_required
    @serialize_response
    def list_operaciones():
        return finanzascontroller.list_operaciones(request)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['GET'])
    @login_required
    @serialize_response
    def get_operacion(id_operacion: int):
        return finanzascontroller.get_operacion(request, id_operacion)

    @app.route(rootpath + "/operacion", methods=['POST'])
    @login_required
    @serialize_response
    def create_operacion():
        return finanzascontroller.create_operacion(request)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['POST'])
    @login_required
    @serialize_response
    def update_operacion(id_operacion: int):
        return finanzascontroller.update_operacion(request, id_operacion)

    @app.route(rootpath + "/operacion/<id_operacion>", methods=['DELETE'])
    @login_required
    @serialize_response
    def delete_operacion(id_operacion: int):
        return finanzascontroller.delete_operacion(request, id_operacion)
