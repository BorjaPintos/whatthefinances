from datetime import date

from sqlalchemy import Column, Float, Integer
from typing_extensions import Any

from src.finanzas.domain.cuenta import Cuenta
from src.finanzas.domain.movimientocuenta import MovimientoCuenta
from src.finanzas.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class MovimientoCuentaEntity(BaseEntity):
    __tablename__ = 'finanzas_movimientos_cuentas'
    id_operacion = Column(Integer, nullable=False)
    id_cuenta = Column(Integer, nullable=False)
    cantidad = Column(Float(precision=2), nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": MovimientoCuentaEntity.id,
            "fecha": OperacionEntity.fecha,
            "id_operacion": MovimientoCuentaEntity.id_operacion,
            "id_cuenta": MovimientoCuentaEntity.id_cuenta,
            "cantidad": MovimientoCuentaEntity.cantidad
        }
        return switcher.get(str_property, MovimientoCuentaEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": MovimientoCuentaEntity.id,
            "fecha": OperacionEntity.fecha,
            "id_operacion": MovimientoCuentaEntity.id_operacion,
            "id_cuenta": MovimientoCuentaEntity.id_cuenta,
            "cantidad": MovimientoCuentaEntity.cantidad
        }
        return switcher.get(str_property, MovimientoCuentaEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                MovimientoCuentaEntity.id: int,
                OperacionEntity.fecha: date,
                MovimientoCuentaEntity.id_operacion: int,
                MovimientoCuentaEntity.id_cuenta: int,
                MovimientoCuentaEntity.cantidad: float

            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> MovimientoCuenta:
        return MovimientoCuenta({"id": self.id,
                       "id_operacion": self.id_operacion,
                       "id_cuenta": self.id_cuenta,
                       "cantidad": self.cantidad,
                       })
