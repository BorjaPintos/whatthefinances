from typing import Union, Any

from src.persistence.domain.filter import Filter
from src.persistence.domain.filtercomposite import CompositeOperator, FilterComposite


def combine_filters(filter1: Union[Filter, Any], operator: CompositeOperator, filter2: Filter) -> Filter:
    if filter1 is None:
        return filter2
    if filter2 is None:
        return filter1
    return FilterComposite(filter1, operator, filter2)
