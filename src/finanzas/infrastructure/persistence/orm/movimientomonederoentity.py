from datetime import date

from sqlalchemy import Column, Float, Integer
from typing_extensions import Any

from src.finanzas.domain.cuenta import Cuenta
from src.finanzas.domain.movimientomonedero import MovimientoMonedero
from src.finanzas.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class MovimientoMonederoEntity(BaseEntity):
    __tablename__ = 'finanzas_movimientos_monederos'
    __table_args__ = {'extend_existing': True}
    id_operacion = Column(Integer, nullable=False)
    id_monedero = Column(Integer, nullable=False)
    cantidad = Column(Float(precision=2), nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": MovimientoMonederoEntity.id,
            "fecha": OperacionEntity.fecha,
            "id_operacion": MovimientoMonederoEntity.id_operacion,
            "id_cuenta": MovimientoMonederoEntity.id_monedero,
            "cantidad": MovimientoMonederoEntity.cantidad
        }
        return switcher.get(str_property, MovimientoMonederoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": MovimientoMonederoEntity.id,
            "begin_fecha": OperacionEntity.fecha,
            "end_fecha": OperacionEntity.fecha,
            "id_operacion": MovimientoMonederoEntity.id_operacion,
            "id_monedero": MovimientoMonederoEntity.id_monedero,
            "cantidad": MovimientoMonederoEntity.cantidad
        }
        return switcher.get(str_property, MovimientoMonederoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                MovimientoMonederoEntity.id: int,
                OperacionEntity.fecha: date,
                MovimientoMonederoEntity.id_operacion: int,
                MovimientoMonederoEntity.id_monedero: int,
                MovimientoMonederoEntity.cantidad: float

            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> MovimientoMonedero:
        return MovimientoMonedero({"id": self.id,
                                   "id_operacion": self.id_operacion,
                                   "id_monedero": self.id_monedero,
                                   "cantidad": self.cantidad,
                                   })
