from sqlalchemy import Column, Text, Float, Integer
from sqlalchemy.orm import column_property
from typing_extensions import Any

from src.finanzas.domain.cuenta import Cuenta
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class CuentaEntity(BaseEntity):
    __tablename__ = 'finanzas_cuentas'
    nombre = Column(Text, nullable=False, unique=True)
    cantidad_base = Column(Float(precision=2), nullable=False)
    diferencia = Column(Float(precision=2), server_default="0.00", nullable=False)
    total = column_property(cantidad_base + diferencia)
    ponderacion = Column(Integer)

    @staticmethod
    def get_column(str_property) -> Column:
        switcher = {
            "id": CuentaEntity.id,
            "nombre": CuentaEntity.nombre,
            "cantidad_base": CuentaEntity.cantidad_base,
            "diferencia": CuentaEntity.diferencia,
            "total": CuentaEntity.total,
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
            CuentaEntity.cantidad_base: float,
            CuentaEntity.diferencia: float,
            CuentaEntity.total: float,
            CuentaEntity.ponderacion: int

        }
        return caster.get(column)(value)

    def convert_to_object_domain(self) -> Cuenta:
        return Cuenta({"id": self.id,
                       "nombre": self.nombre,
                       "cantidad_base": self.cantidad_base,
                       "diferencia": self.diferencia,
                       "total": self.total,
                       "ponderacion": self.ponderacion
                       })

    def update(self, params: dict):
        if params["nombre"]:
            self.nombre = params["nombre"]
        if params["cantidad_base"]:
            self.cantidad_base = params["cantidad_base"]
        if params["ponderacion"]:
            self.ponderacion = params["ponderacion"]
