from typing import Any

from sqlalchemy import Column, Text, Integer

from src.finanzas.inversion.producto.domain.plataformaproductoenum import PlataformaProductoEnum
from src.finanzas.inversion.producto.domain.producto import Producto
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class ProductoEntity(BaseEntity):
    __tablename__ = 'finanzas_productos'
    __table_args__ = {'extend_existing': True}
    nombre = Column(Text, nullable=False, unique=True)
    isin = Column(Text, nullable=False, unique=True)
    plataforma = Column(Integer)
    url = Column(Text)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": ProductoEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": ProductoEntity.isin,
            "plataforma": ProductoEntity.plataforma,
            "url": ProductoEntity.url
        }
        return switcher.get(str_property, ProductoEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": ProductoEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": ProductoEntity.isin,
            "plataforma": ProductoEntity.plataforma,
            "url": ProductoEntity.url
        }
        return switcher.get(str_property, ProductoEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                ProductoEntity.id: int,
                ProductoEntity.nombre: str,
                ProductoEntity.isin: str,
                ProductoEntity.plataforma: int,
                ProductoEntity.url: str
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> Producto:
        return Producto({"id": self.id,
                         "nombre": self.nombre,
                         "isin": self.isin,
                         "plataforma": PlataformaProductoEnum.get_enum_from_value(self.plataforma),
                         "url": self.url
                         })

    def update(self, producto: Producto):
        self.nombre = producto.get_nombre()
        self.isin = producto.get_isin()
        self.url = producto.get_url()
        self.plataforma = producto.get_plataforma().value if producto.get_plataforma() is not None else None
