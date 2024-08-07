from typing import Any

from sqlalchemy import Column, Text, Float

from src.finanzas.monederos.domain.monedero import Monedero
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class MonederoEntity(BaseEntity):
    __tablename__ = 'finanzas_monederos'
    __table_args__ = {'extend_existing': True}
    nombre = Column(Text, nullable=False, unique=True)
    cantidad_inicial = Column(Float(precision=2), server_default="0.00", nullable=False)
    diferencia = Column(Float(precision=2), server_default="0.00", nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": MonederoEntity.id,
            "nombre": MonederoEntity.nombre,
            "cantidad_inicial": MonederoEntity.cantidad_inicial,
            "diferencia": MonederoEntity.diferencia,
            "total": (MonederoEntity.cantidad_inicial + MonederoEntity.diferencia),
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
        if isinstance(value, str):
            caster = {
                MonederoEntity.id: int,
                MonederoEntity.nombre: str,
                MonederoEntity.cantidad_inicial: float,
                MonederoEntity.diferencia: float

            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> Monedero:
        return Monedero({"id": self.id,
                         "nombre": self.nombre,
                         "cantidad_inicial": self.cantidad_inicial,
                         "diferencia": self.diferencia
                         })

    def update(self, monedero: Monedero):
        self.nombre = monedero.get_nombre()
        self.cantidad_inicial = monedero.get_cantidad_inicial()
        self.diferencia = monedero.get_diferencia()
