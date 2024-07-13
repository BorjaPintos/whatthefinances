from typing import Any

from sqlalchemy import Column, Text, Boolean

from src.finanzas.inversion.broker.domain.broker import Broker
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class BrokerEntity(BaseEntity):
    __tablename__ = 'finanzas_brokers'
    __table_args__ = {'extend_existing': True}
    nombre = Column(Text, nullable=False, unique=True)
    extranjero = Column(Boolean, nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": BrokerEntity.id,
            "nombre": BrokerEntity.nombre,
            "extranjero": BrokerEntity.extranjero
        }
        return switcher.get(str_property, BrokerEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": BrokerEntity.id,
            "nombre": BrokerEntity.nombre,
            "extranjero": BrokerEntity.extranjero
        }
        return switcher.get(str_property, BrokerEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                BrokerEntity.id: int,
                BrokerEntity.nombre: str,
                BrokerEntity.extranjero: bool
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> Broker:
        return Broker({"id": self.id,
                       "nombre": self.nombre,
                       "extranjero": self.extranjero,
                       })

    def update(self, broker: Broker):
        self.nombre = broker.get_nombre()
        self.extranjero = broker.is_extranjero()
