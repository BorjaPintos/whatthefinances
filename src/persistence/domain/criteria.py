from abc import ABC
from enum import Enum
from typing import Union

from src.persistence.domain.filter import Filter


class OrderBy(ABC):
    def __init__(self, field_name: str):
        self.__field_name = field_name

    def field_name(self):
        return self.__field_name


class OrderType(Enum):

    ASC = "asc"
    DESC = "desc"


class Order(ABC):

    def __init__(self, order_by: OrderBy, order_type: OrderType):
        self.__order_type = order_type
        self.__order_by = order_by

    def order_by(self) -> OrderBy:
        return self.__order_by

    def order_type(self) -> OrderType:
        return self.__order_type


class Criteria(ABC):
    def __init__(self, order: Union[Order, None] = None, offset: int = 0, limit: int = 10,
                 filter: Union[Filter, None] = None):
        if offset < 0:
            raise ValueError("offset must be greater or equal than 0")

        self.__order = order
        self.__offset = offset
        self.__limit = limit
        self.__filter = filter

    def order(self) -> Union[Order, None]:
        return self.__order

    def offset(self):
        return self.__offset

    def limit(self):
        return self.__limit

    def filter(self):
        return self.__filter
