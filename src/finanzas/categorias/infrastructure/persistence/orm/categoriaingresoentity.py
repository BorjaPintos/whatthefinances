from typing import Any

from sqlalchemy import Column, Text, Integer

from src.finanzas.categorias.domain.categoriaingreso import CategoriaIngreso
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class CategoriaIngresoEntity(BaseEntity):
    __tablename__ = 'finanzas_categorias_ingreso'
    __table_args__ = {'extend_existing': True}
    descripcion = Column(Text, nullable=False, unique=True)
    id_cuenta_abono_defecto = Column(Integer)
    id_monedero_defecto = Column(Integer)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": CategoriaIngresoEntity.id,
            "descripcion": CategoriaIngresoEntity.descripcion,
            "id_cuenta_abono_defecto": CategoriaIngresoEntity.id_cuenta_abono_defecto,
            "id_monedero_defecto": CategoriaIngresoEntity.id_monedero_defecto,
        }
        return switcher.get(str_property, CategoriaIngresoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": CategoriaIngresoEntity.id,
            "descripcion": CategoriaIngresoEntity.descripcion,
            "id_cuenta_abono_defecto": CategoriaIngresoEntity.id_cuenta_abono_defecto,
            "id_monedero_defecto": CategoriaIngresoEntity.id_monedero_defecto,
        }
        return switcher.get(str_property, CategoriaIngresoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                CategoriaIngresoEntity.id: int,
                CategoriaIngresoEntity.descripcion: str,
                CategoriaIngresoEntity.id_cuenta_abono_defecto: int,
                CategoriaIngresoEntity.id_monedero_defecto: int,

            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> CategoriaIngreso:
        return CategoriaIngreso({"id": self.id,
                                 "descripcion": self.descripcion,
                                 "id_cuenta_abono_defecto": self.id_cuenta_abono_defecto,
                                 "id_monedero_defecto": self.id_monedero_defecto,
                                 })

    def update(self, categoria_ingreso: CategoriaIngreso):
        self.descripcion = categoria_ingreso.get_descripcion()
        self.id_cuenta_abono_defecto = categoria_ingreso.get_id_cuenta_abono_defecto()
        self.id_monedero_defecto = categoria_ingreso.get_id_monedero_defecto()
