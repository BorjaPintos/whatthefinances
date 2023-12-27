from sqlalchemy import Column, Text, Float, Integer, Date, Boolean
from typing_extensions import Any

from src.finanzas.domain.cuenta import Cuenta
from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.infrastructure.persistence.orm.bolsaentity import BolsaEntity
from src.finanzas.infrastructure.persistence.orm.brokerentity import BrokerEntity
from src.finanzas.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class PosicionAccionEntity(BaseEntity):
    __tablename__ = 'finanzas_posiciones_acciones'
    isin = Column(Text, nullable=False)
    fecha_compra = Column(Date, nullable=False)
    fecha_venta = Column(Date, nullable=True)
    numero_acciones = Column(Integer, nullable=False)
    id_bolsa = Column(Integer, nullable=False)
    id_broker = Column(Integer, nullable=False)
    precio_accion_sin_comision = Column(Float(precision=4), server_default="0.00", nullable=False)
    precio_venta_sin_comision = Column(Float(precision=4), server_default="0.00", nullable=True)
    comision_compra = Column(Float(precision=4), server_default="0.00", nullable=False)
    otras_comisiones = Column(Float(precision=4), server_default="0.00", nullable=False)
    comision_venta = Column(Float(precision=4), server_default="0.00", nullable=False)
    abierta = Column(Boolean, nullable=False)

    @staticmethod
    def get_order_column(str_property) -> Column:
        switcher = {
            "id": PosicionAccionEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": PosicionAccionEntity.isin,
            "fecha_compra": PosicionAccionEntity.fecha_compra,
            "fecha_venta": PosicionAccionEntity.fecha_venta,
            "numero_acciones": PosicionAccionEntity.numero_acciones,
            "id_bolsa": PosicionAccionEntity.id_bolsa,
            "id_broker": PosicionAccionEntity.id_broker,
            "nombre_bolsa": BolsaEntity.nombre,
            "nombre_broker": BrokerEntity.nombre,
            "precio_accion_sin_comision": PosicionAccionEntity.precio_accion_sin_comision,
            "precio_venta_sin_comision": PosicionAccionEntity.precio_venta_sin_comision,
            "comision_compra": PosicionAccionEntity.comision_compra,
            "otras_comisiones": PosicionAccionEntity.otras_comisiones,
            "total_comisiones": (
                    PosicionAccionEntity.comision_compra + PosicionAccionEntity.otras_comisiones + PosicionAccionEntity.comision_venta),
            "total_compra_sin_comisiones": (
                    PosicionAccionEntity.precio_accion_sin_comision * PosicionAccionEntity.numero_acciones),
            "total": (
                    (PosicionAccionEntity.precio_accion_sin_comision * PosicionAccionEntity.numero_acciones) + (
                    PosicionAccionEntity.comision_compra + PosicionAccionEntity.otras_comisiones + PosicionAccionEntity.comision_venta)),
            "comision_venta": PosicionAccionEntity.comision_venta,
            "abierta": PosicionAccionEntity.abierta,
        }
        return switcher.get(str_property, PosicionAccionEntity.id)

    @staticmethod
    def get_filter_column(str_property: str) -> Column:
        switcher = {
            "id": PosicionAccionEntity.id,
            "nombre": ProductoEntity.nombre,
            "isin": PosicionAccionEntity.isin,
            "begin_fecha_compra": PosicionAccionEntity.fecha_compra,
            "end_fecha_compra": PosicionAccionEntity.fecha_compra,
            "begin_fecha_venta": PosicionAccionEntity.fecha_venta,
            "end_fecha_venta": PosicionAccionEntity.fecha_venta,
            "id_bolsa": PosicionAccionEntity.id_bolsa,
            "id:broker": PosicionAccionEntity.id_broker,
            "numero_acciones": PosicionAccionEntity.numero_acciones,
            "begin_numero_acciones": PosicionAccionEntity.numero_acciones,
            "end_numero_acciones": PosicionAccionEntity.numero_acciones,
            "precio_accion_sin_comision": PosicionAccionEntity.precio_accion_sin_comision,
            "begin_precio_accion_sin_comision": PosicionAccionEntity.precio_accion_sin_comision,
            "end_precio_accion_sin_comision": PosicionAccionEntity.precio_accion_sin_comision,
            "precio_venta_sin_comision": PosicionAccionEntity.precio_venta_sin_comision,
            "begin_venta_accion_sin_comision": PosicionAccionEntity.precio_venta_sin_comision,
            "end_precio_venta_sin_comision": PosicionAccionEntity.precio_venta_sin_comision,
            "comision_compra": PosicionAccionEntity.comision_compra,
            "begin_comision_compra": PosicionAccionEntity.comision_compra,
            "end_comision_compra": PosicionAccionEntity.comision_compra,
            "otras_comisiones": PosicionAccionEntity.otras_comisiones,
            "begin_otras_comisiones": PosicionAccionEntity.otras_comisiones,
            "end_otras_comisiones": PosicionAccionEntity.otras_comisiones,
            "comision_venta": PosicionAccionEntity.comision_venta,
            "begin_comision_venta": PosicionAccionEntity.comision_venta,
            "end_comision_venta": PosicionAccionEntity.comision_venta,
            "abierta": PosicionAccionEntity.abierta
        }
        return switcher.get(str_property, PosicionAccionEntity.id)

    @staticmethod
    def cast_to_column_type(column: Column, value: str) -> Any:
        if isinstance(value, str):
            caster = {
                PosicionAccionEntity.id: int,
                ProductoEntity.nombre: str,
                PosicionAccionEntity.isin: str,
                PosicionAccionEntity.fecha_compra: Date,
                PosicionAccionEntity.fecha_venta: Date,
                PosicionAccionEntity.numero_acciones: int,
                PosicionAccionEntity.id_bolsa: int,
                PosicionAccionEntity.id_broker: int,
                PosicionAccionEntity.precio_accion_sin_comision: float,
                PosicionAccionEntity.precio_venta_sin_comision: float,
                PosicionAccionEntity.comision_compra: float,
                PosicionAccionEntity.comision_venta: float,
                PosicionAccionEntity.otras_comisiones: float,
                PosicionAccionEntity.abierta: bool,
            }
            return caster.get(column)(value)
        else:
            return value

    def convert_to_object_domain(self) -> PosicionAccion:
        return PosicionAccion({"id": self.id,
                               "isin": self.isin,
                               "fecha_compra": self.fecha_compra,
                               "fecha_venta": self.fecha_venta,
                               "numero_acciones": self.numero_acciones,
                               "id_bolsa": self.id_bolsa,
                               "id_broker": self.id_broker,
                               "precio_accion_sin_comision": self.precio_accion_sin_comision,
                               "precio_venta_sin_comision": self.precio_venta_sin_comision,
                               "comision_compra": self.comision_compra,
                               "otras_comisiones": self.otras_comisiones,
                               "comision_venta": self.comision_venta,
                               "abierta": self.abierta,
                               })

    def update(self, posicion_accion: PosicionAccion):
        self.isin = posicion_accion.get_isin()
        self.fecha_compra = posicion_accion.get_fecha_compra()
        self.fecha_venta = posicion_accion.get_fecha_venta()
        self.numero_acciones = posicion_accion.get_numero_acciones()
        self.id_bolsa = posicion_accion.get_id_bolsa()
        self.id_broker = posicion_accion.get_id_broker()
        self.precio_accion_sin_comision = posicion_accion.get_precio_accion_sin_comision()
        self.precio_venta_sin_comision = posicion_accion.get_precio_venta_sin_comision()
        self.comision_compra = posicion_accion.get_comision_compra()
        self.otras_comisiones = posicion_accion.get_otras_comisiones()
        self.comision_venta = posicion_accion.get_comision_venta()
        self.abierta = posicion_accion.is_abierta()
