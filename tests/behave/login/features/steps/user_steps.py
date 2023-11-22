from tests.behave.shared.features.steps.common_steps import *
from behave import when


@given('Los siguientes usuarios creados')
def create_users(context):
    for row in context.table:
        name = row["name"]
        password = row["password"]
        context.database.exec_sql('INSERT into user ("name", "password") values ("{}","{}");'.format(name, password))

@when('Obtengo el usuario con id {id}')
def get_user(context, id):
    url = common_functions.get_endpoint_server(context) + "/user/{}".format(id)
    context.result = common_functions.make_get_request(context, url)
