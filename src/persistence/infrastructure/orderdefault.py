
from abc import ABC
from sqlalchemy import asc

from src.persistence.infrastructure.orm.baseentity import BaseEntity


class SQLAlchemyOrderDefault(ABC):
    def get_default_order(self, entity: BaseEntity):
        return [asc(entity.id)]
