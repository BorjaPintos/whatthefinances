from abc import abstractmethod

from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase
from typing_extensions import Any


class BaseEntity(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)

    @staticmethod
    @abstractmethod
    def get_order_column(str_property: str) -> Column:
        pass

    @staticmethod
    @abstractmethod
    def get_filter_column(str_property: str) -> Column:
        pass

    @staticmethod
    @abstractmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        pass
