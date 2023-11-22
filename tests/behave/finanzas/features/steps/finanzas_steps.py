from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


@given('Las siguientes cuentas creadas')
def create_cuenta(context):
    for row in context.table:
        nombre = row["nombre"]
        cantidad_base = row["cantidad_base"]
        diferencia = row["diferencia"]
        ponderacion = row["ponderacion"]

        context.database.exec_sql(
            'INSERT into finanzas_cuentas ("nombre", "cantidad_base", "diferencia", "ponderacion") values ("{}",{}, {},{});'.format(
                nombre, cantidad_base, diferencia, ponderacion))

@given('Los siguientes monederos creados')
def create_monedero(context):
    for row in context.table:
        nombre = row["nombre"]
        cantidad_base = row["cantidad_base"]
        diferencia = row["diferencia"]

        context.database.exec_sql(
            'INSERT into finanzas_monederos ("nombre", "cantidad_base", "diferencia") values ("{}",{},{});'.format(
                nombre, cantidad_base, diferencia))

@when('Obtengo la cuenta con id {id}')
def get_cuenta(context, id):
    url = common_functions.get_endpoint_server(context) + "/finanzas/cuenta/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Obtengo el monedero con id {id}')
def get_monedero(context, id):
    url = common_functions.get_endpoint_server(context) + "/finanzas/monedero/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Obtengo la categoria ingreso con id {id}')
def get_categoria_ingreso(context, id):
    url = common_functions.get_endpoint_server(context) + "/finanzas/categoria_ingreso/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Obtengo la categoria gasto con id {id}')
def get_categoria_gasto(context, id):
    url = common_functions.get_endpoint_server(context) + "/finanzas/categoria_gasto/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Obtengo la operacion con id {id}')
def get_operacion(context, id):
    url = common_functions.get_endpoint_server(context) + "/finanzas/operacion/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las cuentas')
def list_cuentas(context):
    url = common_functions.get_endpoint_server(context) + "/finanzas/cuenta".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo los monederos')
def list_monederos(context):
    url = common_functions.get_endpoint_server(context) + "/finanzas/monedero".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las categorias ingreso')
def list_categorias_ingreso(context):
    url = common_functions.get_endpoint_server(context) + "/finanzas/categoria_ingreso".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las categorias gasto')
def list_categorias_gasto(context):
    url = common_functions.get_endpoint_server(context) + "/finanzas/categoria_gasto".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las operacion')
def list_operaciones(context):
    url = common_functions.get_endpoint_server(context) + "/finanzas/operacion".format(id)
    context.result = common_functions.make_get_request(context, url)
