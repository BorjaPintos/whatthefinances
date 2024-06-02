from sqlalchemy import Column, Text, Float, Integer, Date, Boolean
from typing_extensions import Any

from src.finanzas.domain.posicion import Posicion
from src.finanzas.infrastructure.persistence.orm.bolsaentity import BolsaEntity
from src.finanzas.infrastructure.persistence.orm.brokerentity import BrokerEntity
from src.finanzas.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class PosicionEntity(BaseEntity):
    __tablename__ = 'finanzas_posiciones'
    __table_args__ = {'extend_existing': True}
    isin = Column(Text, nullable=False)
    fecha_compra = Column(Date, nullable=False)
    fecha_venta = Column(Date, nullable=True)
    numero_participaciones = Column(Float(precision=4), nullable=False)
    id_bolsa = Column(Integer, nullable=False)
    id_broker = Column(Integer, nullable=False)
    precio_compra_sin_comision = Column(Float(precision=4), server_default="0.00", nullable=False)
    precio_venta_sin_comision = Column(Float(precision=4), server_default="0.00", nullable=True)
    comision_compra = Column(Float(precision=4), server_default="0.00", nullable=False)
    otras_comisiones = Column(Float(precision=4), server_default="0.00", nullable=False)
    comision_venta = Column(Float(precision=4), server_default="0.00", nullable=False)
    abierta = Column(Boolean, nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": PosicionEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": PosicionEntity.isin,
            "fecha_compra": PosicionEntity.fecha_compra,
            "fecha_venta": PosicionEntity.fecha_venta,
            "numero_participaciones": PosicionEntity.numero_participaciones,
            "id_bolsa": PosicionEntity.id_bolsa,
            "id_broker": PosicionEntity.id_broker,
            "nombre_bolsa": BolsaEntity.nombre,
            "nombre_broker": BrokerEntity.nombre,
            "precio_compra_sin_comision": PosicionEntity.precio_compra_sin_comision,
            "precio_venta_sin_comision": PosicionEntity.precio_venta_sin_comision,
            "comision_compra": PosicionEntity.comision_compra,
            "otras_comisiones": PosicionEntity.otras_comisiones,
            "total_comisiones": (
                    PosicionEntity.comision_compra + PosicionEntity.otras_comisiones + PosicionEntity.comision_venta),
            "total_compra_sin_comisiones": (
                    PosicionEntity.precio_compra_sin_comision * PosicionEntity.numero_participaciones),
            "total": (
                    (PosicionEntity.precio_compra_sin_comision * PosicionEntity.numero_participaciones) + (
                    PosicionEntity.comision_compra + PosicionEntity.otras_comisiones + PosicionEntity.comision_venta)),
            "comision_venta": PosicionEntity.comision_venta,
            "abierta": PosicionEntity.abierta,
        }
        return switcher.get(str_property, PosicionEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": PosicionEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": PosicionEntity.isin,
            "begin_fecha_compra": PosicionEntity.fecha_compra,
            "end_fecha_compra": PosicionEntity.fecha_compra,
            "begin_fecha_venta": PosicionEntity.fecha_venta,
            "end_fecha_venta": PosicionEntity.fecha_venta,
            "id_bolsa": PosicionEntity.id_bolsa,
            "id_broker": PosicionEntity.id_broker,
            "numero_participaciones": PosicionEntity.numero_participaciones,
            "begin_numero_participaciones": PosicionEntity.numero_participaciones,
            "end_numero_participaciones": PosicionEntity.numero_participaciones,
            "precio_compra_sin_comision": PosicionEntity.precio_compra_sin_comision,
            "begin_precio_compra_sin_comision": PosicionEntity.precio_compra_sin_comision,
            "end_precio_compra_sin_comision": PosicionEntity.precio_compra_sin_comision,
            "precio_venta_sin_comision": PosicionEntity.precio_venta_sin_comision,
            "begin_venta_sin_comision": PosicionEntity.precio_venta_sin_comision,
            "end_precio_venta_sin_comision": PosicionEntity.precio_venta_sin_comision,
            "comision_compra": PosicionEntity.comision_compra,
            "begin_comision_compra": PosicionEntity.comision_compra,
            "end_comision_compra": PosicionEntity.comision_compra,
            "otras_comisiones": PosicionEntity.otras_comisiones,
            "begin_otras_comisiones": PosicionEntity.otras_comisiones,
            "end_otras_comisiones": PosicionEntity.otras_comisiones,
            "comision_venta": PosicionEntity.comision_venta,
            "begin_comision_venta": PosicionEntity.comision_venta,
            "end_comision_venta": PosicionEntity.comision_venta,
            "abierta": PosicionEntity.abierta
        }
        return switcher.get(str_property, PosicionEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                PosicionEntity.id: int,
                ProductoEntity.nombre: str,
                PosicionEntity.isin: str,
                PosicionEntity.fecha_compra: Date,
                PosicionEntity.fecha_venta: Date,
                PosicionEntity.numero_participaciones: float,
                PosicionEntity.id_bolsa: int,
                PosicionEntity.id_broker: int,
                PosicionEntity.precio_compra_sin_comision: float,
                PosicionEntity.precio_venta_sin_comision: float,
                PosicionEntity.comision_compra: float,
                PosicionEntity.comision_venta: float,
                PosicionEntity.otras_comisiones: float,
                PosicionEntity.abierta: bool,
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> Posicion:
        return Posicion({"id": self.id,
                         "isin": self.isin,
                         "fecha_compra": self.fecha_compra,
                         "fecha_venta": self.fecha_venta,
                         "numero_participaciones": self.numero_participaciones,
                         "id_bolsa": self.id_bolsa,
                         "id_broker": self.id_broker,
                         "precio_compra_sin_comision": self.precio_compra_sin_comision,
                         "precio_venta_sin_comision": self.precio_venta_sin_comision,
                         "comision_compra": self.comision_compra,
                         "otras_comisiones": self.otras_comisiones,
                         "comision_venta": self.comision_venta,
                         "abierta": self.abierta,
                         })

    def update(self, posicion: Posicion):
        self.isin = posicion.get_isin()
        self.fecha_compra = posicion.get_fecha_compra()
        self.fecha_venta = posicion.get_fecha_venta()
        self.numero_participaciones = posicion.get_numero_participaciones()
        self.id_bolsa = posicion.get_id_bolsa()
        self.id_broker = posicion.get_id_broker()
        self.precio_compra_sin_comision = posicion.get_precio_compra_sin_comision()
        self.precio_venta_sin_comision = posicion.get_precio_venta_sin_comision()
        self.comision_compra = posicion.get_comision_compra()
        self.otras_comisiones = posicion.get_otras_comisiones()
        self.comision_venta = posicion.get_comision_venta()
        self.abierta = posicion.is_abierta()
