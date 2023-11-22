from tests.behave.shared.features.steps.common_steps import *
from behave import when

@when('Obtengo el usuario con id {id}')
def get_user(context, id):
    url = common_functions.get_endpoint_server(context) + "/user/{}".format(id)
    context.result = common_functions.make_get_request(context, url)
