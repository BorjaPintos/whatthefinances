from typing import Any

from sqlalchemy import Column, Text, Integer, Float
from sqlalchemy.orm import column_property

from src.finanzas.domain.monedero import Monedero
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class MonederoEntity(BaseEntity):
    __tablename__ = 'finanzas_monederos'
    nombre = Column(Text, nullable=False)
    cantidad_base = Column(Float(precision=2), nullable=False)
    diferencia = Column(Float(precision=2), server_default="0.00", nullable=False)
    total = column_property(cantidad_base + diferencia)

    @staticmethod
    def get_column(str_property) -> Column:
        switcher = {
            "id": MonederoEntity.id,
            "nombre": MonederoEntity.nombre,
            "cantidad_base": MonederoEntity.cantidad_base,
            "diferencia": MonederoEntity.diferencia,
            "total": MonederoEntity.total,
        }
        return switcher.get(str_property, MonederoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": MonederoEntity.id,
            "nombre": MonederoEntity.nombre
        }
        return switcher.get(str_property, MonederoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        caster = {
            MonederoEntity.id: int,
            MonederoEntity.nombre: str,
            MonederoEntity.cantidad_base: float,
            MonederoEntity.diferencia: float,
            MonederoEntity.total: float

        }
        return caster.get(column)(value)

    def convert_to_object_domain(self) -> Monedero:
        return Monedero({"id": self.id,
                         "nombre": self.nombre,
                         "cantidad_base": self.cantidad_base,
                         "diferencia": self.diferencia,
                         "total": self.total
                         })
