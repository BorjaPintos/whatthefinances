from datetime import datetime, date
from typing import Any

from sqlalchemy import Column, Date, Float, Text, Integer

from src.finanzas.domain.operacion import Operacion
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class OperacionEntity(BaseEntity):
    __tablename__ = 'finanzas_operaciones'
    __table_args__ = {'extend_existing': True}
    fecha = Column(Date, nullable=False)
    cantidad = Column(Float(precision=2), nullable=False)
    descripcion = Column(Text, nullable=False)
    id_categoria_gasto = Column(Integer)
    id_cuenta_cargo = Column(Integer)
    id_monedero_cargo = Column(Integer)
    id_categoria_ingreso = Column(Integer)
    id_cuenta_abono = Column(Integer)
    id_monedero_abono = Column(Integer)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": OperacionEntity.id,
            "fecha": OperacionEntity.fecha,
            "cantidad": OperacionEntity.cantidad,
        }
        return switcher.get(str_property, OperacionEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": OperacionEntity.id,
            "begin_fecha": OperacionEntity.fecha,
            "end_fecha": OperacionEntity.fecha,
            "begin_cantidad": OperacionEntity.cantidad,
            "end_cantidad": OperacionEntity.cantidad,
            "descripcion": OperacionEntity.descripcion,
            "id_categoria_gasto": OperacionEntity.id_categoria_gasto,
            "id_cuenta_cargo": OperacionEntity.id_cuenta_cargo,
            "id_monedero_cargo": OperacionEntity.id_monedero_cargo,
            "id_categoria_ingreso": OperacionEntity.id_categoria_ingreso,
            "id_cuenta_abono": OperacionEntity.id_cuenta_abono,
            "id_monedero_abono": OperacionEntity.id_monedero_abono,
        }
        return switcher.get(str_property, OperacionEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                OperacionEntity.id: int,
                OperacionEntity.fecha: date,
                OperacionEntity.cantidad: float,
                OperacionEntity.descripcion: str,
                OperacionEntity.id_categoria_gasto: int,
                OperacionEntity.id_cuenta_cargo: int,
                OperacionEntity.id_monedero_cargo: int,
                OperacionEntity.id_categoria_ingreso: int,
                OperacionEntity.id_cuenta_abono: int,
                OperacionEntity.id_monedero_abono: int
            }
            return caster.get(column)(value)
        else:
            return value

    def update(self, operacion: Operacion):
        self.fecha = operacion.get_fecha()
        self.cantidad = operacion.get_cantidad()
        self.descripcion = operacion.get_descripcion()
        self.id_categoria_gasto = operacion.get_id_categoria_gasto()
        self.id_categoria_ingreso = operacion.get_id_categoria_ingreso()
        self.id_cuenta_cargo = operacion.get_id_cuenta_cargo()
        self.id_cuenta_abono = operacion.get_id_cuenta_abono()
        self.id_monedero_cargo = operacion.get_id_monedero_cargo()
        self.id_monedero_abono = operacion.get_id_monedero_abono()
