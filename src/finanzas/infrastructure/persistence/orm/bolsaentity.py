from typing import Any

from sqlalchemy import Column, Text

from src.finanzas.domain.bolsa import Bolsa
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class BolsaEntity(BaseEntity):
    __tablename__ = 'finanzas_bolsas'
    nombre = Column(Text, nullable=False, unique=True)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": BolsaEntity.id,
            "nombre": BolsaEntity.nombre,
        }
        return switcher.get(str_property, BolsaEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": BolsaEntity.id,
            "nombre": BolsaEntity.nombre
        }
        return switcher.get(str_property, BolsaEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                BolsaEntity.id: int,
                BolsaEntity.nombre: str,
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> Bolsa:
        return Bolsa({"id": self.id,
                      "nombre": self.nombre,
                      })

    def update(self, bolsa: Bolsa):
        self.nombre = bolsa.get_nombre()
