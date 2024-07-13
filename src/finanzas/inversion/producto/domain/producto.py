from src.finanzas.inversion.producto.domain.plataformaproductoenum import PlataformaProductoEnum


class Producto:

    def __init__(self, params: dict):
        self._id = params.get("id")
        self._nombre = params.get("nombre")
        self._isin = params.get("isin")
        self._plataforma = params.get("plataforma")
        self._url = params.get("url")

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

    def get_plataforma(self) -> PlataformaProductoEnum:
        return self._plataforma

    def set_plataforma(self, plataforma: PlataformaProductoEnum):
        self._plataforma = plataforma

    def get_url(self) -> str:
        return self._url

    def set_url(self, url: str):
        self._url = url

    def get_dto(self) -> dict:
        return {"id": self._id,
                "nombre": self._nombre,
                "isin": self._isin,
                "id_plataforma": self._plataforma.value if self._plataforma is not None else None,
                "plataforma": self._plataforma.name if self._plataforma is not None else None,
                "url": self._url
                }
