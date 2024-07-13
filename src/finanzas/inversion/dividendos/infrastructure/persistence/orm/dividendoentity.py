from datetime import date
from typing import Any

from sqlalchemy import Column, Date, Float, Text

from src.finanzas.inversion.dividendos.domain.dividendo import Dividendo
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class DividendoEntity(BaseEntity):
    __tablename__ = 'finanzas_dividendos'
    __table_args__ = {'extend_existing': True}
    fecha = Column(Date, nullable=False)
    isin = Column(Text, nullable=False)
    dividendo_por_participacion = Column(Float(precision=2), nullable=False)
    retencion_por_participacion = Column(Float(precision=2), nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": DividendoEntity.id,
            "fecha": DividendoEntity.fecha,
            "isin": DividendoEntity.isin,
            "dividendo_por_participacion": DividendoEntity.dividendo_por_participacion,
            "retencion_por_participacion": DividendoEntity.retencion_por_participacion
        }
        return switcher.get(str_property, DividendoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": DividendoEntity.id,
            "begin_fecha": DividendoEntity.fecha,
            "end_fecha": DividendoEntity.fecha,
            "isin": DividendoEntity.isin
        }
        return switcher.get(str_property, DividendoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                DividendoEntity.id: int,
                DividendoEntity.fecha: date,
                DividendoEntity.isin: str,
                DividendoEntity.dividendo_por_participacion: float,
                DividendoEntity.retencion_por_participacion: float
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> Dividendo:
        return Dividendo({"id": self.id,
                          "isin": self.isin,
                          "fecha": self.fecha,
                          "dividendo_por_participacion": self.dividendo_por_participacion,
                          "retencion_por_participacion": self.retencion_por_participacion})

    def update(self, dividendo: Dividendo):
        self.fecha = dividendo.get_fecha()
        self.isin = dividendo.get_isin()
        self.dividendo_por_participacion = dividendo.get_dividendo_por_participacion()
        self.retencion_por_participacion = dividendo.get_retencion_por_participacion()
