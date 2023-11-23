from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


def _get_monedero_base_url(context) -> str:
    return common_functions.get_endpoint_server(context) + "/finanzas/monedero"


@given('Los siguientes monederos creados')
def given_monedero(context):
    for row in context.table:
        nombre = row["nombre"]
        cantidad_base = row["cantidad_base"]
        diferencia = row["diferencia"]

        context.database.exec_sql(
            'INSERT into finanzas_monederos ("nombre", "cantidad_base", "diferencia") values ("{}",{},{});'.format(
                nombre, cantidad_base, diferencia))


@when('Obtengo el monedero con id {id}')
def get_monedero(context, id):
    url = _get_monedero_base_url(context) + "/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo los monederos')
def list_monederos(context):
    url = _get_monedero_base_url(context)
    context.result = common_functions.make_get_request(context, url)


@when('Creo el siguiente monedero')
def create_monedero(context):
    for row in context.table:
        data = {
            "nombre": row.get("nombre"),
            "cantidad_base": row.get("cantidad_base"),
            "diferencia": row.get("diferencia")
        }
        url = _get_monedero_base_url(context)
        context.result = common_functions.make_post_request(context, url, data)


@when('Actualizo el monedero con id {id}')
def create_monedero(context, id):
    for row in context.table:
        data = {
            "nombre": row.get("nombre"),
            "cantidad_base": row.get("cantidad_base"),
            "diferencia": row.get("diferencia")
        }
        url = _get_monedero_base_url(context) + "/{}".format(id)
        context.result = common_functions.make_post_request(context, url, data)
