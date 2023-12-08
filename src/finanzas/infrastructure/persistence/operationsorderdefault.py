
from abc import ABC
from sqlalchemy import asc, desc

from src.persistence.infrastructure.orderdefault import SQLAlchemyOrderDefault
from src.persistence.infrastructure.orm.baseentity import BaseEntity


class OperationsOrderDefault(SQLAlchemyOrderDefault):
    def get_default_order(self, entity: BaseEntity):
        return [desc(entity.id)]
