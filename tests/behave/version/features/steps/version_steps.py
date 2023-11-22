from behave import when
from tests.behave.shared.features.steps.common_steps import *
from tests.behave.shared import common_functions


@when('Pido la version')
def get_version(context):
    url = common_functions.get_endpoint_server(context) + "/version"
    context.result = common_functions.make_get_request(context, url)

