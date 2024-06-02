from typing import Any

from sqlalchemy import Column,  Float, Text, Integer

from src.finanzas.domain.operacionFavorita import OperacionFavorita
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class OperacionFavoritaEntity(BaseEntity):
    __tablename__ = 'finanzas_operaciones_favoritas'
    __table_args__ = {'extend_existing': True}
    nombre = Column(Text, nullable=False, unique=True)
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
            "id": OperacionFavoritaEntity.id,
            "nombre": OperacionFavoritaEntity.nombre
        }
        return switcher.get(str_property, OperacionFavoritaEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": OperacionFavoritaEntity.id,
            "nombre": OperacionFavoritaEntity.nombre,
        }
        return switcher.get(str_property, OperacionFavoritaEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                OperacionFavoritaEntity.id: int,
                OperacionFavoritaEntity.nombre: str,
                OperacionFavoritaEntity.cantidad: float,
                OperacionFavoritaEntity.descripcion: str,
                OperacionFavoritaEntity.id_categoria_gasto: int,
                OperacionFavoritaEntity.id_cuenta_cargo: int,
                OperacionFavoritaEntity.id_monedero_cargo: int,
                OperacionFavoritaEntity.id_categoria_ingreso: int,
                OperacionFavoritaEntity.id_cuenta_abono: int,
                OperacionFavoritaEntity.id_monedero_abono: int
            }
            return caster.get(column)(value)
        else:
            return value

    def update(self, operacion_favorita: OperacionFavorita):
        self.nombre = operacion_favorita.get_nombre()
        self.cantidad = operacion_favorita.get_cantidad()
        self.descripcion = operacion_favorita.get_descripcion()
        self.id_categoria_gasto = operacion_favorita.get_id_categoria_gasto()
        self.id_categoria_ingreso = operacion_favorita.get_id_categoria_ingreso()
        self.id_cuenta_cargo = operacion_favorita.get_id_cuenta_cargo()
        self.id_cuenta_abono = operacion_favorita.get_id_cuenta_abono()
        self.id_monedero_cargo = operacion_favorita.get_id_monedero_cargo()
        self.id_monedero_abono = operacion_favorita.get_id_monedero_abono()