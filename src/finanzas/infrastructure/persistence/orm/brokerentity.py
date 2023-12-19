from typing import Any

from sqlalchemy import Column, Text

from src.finanzas.domain.broker import Broker
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class BrokerEntity(BaseEntity):
    __tablename__ = 'finanzas_brokers'
    nombre = Column(Text, nullable=False, unique=True)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": BrokerEntity.id,
            "nombre": BrokerEntity.nombre,
        }
        return switcher.get(str_property, BrokerEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": BrokerEntity.id,
            "nombre": BrokerEntity.nombre
        }
        return switcher.get(str_property, BrokerEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        caster = {
            BrokerEntity.id: int,
            BrokerEntity.nombre: str,
        }
        return caster.get(column)(value)

    def convert_to_object_domain(self) -> Broker:
        return Broker({"id": self.id,
                       "nombre": self.nombre,
                       })

    def update(self, broker: Broker):
        self.nombre = broker.get_nombre()
