from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


def _get_operacion_base_url(context) -> str:
    return common_functions.get_endpoint_server(context) + "/finanzas/operacion"


@when('Obtengo la operacion con id {id}')
def get_operacion(context, id):
    url = _get_operacion_base_url(context) + "/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo {count} operaciones desde la pagina {offset}')
def list_operaciones(context, count, offset):
    url = _get_operacion_base_url(context) + "?count={}&offset={}".format(count, offset)
    context.result = common_functions.make_get_request(context, url)


@when('Creo la siguiente operacion')
def create_operacion(context):
    for row in context.table:
        data = {
            "fecha": row.get("fecha"),
            "descripcion": row.get("descripcion"),
            "cantidad": float(row.get("cantidad")),
            "id_cuenta_abono": int(row.get("id_cuenta_abono")) if row.get("id_cuenta_abono") else None,
            "id_monedero_abono": int(row.get("id_monedero_abono")) if row.get("id_monedero_abono") else None,
            "id_categoria_ingreso": int(row.get("id_categoria_ingreso")) if row.get("id_categoria_ingreso") else None,
            "id_cuenta_cargo": int(row.get("id_cuenta_cargo")) if row.get("id_cuenta_cargo") else None,
            "id_monedero_cargo": int(row.get("id_monedero_cargo")) if row.get("id_monedero_cargo") else None,
            "id_categoria_gasto": int(row.get("id_categoria_gasto")) if row.get("id_categoria_gasto") else None
        }
        url = _get_operacion_base_url(context)
        context.result = common_functions.make_post_request(context, url, data)


@when('Actualizo la operacion con id {id}')
def update_operacion(context, id):
    for row in context.table:
        data = {
            "fecha": row.get("fecha"),
            "descripcion": row.get("descripcion"),
            "cantidad": float(row.get("cantidad")),
            "id_cuenta_abono": int(row.get("id_cuenta_abono")) if row.get("id_cuenta_abono") else None,
            "id_monedero_abono": int(row.get("id_monedero_abono")) if row.get("id_monedero_abono") else None,
            "id_categoria_ingreso": int(row.get("id_categoria_ingreso")) if row.get("id_categoria_ingreso") else None,
            "id_cuenta_cargo": int(row.get("id_cuenta_cargo")) if row.get("id_cuenta_cargo") else None,
            "id_monedero_cargo": int(row.get("id_monedero_cargo")) if row.get("id_monedero_cargo") else None,
            "id_categoria_gasto": int(row.get("id_categoria_gasto")) if row.get("id_categoria_gasto") else None
        }
        url = _get_operacion_base_url(context) + "/{}".format(id)
        context.result = common_functions.make_post_request(context, url, data)


@when('Borro la operacion con id {id}')
def delete_operacion(context, id):
    url = _get_operacion_base_url(context) + "/{}".format(id)
    context.result = common_functions.make_delete_request(context, url)
