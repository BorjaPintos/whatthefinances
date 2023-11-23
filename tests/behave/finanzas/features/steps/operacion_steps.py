from tests.behave.shared.features.steps.common_steps import *

from behave import when, given


@when('Obtengo la operacion con id {id}')
def get_operacion(context, id):
    url = common_functions.get_endpoint_server(context) + "/finanzas/operacion/{}".format(id)
    context.result = common_functions.make_get_request(context, url)

@when('Listo las operacion')
def list_operaciones(context):
    url = common_functions.get_endpoint_server(context) + "/finanzas/operacion".format(id)
    context.result = common_functions.make_get_request(context, url)
