from typing import Any

from sqlalchemy import Column, Text
from src.finanzas.domain.producto import Producto
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class ProductoEntity(BaseEntity):
    __tablename__ = 'finanzas_productos'
    __table_args__ = {'extend_existing': True}
    nombre = Column(Text, nullable=False, unique=True)
    isin = Column(Text, nullable=False, unique=True)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": ProductoEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": ProductoEntity.isin
        }
        return switcher.get(str_property, ProductoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": ProductoEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": ProductoEntity.isin
        }
        return switcher.get(str_property, ProductoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                ProductoEntity.id: int,
                ProductoEntity.nombre: str,
                ProductoEntity.isin: str
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> Producto:
        return Producto({"id": self.id,
                       "nombre": self.nombre,
                       "isin": self.isin,
                       })

    def update(self, producto: Producto):
        self.nombre = producto.get_nombre()
        self.isin = producto.get_isin()
