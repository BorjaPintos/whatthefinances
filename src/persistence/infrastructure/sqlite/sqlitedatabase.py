from sqlalchemy import Column, func

from src.persistence.infrastructure.sqlalchemydatabase import SQLAlchemyDatabase


class SQLiteDatabase(SQLAlchemyDatabase):

    def __init__(self, config: dict):
        super().__init__("sqlite", config)

    def _get_url(self):
        return """sqlite:///{0}""".format(self._config["file"])

    def year(self, colum: Column):
        return func.strftime("%Y", colum)

    def month(self, colum: Column):
        return func.strftime("%m", colum)
