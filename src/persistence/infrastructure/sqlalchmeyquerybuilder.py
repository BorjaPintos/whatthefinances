from typing import Tuple, Any, Union

from sqlalchemy import desc, asc, or_, and_, not_, func, Text
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import BooleanClauseList

from src.persistence.domain.criteria import Criteria, OrderType
from src.persistence.domain.filtercomposite import CompositeOperator, FilterComposite
from src.persistence.domain.simplefilter import WhereOperator, SimpleFilter
from src.persistence.infrastructure.orderdefault import SQLAlchemyOrderDefault
from src.persistence.infrastructure.sqlalchemysession import SQLAlchmeySession


class SQLAlchemyQueryBuilder:
    """The class SQLAlchemyQueryBuilder."""

    SQL_FUNCTION_MAP = {
        CompositeOperator.AND:
            and_,
        CompositeOperator.OR:
            or_,
        WhereOperator.EQUAL:
            lambda a, b: a == b,
        WhereOperator.NOTEQUAL:
            lambda a, b: a != b,
        WhereOperator.GREATER:
            lambda a, b: a > b,
        WhereOperator.GREATERTHANOREQUAL:
            lambda a, b: a >= b,
        WhereOperator.IN:
            lambda a, b: a.in_(b),
        WhereOperator.LESS:
            lambda a, b: a < b,
        WhereOperator.LESSTHANOREQUAL:
            lambda a, b: a <= b,
        WhereOperator.LIKE:
            lambda a, b: a.like(b),
        WhereOperator.NOT:
            lambda a, b: a.not_(b),
        WhereOperator.IS:
            lambda a, b: a == b,
        WhereOperator.ILIKE:
            lambda a, b: a.ilike(b)
    }

    def __init__(self, entity_class, session: SQLAlchmeySession, selected_columns: Tuple = None):
        self.__session = session
        self.__entity_class = entity_class
        self.__selected_columns = selected_columns

    def build_base_query(self) -> Query:
        """Build simple query."""

        if self.__selected_columns is None:
            return self.__session.query(self.__entity_class)
        else:
            return self.__session.query(*self.__selected_columns)

    def build_query(self, criteria: Criteria) -> Query:
        """Build filter query."""
        query = self.build_base_query()
        if criteria.filter() is not None:
            condition = self._get_conditions(criteria.filter())
            if condition is not None:
                query = query.filter(condition)
        return query

    def build_query_cte(self, select_from, criteria: Criteria) -> Query:
        query = self.build_base_query().select_from(select_from)
        condition = self._get_conditions(criteria.filter())
        if condition is not None:
            query = query.filter(condition)
        return query

    def _get_conditions(self, filter: SimpleFilter) -> Union[BooleanClauseList, Any]:
        function = SQLAlchemyQueryBuilder.SQL_FUNCTION_MAP.get(filter.get_operator())
        if function is None:
            return None

        if isinstance(filter, SimpleFilter):
            if filter.get_value() is not None:
                entity = self.__entity_class
                property = entity.get_filter_column(filter.get_key())
                value = entity.cast_to_column_type(
                    column=property,
                    value=filter.get_value()
                )
                return and_(function(property, value))
            else:
                if filter.get_operator() == WhereOperator.NOT or filter.get_operator() == WhereOperator.IS:
                    entity = self.__entity_class
                    property = entity.get_filter_column(filter.get_key())
                    value = None
                    return and_(function(property, value))

        if isinstance(filter, FilterComposite):
            condition_left = self._get_conditions(filter.get_left())
            condition_right = self._get_conditions(filter.get_right())
            if condition_left is not None:
                if condition_right is not None:
                    return function(condition_left, condition_right)
                return condition_left
            if condition_right is not None:
                return condition_right

        return None

    def build_order_query(self, criteria: Criteria,
                          defaultOrder: SQLAlchemyOrderDefault = SQLAlchemyOrderDefault()) -> Query:
        """Build the query."""
        query = self.build_query(criteria)
        order_by_clauses = self.__get_order_by_clauses(criteria, defaultOrder)
        query = query.order_by(*order_by_clauses)
        return query


    def __get_order_by_clauses(self, criteria: Criteria, defaultOrder: SQLAlchemyOrderDefault):
        if criteria.order() is None:
            return defaultOrder.get_default_order(self.__entity_class)

        order = self.__order_func_from_order_type(
            criteria.order().order_type())
        column_order = self.__entity_class.get_order_column(criteria.order().order_by().field_name())
        order_list = []
        if isinstance(column_order.type, Text):
            order_list.append(
                order(func.upper(self.__entity_class.get_order_column(criteria.order().order_by().field_name()))))
        else:
            order_list.append(order(self.__entity_class.get_order_column(criteria.order().order_by().field_name())))

        order_list.extend(defaultOrder.get_default_order(self.__entity_class))
        return order_list

    @staticmethod
    def __order_func_from_order_type(order_type: OrderType):
        if order_type == OrderType.DESC:
            return desc
        else:
            return asc
