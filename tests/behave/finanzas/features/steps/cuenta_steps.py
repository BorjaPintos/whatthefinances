from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


def _get_cuenta_base_url(context) -> str:
    return common_functions.get_endpoint_server(context) + "/finanzas/cuenta"


@given('Las siguientes cuentas creadas')
def given_cuenta(context):
    for row in context.table:
        nombre = row["nombre"]
        cantidad_inicial = row["cantidad_inicial"]
        diferencia = row["diferencia"]
        ponderacion = row["ponderacion"]

        context.database.exec_sql(
            'INSERT into finanzas_cuentas ("nombre", "cantidad_inicial", "diferencia", "ponderacion") values ("{}",{},{},{});'.format(
                nombre, cantidad_inicial, diferencia, ponderacion))


@when('Obtengo la cuenta con id {id}')
def get_cuenta(context, id):
    url = _get_cuenta_base_url(context) + "/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las cuentas')
def list_cuentas(context):
    url = _get_cuenta_base_url(context)
    context.result = common_functions.make_get_request(context, url)


@when('Creo la siguiente cuenta')
def create_cuenta(context):
    for row in context.table:
        data = {
            "nombre": row.get("nombre"),
            "cantidad_inicial": float(row.get("cantidad_inicial")),
            "ponderacion": float(row.get("ponderacion"))
        }
        url = _get_cuenta_base_url(context)
        context.result = common_functions.make_post_request(context, url, data)


@when('Actualizo la cuenta con id {id}')
def update_cuenta(context, id):
    for row in context.table:
        data = {
            "nombre": row.get("nombre"),
            "cantidad_inicial": float(row.get("cantidad_inicial")),
            "ponderacion": float(row.get("ponderacion"))
        }
        url = _get_cuenta_base_url(context) + "/{}".format(id)
        context.result = common_functions.make_post_request(context, url, data)
