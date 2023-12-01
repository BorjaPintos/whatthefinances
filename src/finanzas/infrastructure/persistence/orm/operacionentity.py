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
    id_categoria_gasto = Column(Integer, nullable=False)
    id_cuenta_cargo = Column(Integer, nullable=False)
    id_monedero_cargo = Column(Integer, nullable=False)
    id_categoria_ingreso = Column(Integer, nullable=False)
    id_cuenta_abono = Column(Integer, nullable=False)
    id_monedero_abono = Column(Integer, nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": OperacionEntity.id,
            "fecha": OperacionEntity.fecha,
            "cantidad": OperacionEntity.cantidad,
            "descripcion": OperacionEntity.descripcion
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
        caster = {
            OperacionEntity.id: int,
            OperacionEntity.fecha: datetime,
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

    def update(self, params: dict):
        self.fecha = params.get("fecha"),
        self.cantidad = params.get("cantidad"),
        self.descripcion = params.get("descripcion"),
        self.id_categoria_gasto = params.get("id_categoria_gasto"),
        self.id_categoria_ingreso = params.get("id_categoria_ingreso"),
        self.id_cuenta_cargo = params.get("id_cuenta_cargo"),
        self.id_cuenta_abono = params.get("id_cuenta_abono"),
        self.id_monedero_cargo = params.get("id_monedero_cargo"),
        self.id_monedero_abono = params.get("id_monedero_abono")
