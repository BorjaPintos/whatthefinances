import enum
from src.persistence.domain.filter import Filter, FilterType


class WhereOperator(enum.Enum):
    EQUAL = 1
    GREATER = 2
    LESS = 3
    LESSTHANOREQUAL = 4
    GREATERTHANOREQUAL = 5
    IN = 6
    LIKE = 7
    NOT = 8
    NOTEQUAL = 9
    IS = 10
    ILIKE = 11


class SimpleFilter(Filter):

    def __init__(self, key: str, operator: WhereOperator, value):
        super().__init__(FilterType.SIMPLE)
        self._key = key
        self._operator = operator
        self._value = value

    def get_key(self):
        return self._key

    def get_operator(self):
        return self._operator

    def get_value(self):
        return self._value


