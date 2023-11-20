import enum

from src.persistence.domain.filter import Filter, FilterType


class CompositeOperator(enum.Enum):
    AND = 1
    OR = 2


class FilterComposite(Filter):

    def __init__(self, left: Filter, operator: CompositeOperator, right: Filter):
        super().__init__(FilterType.COMPOSITE)
        self._left = left
        self._operator = operator
        self._right = right

    def get_left(self):
        return self._left

    def get_operator(self):
        return self._operator

    def get_right(self):
        return self._right
