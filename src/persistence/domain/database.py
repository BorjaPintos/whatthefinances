from abc import abstractmethod
from typing import List

from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeMeta

from src.persistence.infrastructure.orm.baseentity import BaseEntity


class Database:

    def __init__(self, database_type: str, config: dict):
        self._config = config
        self._database_type = database_type
        self._connection = self._connect()

    @abstractmethod
    def _connect(self) -> object:
        pass

    def get_database_type(self) -> str:
        return self._database_type

    def get_connection(self) -> object:
        return self._connection

    @abstractmethod
    def list_tables(self) -> List[str]:
        pass

    @abstractmethod
    def delete_table(self, entity: BaseEntity):
        pass

    @abstractmethod
    def clear_table(self, table_name: str):
        pass

    @abstractmethod
    def describe_table(self, table_name: str) -> List[tuple]:
        """devuelve (nombre,tipo)"""
        pass

    @abstractmethod
    def check_if_table_exist(self, table_name: str) -> bool:
        pass

    @abstractmethod
    def check_if_table_has_data(self, table_name: str) -> bool:
        pass

    @abstractmethod
    def create_table(self, entity: DeclarativeMeta) -> bool:
        pass

    @abstractmethod
    def exec_sql(self, query: str, commit: bool = True):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


    @abstractmethod
    def new_session(self):
        pass

    @abstractmethod
    def year(self, colum: Column):
        pass

    @abstractmethod
    def month(self, colum: Column):
        pass

    @abstractmethod
    def day(self, colum: Column):
        pass