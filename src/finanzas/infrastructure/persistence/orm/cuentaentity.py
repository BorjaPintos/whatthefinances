from sqlalchemy import Column, Text, Float, Integer
from sqlalchemy.orm import column_property
from sqlalchemy.sql import functions
from typing_extensions import Any

from src.finanzas.domain.cuenta import Cuenta
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class CuentaEntity(BaseEntity):
    __tablename__ = 'finanzas_cuentas'
    nombre = Column(Text, nullable=False, unique=True)
    cantidad_inicial = Column(Float(precision=2), server_default="0.00", nullable=False)
    diferencia = Column(Float(precision=2), server_default="0.00", nullable=False)
    ponderacion = Column(Integer)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": CuentaEntity.id,
            "nombre": CuentaEntity.nombre,
            "cantidad_inicial": CuentaEntity.cantidad_inicial,
            "diferencia": CuentaEntity.diferencia,
            "total": (CuentaEntity.cantidad_inicial + CuentaEntity.diferencia),
            "ponderacion": CuentaEntity.ponderacion
        }
        return switcher.get(str_property, CuentaEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": CuentaEntity.id,
            "nombre": CuentaEntity.nombre
        }
        return switcher.get(str_property, CuentaEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        caster = {
            CuentaEntity.id: int,
            CuentaEntity.nombre: str,
            CuentaEntity.cantidad_inicial: float,
            CuentaEntity.diferencia: float,
            CuentaEntity.ponderacion: int

        }
        return caster.get(column)(value)

    def convert_to_object_domain(self) -> Cuenta:
        return Cuenta({"id": self.id,
                       "nombre": self.nombre,
                       "cantidad_inicial": self.cantidad_inicial,
                       "diferencia": self.diferencia,
                       "ponderacion": self.ponderacion
                       })

    def update(self, cuenta: Cuenta):
        self.nombre = cuenta.get_nombre()
        self.cantidad_inicial = cuenta.get_cantidad_inicial()
        self.diferencia = cuenta.get_diferencia()
        self.ponderacion = cuenta.get_ponderacion()
