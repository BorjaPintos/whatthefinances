from src.configuration.infrastruture.loadjsonconfiguration import LoadJsonConfiguration
from src.persistence.application.databasemanager import DatabaseManager


def load_config(context):
    config = LoadJsonConfiguration().load_from_file("behave_config.json")
    context.config = config
    context.database = DatabaseManager.init(config["database"])
    return context

def before_scenario(context, scenario):
    context.token = None
    database = context.database
    tables = database.list_tables()
    for table in tables:
        database.clear_table(table)


def before_all(context):
    load_config(context)
