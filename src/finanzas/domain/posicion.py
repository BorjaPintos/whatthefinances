from datetime import date


class Posicion:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._nombre = params.get("nombre")
        self._isin = params.get("isin")
        self._fecha_compra = params.get("fecha_compra")
        self._fecha_venta = params.get("fecha_venta")
        self._numero_participaciones = params.get("numero_participaciones")
        self._id_bolsa = params.get("id_bolsa")
        self._nombre_bolsa = params.get("nombre_bolsa")
        self._id_broker = params.get("id_broker")
        self._nombre_broker = params.get("nombre_broker")
        self._precio_compra_sin_comision = params.get("precio_compra_sin_comision")
        self._precio_venta_sin_comision = params.get("precio_venta_sin_comision")
        self._comision_compra = params.get("comision_compra")
        self._otras_comisiones = params.get("otras_comisiones")
        self._comision_venta = params.get("comision_venta")
        self._abierta = params.get("abierta")
        self._valor_participacion = params.get("valor_participacion")
        self._dividendos_por_participacion = params.get("dividendos_por_participacion")
        self._retencion_por_participacion = params.get("retencion_por_participacion")

    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def set_nombre(self, nombre: str):
        self._nombre = nombre

    def get_isin(self) -> str:
        return self._isin

    def set_isin(self, isin: str):
        self._isin = isin

    def get_fecha_compra(self) -> date:
        return self._fecha_compra

    def set_fecha_compra(self, fecha_compra: date):
        self._fecha_compra = fecha_compra

    def get_fecha_venta(self) -> date:
        return self._fecha_venta

    def set_fecha_venta(self, fecha_venta: date):
        self._fecha_venta = fecha_venta

    def get_numero_participaciones(self) -> float:
        return self._numero_participaciones

    def set_numero_participaciones(self, numero_participaciones: float):
        self._numero_participaciones = numero_participaciones

    def get_id_bolsa(self) -> int:
        return self._id_bolsa

    def set_id_bolsa(self, id_bolsa: int):
        self._id_bolsa = id_bolsa

    def get_id_broker(self) -> int:
        return self._id_broker

    def set_id_broker(self, id_broker: int):
        self._id_broker = id_broker

    def get_precio_compra_sin_comision(self) -> float:
        return self._precio_compra_sin_comision

    def set_precio_compra_sin_comision(self, precio_compra_sin_comision: float):
        self._precio_compra_sin_comision = precio_compra_sin_comision

    def get_precio_venta_sin_comision(self) -> float:
        return self._precio_venta_sin_comision

    def set_precio_venta_sin_comision(self, precio_venta_sin_comision: float):
        self._precio_venta_sin_comision = precio_venta_sin_comision

    def get_comision_compra(self) -> float:
        return self._comision_compra

    def set_comision_compra(self, comision_compra: float):
        self._comision_compra = comision_compra

    def get_otras_comisiones(self) -> float:
        return self._otras_comisiones

    def set_otras_comisiones(self, otras_comisiones: float):
        self._otras_comisiones = otras_comisiones

    def get_comision_venta(self) -> float:
        return self._comision_venta

    def set_comision_venta(self, comision_venta: float):
        self._comision_venta = comision_venta

    def is_abierta(self) -> bool:
        return self._abierta

    def set_abierta(self, abierta: bool):
        self._abierta = abierta

    def get_nombre_bolsa(self) -> str:
        return self._nombre_bolsa

    def get_nombre_broker(self) -> str:
        return self._nombre_broker

    def get_valor_participacion(self) -> float:
        if self._valor_participacion is None:
            return self._precio_compra_sin_comision
        return self._valor_participacion

    def get_dividendos(self) -> float:
        if self._dividendos_por_participacion is None:
            return 0.0
        else:
            return self._dividendos_por_participacion * self._numero_participaciones

    def get_retencion_dividendos(self) -> float:
        if self._retencion_por_participacion is None:
            return 0.0
        else:
            return self._retencion_por_participacion * self._numero_participaciones

    def get_dividendos_total(self) -> float:
        return self.get_dividendos() - self.get_retencion_dividendos()

    def get_todas_comisiones(self):
        return self.get_comision_compra() + self.get_otras_comisiones() + self.get_comision_venta()

    def get_precio_compra_sin_comisiones(self):
        return self.get_precio_compra_sin_comision() * self.get_numero_participaciones()

    def get_precio_venta_sin_comisiones(self):
        return self.get_precio_venta_sin_comision() * self.get_numero_participaciones()

    def get_valor_actual(self):
        return self.get_valor_participacion() * self.get_numero_participaciones()

    def get_dto(self) -> dict:
        return {"id": self._id,
                "nombre": self._nombre,
                "isin": self._isin,
                "fecha_compra": self._fecha_compra.strftime("%d/%m/%Y"),
                "fecha_venta": self._fecha_venta.strftime("%d/%m/%Y") if self._fecha_venta is not None else "",
                "numero_participaciones": self._numero_participaciones,
                "id_bolsa": self._id_bolsa,
                "id_broker": self._id_broker,
                "nombre_bolsa": self._nombre_bolsa,
                "nombre_broker": self._nombre_broker,
                "precio_compra_sin_comision": self._precio_compra_sin_comision,
                "precio_venta_sin_comision": self._precio_venta_sin_comision,
                "comision_compra": self._comision_compra,
                "comision_venta": self._comision_venta,
                "otras_comisiones": self._otras_comisiones,
                "total_comisiones": self.get_todas_comisiones(),
                "total_compra_sin_comisiones": self.get_precio_compra_sin_comisiones(),
                "total": self.get_precio_compra_sin_comisiones() + self.get_todas_comisiones(),
                "abierta": self._abierta,
                "valor_participacion": self.get_valor_participacion(),
                "valor_actual": self.get_valor_actual(),
                "ganacia_sin_comosiones": self.get_valor_actual() - self.get_precio_compra_sin_comisiones(),
                "ganacia_con_comosiones": self.get_valor_actual() - self.get_precio_compra_sin_comisiones() -
                                          self.get_todas_comisiones(),
                "diviendos": self.get_dividendos(),
                "retencion_dividendos": self.get_retencion_dividendos(),
                "dividendos_total": self.get_dividendos_total(),
                "ganacia_con_comosiones_y_dividendos": self.get_valor_actual() + self.get_dividendos_total()
                                                       - self.get_precio_compra_sin_comisiones() - self.get_todas_comisiones(),
                "valor_adquisicion": self.get_precio_compra_sin_comisiones() + self.get_comision_compra(),
                "valor_transmision": self.get_precio_venta_sin_comisiones() - self.get_comision_venta()

                }
