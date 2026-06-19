from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


def _get_posicion_base_url(context) -> str:
    return common_functions.get_endpoint_server(context) + "/finanzas/posicion"


@given('Los siguientes productos creados')
def given_producto(context):
    for row in context.table:
        context.database.exec_sql(
            'INSERT into finanzas_productos ("nombre", "isin") values ("{}","{}");'.format(
                row["nombre"], row["isin"]))


@given('Los siguientes brokers creados')
def given_broker(context):
    for row in context.table:
        context.database.exec_sql(
            'INSERT into finanzas_brokers ("nombre", "extranjero") values ("{}",{});'.format(
                row["nombre"], row["extranjero"]))


@given('Las siguientes bolsas creadas')
def given_bolsa(context):
    for row in context.table:
        context.database.exec_sql(
            'INSERT into finanzas_bolsas ("nombre") values ("{}");'.format(
                row["nombre"]))


@given('Las siguientes posiciones creadas')
def given_posicion(context):
    for row in context.table:
        context.database.exec_sql(
            'INSERT into finanzas_posiciones '
            '("isin", "fecha_compra", "numero_participaciones", "id_bolsa", "id_broker", '
            '"precio_compra_sin_comision", "comision_compra", "otras_comisiones", "abierta") '
            'values ("{}",\'{}\',{},{},{},{},{},{},{});'.format(
                row["isin"],
                row["fecha_compra"],
                row["numero_participaciones"],
                row["id_bolsa"],
                row["id_broker"],
                row["precio_compra_sin_comision"],
                row["comision_compra"],
                row["otras_comisiones"],
                row["abierta"]))


@when('Listo las posiciones')
def list_posiciones(context):
    url = _get_posicion_base_url(context)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las posiciones con filtro abierta {valor}')
def list_posiciones_with_filter(context, valor):
    url = _get_posicion_base_url(context) + "?abierta={}".format(valor)
    context.result = common_functions.make_get_request(context, url)


@when('Cierro la posicion con id {id}')
def cerrar_posicion(context, id):
    for row in context.table:
        data = {}
        if "fecha_venta" in row:
            data["fecha_venta"] = row["fecha_venta"]
        if "comision_venta" in row:
            data["comision_venta"] = float(row["comision_venta"])
        url = _get_posicion_base_url(context) + "/cerrar/{}".format(id)
        context.result = common_functions.make_post_request(context, url, data)


@when('Deshago el cierre de la posicion con id {id}')
def deshacer_cerrar_posicion(context, id):
    url = _get_posicion_base_url(context) + "/deshacer-cerrar/{}".format(id)
    context.result = common_functions.make_post_request(context, url, {})
