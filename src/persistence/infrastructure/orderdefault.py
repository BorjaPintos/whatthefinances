
from abc import ABC
from sqlalchemy import asc, desc

from src.persistence.infrastructure.orm.baseentity import BaseEntity


class SQLAlchemyOrderDefault(ABC):
    def get_default_order(self, entity: BaseEntity):
        return [asc(entity.id)]


class MovimientosOrderDefault(SQLAlchemyOrderDefault):
    def get_default_order(self, entity: BaseEntity):
        return [desc(entity.id)]
