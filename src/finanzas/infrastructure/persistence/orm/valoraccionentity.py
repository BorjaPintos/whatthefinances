from datetime import datetime
from typing import Any

from sqlalchemy import Column, Text, Float, DateTime

from src.finanzas.domain.valoraccion import ValorAccion
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class ValorAccionEntity(BaseEntity):
    __tablename__ = 'finanzas_valor_acciones'
    isin = Column(Text, nullable=False)
    fecha = Column(DateTime, nullable=False)
    valor = Column(Float(precision=4), server_default="0.00", nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": ValorAccionEntity.id,
            "isin": ValorAccionEntity.isin,
            "fecha": ValorAccionEntity.fecha,
            "valor": ValorAccionEntity.valor
        }
        return switcher.get(str_property, ValorAccionEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": ValorAccionEntity.id,
            "isin": ValorAccionEntity.isin,
            "begin_fecha": ValorAccionEntity.fecha,
            "end_fecha": ValorAccionEntity.fecha,
            "begin_valor": ValorAccionEntity.valor,
            "end_valor": ValorAccionEntity.valor
        }
        return switcher.get(str_property, ValorAccionEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                ValorAccionEntity.id: int,
                ValorAccionEntity.isin: str,
                ValorAccionEntity.fecha: datetime,
                ValorAccionEntity.valor: float,
            }
            return caster.get(column)(value)
        return value

    def convert_to_object_domain(self) -> ValorAccion:
        return ValorAccion({"id": self.id,
                            "isin": self.isin,
                            "fecha": self.fecha,
                            "valor": self.valor
                            })
