from datetime import datetime
from typing import Any

from sqlalchemy import Column, Text, Float, DateTime

from src.finanzas.inversion.valorparticipacion.domain.valorparticipacion import ValorParticipacion
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class ValorParticipacionEntity(BaseEntity):
    __tablename__ = 'finanzas_valor_participaciones'
    __table_args__ = {'extend_existing': True}
    isin = Column(Text, nullable=False)
    fecha = Column(DateTime, nullable=False)
    valor = Column(Float(precision=4), server_default="0.00", nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": ValorParticipacionEntity.id,
            "isin": ValorParticipacionEntity.isin,
            "fecha": ValorParticipacionEntity.fecha,
            "valor": ValorParticipacionEntity.valor
        }
        return switcher.get(str_property, ValorParticipacionEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": ValorParticipacionEntity.id,
            "isin": ValorParticipacionEntity.isin,
            "begin_fecha": ValorParticipacionEntity.fecha,
            "end_fecha": ValorParticipacionEntity.fecha,
            "begin_valor": ValorParticipacionEntity.valor,
            "end_valor": ValorParticipacionEntity.valor
        }
        return switcher.get(str_property, ValorParticipacionEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                ValorParticipacionEntity.id: int,
                ValorParticipacionEntity.isin: str,
                ValorParticipacionEntity.fecha: datetime,
                ValorParticipacionEntity.valor: float,
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> ValorParticipacion:
        return ValorParticipacion({"id": self.id,
                            "isin": self.isin,
                            "fecha": self.fecha,
                            "valor": self.valor
                                   })
