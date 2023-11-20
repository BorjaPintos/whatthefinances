from typing import Any

from sqlalchemy import Column, Text, Integer

from src.finanzas.domain.categoriagasto import CategoriaGasto
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class CategoriaGastoEntity(BaseEntity):
    __tablename__ = 'finanzas_categorias_gasto'

    descripcion = Column(Text, nullable=False)
    cuenta_cargo_defecto = Column(Integer)
    monedero_defecto = Column(Integer)

    @staticmethod
    def get_column(str_property) -> Column:
        switcher = {
            "id": CategoriaGastoEntity.id,
            "descripcion": CategoriaGastoEntity.descripcion,
            "id_cuenta_cargo_defecto": CategoriaGastoEntity.cuenta_cargo_defecto,
            "id_monedero_defecto": CategoriaGastoEntity.monedero_defecto,
        }
        return switcher.get(str_property, CategoriaGastoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": CategoriaGastoEntity.id,
            "descripcion": CategoriaGastoEntity.descripcion,
            "id_cuenta_cargo_defecto": CategoriaGastoEntity.cuenta_cargo_defecto,
            "id_monedero_defecto": CategoriaGastoEntity.monedero_defecto,
        }
        return switcher.get(str_property, CategoriaGastoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        caster = {
            CategoriaGastoEntity.id: int,
            CategoriaGastoEntity.descripcion: str,
            CategoriaGastoEntity.cuenta_cargo_defecto: int,
            CategoriaGastoEntity.monedero_defecto: int,

        }
        return caster.get(column)(value)

    def convert_to_object_domain(self) -> CategoriaGasto:
        return CategoriaGasto({"id": self.id,
                               "descripcion": self.descripcion,
                               "id_cuenta_cargo_defecto": self.cuenta_cargo_defecto,
                               "id_monedero_defecto": self.monedero_defecto
                               })
