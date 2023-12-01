from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


def _get_categoria_gasto_base_url(context) -> str:
    return common_functions.get_endpoint_server(context) + "/finanzas/categoria_gasto"


@given('Las siguientes categorias_gasto creadas')
def given_categoria_gasto(context):
    for row in context.table:
        descripcion = row["descripcion"]
        id_cuenta_cargo_defecto = row["id_cuenta_cargo_defecto"]
        id_monedero_defecto = row["id_monedero_defecto"]

        context.database.exec_sql(
            'INSERT into finanzas_categorias_gasto ("descripcion", "id_cuenta_cargo_defecto", "id_monedero_defecto") values ("{}",{},{});'.format(
                descripcion, id_cuenta_cargo_defecto, id_monedero_defecto))


@when('Obtengo la categoria_gasto con id {id}')
def get_categoria_gasto(context, id):
    url = _get_categoria_gasto_base_url(context) + "/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las categorias_gasto')
def list_categoria_gasto(context):
    url = _get_categoria_gasto_base_url(context)
    context.result = common_functions.make_get_request(context, url)


@when('Creo la siguiente categoria_gasto')
def create_categoria_gasto(context):
    for row in context.table:
        data = {
            "descripcion": row.get("descripcion"),
            "id_cuenta_cargo_defecto": int(row.get("id_cuenta_cargo_defecto")) if row.get(
                "id_cuenta_cargo_defecto") else None,
            "id_monedero_defecto": int(row.get("id_monedero_defecto")) if row.get("id_monedero_defecto") else None
        }
        url = _get_categoria_gasto_base_url(context)
        context.result = common_functions.make_post_request(context, url, data)


@when('Actualizo la categoria_gasto con id {id}')
def update_categoria_gasto(context, id):
    for row in context.table:
        data = {
            "descripcion": row.get("descripcion"),
            "id_cuenta_cargo_defecto": int(row.get("id_cuenta_cargo_defecto")) if row.get(
                "id_cuenta_cargo_defecto") else None,
            "id_monedero_defecto": int(row.get("id_monedero_defecto")) if row.get("id_monedero_defecto") else None
        }
        url = _get_categoria_gasto_base_url(context) + "/{}".format(id)
        context.result = common_functions.make_post_request(context, url, data)
