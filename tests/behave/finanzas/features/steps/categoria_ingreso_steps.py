from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


def _get_categoria_ingreso_base_url(context) -> str:
    return common_functions.get_endpoint_server(context) + "/finanzas/categoria_ingreso"

@given('Las siguientes categorias_ingreso creadas')
def given_categoria_ingreso(context):
    for row in context.table:
        descripcion = row["descripcion"]
        id_cuenta_abono_defecto = row["id_cuenta_abono_defecto"]
        id_monedero_defecto = row["id_monedero_defecto"]

        context.database.exec_sql(
            'INSERT into finanzas_categorias_ingreso ("descripcion", "id_cuenta_abono_defecto", "id_monedero_defecto") values ("{}",{},{});'.format(
                descripcion, id_cuenta_abono_defecto, id_monedero_defecto))


@when('Obtengo la categoria_ingreso con id {id}')
def get_categoria_ingreso(context, id):
    url = _get_categoria_ingreso_base_url(context) + "/{}".format(id)
    context.result = common_functions.make_get_request(context, url)


@when('Listo las categorias_ingreso')
def list_categoria_ingreso(context):
    url = _get_categoria_ingreso_base_url(context)
    context.result = common_functions.make_get_request(context, url)


@when('Creo la siguiente categoria_ingreso')
def create_categoria_ingreso(context):
    for row in context.table:
        data = {
            "descripcion": row.get("descripcion"),
            "id_cuenta_abono_defecto": int(row.get("id_cuenta_abono_defecto")) if row.get("id_cuenta_abono_defecto") else None,
            "id_monedero_defecto": int(row.get("id_monedero_defecto"))if row.get("id_monedero_defecto") else None
        }
        url = _get_categoria_ingreso_base_url(context)
        context.result = common_functions.make_post_request(context, url, data)


@when('Actualizo la categoria_ingreso con id {id}')
def update_categoria_ingreso(context, id):
    for row in context.table:
        data = {
            "descripcion": row.get("descripcion"),
            "id_cuenta_abono_defecto": int(row.get("id_cuenta_abono_defecto")) if row.get("id_cuenta_abono_defecto") else None,
            "id_monedero_defecto": int(row.get("id_monedero_defecto"))if row.get("id_monedero_defecto") else None
        }
        url = _get_categoria_ingreso_base_url(context) + "/{}".format(id)
        context.result = common_functions.make_post_request(context, url, data)
