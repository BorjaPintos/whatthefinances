from src.persistence.infrastructure.sqlalchemydatabase import SQLAlchemyDatabase


class PostgresDatabase(SQLAlchemyDatabase):

    def __init__(self, config: dict):
        super().__init__("postgres", config)

    def _get_url(self):
        return """postgresql://{0}:{1}@{2}:{3}/{4}""".format(self._config["user"], self._config["password"],
                                                             self._config["host"], self._config["port"],
                                                             self._config["database"])
