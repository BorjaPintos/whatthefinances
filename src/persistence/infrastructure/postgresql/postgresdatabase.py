from sqlalchemy import Column, func

from src.persistence.infrastructure.sqlalchemydatabase import SQLAlchemyDatabase


class PostgresDatabase(SQLAlchemyDatabase):

    def __init__(self, config: dict):
        super().__init__("postgres", config)

    def _get_url(self):
        return """postgresql://{0}:{1}@{2}:{3}/{4}""".format(self._config["user"], self._config["password"],
                                                             self._config["host"], self._config["port"],
                                                             self._config["database"])

    def year(self, colum: Column):
        return func.extract("Year", colum)

    def month(self, colum: Column):
        return func.extract("Month", colum)

    def day(self, colum: Column):
        return func.extract("Day", colum)
