from typing import Any

from sqlalchemy import Column, Text, Integer

from src.finanzas.domain.categoriaingreso import CategoriaIngreso
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class CategoriaIngresoEntity(BaseEntity):
    __tablename__ = 'finanzas_categorias_ingreso'
    descripcion = Column(Text, nullable=False)
    cuenta_abono_defecto = Column(Integer)
    monedero_defecto = Column(Integer)

    @staticmethod
    def get_column(str_property) -> Column:
        switcher = {
            "id": CategoriaIngresoEntity.id,
            "descripcion": CategoriaIngresoEntity.descripcion,
            "id_cuenta_abono_defecto": CategoriaIngresoEntity.cuenta_abono_defecto,
            "id_monedero_defecto": CategoriaIngresoEntity.monedero_defecto,
        }
        return switcher.get(str_property, CategoriaIngresoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": CategoriaIngresoEntity.id,
            "descripcion": CategoriaIngresoEntity.descripcion,
            "id_cuenta_abono_defecto": CategoriaIngresoEntity.cuenta_abono_defecto,
            "id_monedero_defecto": CategoriaIngresoEntity.monedero_defecto,
        }
        return switcher.get(str_property, CategoriaIngresoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        caster = {
            CategoriaIngresoEntity.id: int,
            CategoriaIngresoEntity.descripcion: str,
            CategoriaIngresoEntity.cuenta_abono_defecto: int,
            CategoriaIngresoEntity.monedero_defecto: int,

        }
        return caster.get(column)(value)

