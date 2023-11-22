from typing import List
from unittest.mock import Mock
from sqlalchemy import Connection
from src.persistence.domain.database import Database
from src.persistence.infrastructure.orm.baseentity import BaseEntity


class MockDatabase(Database):

    def __init__(self, config: dict):
        super().__init__("Mock", config)

    def _connect(self, ) -> Connection:
        return Mock()

    def commit(self):
        pass

    def rollback(self):
        pass

    def list_tables(self) -> List[str]:
        pass

    def describe_table(self, table_name: str) -> List[tuple]:
        pass

    def check_if_table_exist(self, table_name: str) -> bool:
        pass

    def check_if_table_has_data(self, table_name: str) -> bool:
        pass

    def create_table(self, entity: BaseEntity) -> bool:
        return True

    def delete_table(self, entity: BaseEntity):
        return None

    def clear_table(self, table_name: str):
        pass

    def exec_sql(self, query: str, commit: bool = True):
        pass

    def new_session(self):
        return Mock()
