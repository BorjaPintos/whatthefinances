from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.producto import Producto
from src.persistence.domain.criteria import Criteria


class ProductoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Producto]:
        pass

    @abstractmethod
    def new(self, params: dict) -> Producto:
        pass

    @abstractmethod
    def update(self, broker: Producto) -> bool:
        pass

    @abstractmethod
    def get(self, id_producto: int) -> Producto:
        pass