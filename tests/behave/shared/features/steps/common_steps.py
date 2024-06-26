from behave import then, when, given
from tests.behave.shared import common_functions


@then(u'Obtengo el siguiente objeto')
def check_item(context):
    element = context.result.json()
    items = common_functions.retrieve_context_table(context)
    if len(items) != 1:
        raise AssertionError('There must be only one item')
    else:
        for k in items[0]:
            assert (k in element)
            assert (k in items[0])
            assert (str(items[0][k]) == str(element[k]))
    return items[0] == element


@then(u'Obtengo la siguiente lista')
def check_list(context):
    event_list = context.result.json()
    table = common_functions.retrieve_context_table(context)
    common_functions.check_list_elements_by_keys(table, event_list)

@then(u'Obtengo una lista vacía')
def check_list(context):
    event_list = context.result.json()
    if len(event_list) != 0:
        raise AssertionError(f'Expected 0 elements, found {len(event_list)}')


@then(u'Obtengo la siguiente lista paginada')
def check_pagination_list(context):
    pagination_list = context.result.json()
    table = common_functions.retrieve_context_table(context)
    elements = pagination_list.get("elements")
    common_functions.check_list_elements_by_keys(table, elements)


@then(u'No obtengo nada paginado')
def check_pagination_list(context):
    pagination_list = context.result.json()
    elements = pagination_list.get("elements")
    if len(elements) != 0:
        raise AssertionError(f'Expected 0 elements, found {len(elements)}')


@then(u'No hay mas elementos en la lista paginada')
def check_pagination_more_elements(context):
    pagination_list = context.result.json()
    more_elements = pagination_list.get("has_more_elements")
    if more_elements:
        raise AssertionError("Existen más elementos de los que se piden")


@then(u'Hay mas elementos en la lista paginada')
def check_pagination_more_elements(context):
    pagination_list = context.result.json()
    more_elements = pagination_list.get("has_more_elements")
    if not more_elements:
        raise AssertionError("No existen más elementos de los que se piden")


@then('Obtengo el codigo de estado {code}')
def status_code(context, code):
    if str(context.result.status_code) != str(code):
        raise AssertionError(
            "expected:" + str(code) + " -> actual: " + str(context.result.status_code))
    assert (str(context.result.status_code) == str(code))


@when('Me logueo como el usuario {name} y contraseña {password}')
def login(context, name, password):
    url = common_functions.get_endpoint_server(context) + '/login'
    data = {"name": name,
            "password": password}
    context.result = common_functions.make_post_request(context, url, data)


@given('Una sesion correcta')
def create_users(context):
    context.database.exec_sql('INSERT into users ("name", "password") values ("{}","{}");'.format("admin",
                                                                                                 "addd55c9db8c0d868e7a826df9c58c364dda0bbd25e151f9acfaf993e73c5fb1276d119d3a11c2931aeb72fc3131a71c61edfa291cf261347e8377108fa61c22"))
    url = common_functions.get_endpoint_server(context) + '/login'
    data = {"name": "admin",
            "password": "test"}
    context.token = common_functions.make_post_request(context, url, data).json().get("token")


@then('Obtengo el token')
def get_token(context):
    assert "token" in context.result.json()
