from abc import abstractmethod
from typing import List
from sqlalchemy import inspect, MetaData, text
from sqlalchemy import create_engine, Connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from src.persistence.domain.database import Database
from src.persistence.infrastructure.orm.baseentity import BaseEntity


class SQLAlchemyDatabase(Database):

    @abstractmethod
    def _get_url(self):
        pass

    def _connect(self) -> Connection:
        url = self._get_url()
        self._engine = create_engine(url, echo=self._config.get("debug", False))
        if not database_exists(self._engine.url):
            create_database(self._engine.url)
        connection = self._engine.connect()
        self._inspect = inspect(self._engine)
        self._metadata = MetaData()
        self._session_maker = sessionmaker(bind=self._engine)
        return connection

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def list_tables(self) -> List[str]:
        return self._inspect.get_table_names()

    def describe_table(self, table_name: str) -> List[tuple]:
        result_list = []
        for column in self._inspect.get_columns(table_name):
            result_list.append((column["name"], column["type"]))
        return result_list

    def check_if_table_exist(self, table_name: str) -> bool:
        return self._inspect.has_table(table_name)

    def check_if_table_has_data(self, table_name: str) -> bool:
        result = self.exec_sql("select * from {} limit 1".format(table_name, commit=False))
        if result.first():
            return True
        else:
            return False

    def create_table(self, entity: BaseEntity) -> bool:
        self._metadata.create_all(self._engine, [entity.__table__])
        return True

    def delete_table(self, entity: BaseEntity):
        return self._metadata.drop_all(self._engine, [entity.__table__])

    def exec_sql(self, query: str, commit: bool = True):
        res = self._connection.execute(text(query))
        if commit:
            self._connection.commit()
        return res

    def new_session(self):
        return self._session_maker()
