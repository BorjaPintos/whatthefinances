from tests.behave.shared.features.steps.common_steps import *
from behave import given

@given('Los siguientes usuarios creados')
def create_users(context):
    for row in context.table:
        name = row["name"]
        password = row["password"]
        context.database.exec_sql('INSERT into user ("name", "password") values ("{}","{}");'.format(name, password))
