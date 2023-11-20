from abc import ABC
import enum


class FilterType(enum.Enum):
    SIMPLE = 1
    COMPOSITE = 2


class Filter(ABC):

    def __init__(self, filter_type: FilterType):
        self._type = filter_type

    def get_type(self) -> FilterType:
        return self._type
