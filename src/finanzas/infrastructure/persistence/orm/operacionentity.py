from datetime import datetime
from typing import Any

from sqlalchemy import Column, Date, Float, Text, Integer

from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class OperacionEntity(BaseEntity):
    __tablename__ = 'finanzas_operaciones'
    fecha = Column(Date, nullable=False)
    cantidad = Column(Float(precision=2), nullable=False)
    descripcion = Column(Text, nullable=False)
    categoria_gasto = Column(Integer, nullable=False)
    cuenta_cargo = Column(Integer, nullable=False)
    monedero_cargo = Column(Integer, nullable=False)
    categoria_ingreso = Column(Integer, nullable=False)
    cuenta_abono = Column(Integer, nullable=False)
    monedero_abono = Column(Integer, nullable=False)

    @staticmethod
    def get_column(str_property) -> Column:
        switcher = {
            "id": OperacionEntity.id,
            "fecha": OperacionEntity.fecha,
            "cantidad": OperacionEntity.cantidad,
            "descripcion": OperacionEntity.descripcion,
            "categoria_gasto": OperacionEntity.categoria_gasto,
            "cuenta_cargo": OperacionEntity.cuenta_cargo,
            "monedero_cargo": OperacionEntity.monedero_cargo,
            "categoria_ingreso": OperacionEntity.categoria_ingreso,
            "cuenta_abono": OperacionEntity.cuenta_abono,
            "monedero_abono": OperacionEntity.monedero_abono,
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
            "categoria_gasto": OperacionEntity.categoria_gasto,
            "cuenta_cargo": OperacionEntity.cuenta_cargo,
            "monedero_cargo": OperacionEntity.monedero_cargo,
            "categoria_ingreso": OperacionEntity.categoria_ingreso,
            "cuenta_abono": OperacionEntity.cuenta_abono,
            "monedero_abono": OperacionEntity.monedero_abono,
        }
        return switcher.get(str_property, OperacionEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        caster = {
            OperacionEntity.id: int,
            OperacionEntity.fecha: datetime,
            OperacionEntity.cantidad: float,
            OperacionEntity.descripcion: str,
            OperacionEntity.categoria_gasto: int,
            OperacionEntity.cuenta_cargo: int,
            OperacionEntity.monedero_cargo: int,
            OperacionEntity.categoria_ingreso: int,
            OperacionEntity.cuenta_abono: int,
            OperacionEntity.monedero_abono: int

        }
        return caster.get(column)(value)
