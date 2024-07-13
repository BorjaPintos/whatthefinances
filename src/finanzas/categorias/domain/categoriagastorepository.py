from abc import ABC, abstractmethod
from typing import List

from src.finanzas.categorias.domain.categoriagasto import CategoriaGasto
from src.persistence.domain.criteria import Criteria


class CategoriaGastoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[CategoriaGasto]:
        pass

    @abstractmethod
    def new(self, params: dict) -> CategoriaGasto:
        pass

    @abstractmethod
    def update(self, categoria_gasto: CategoriaGasto) -> bool:
        pass

    @abstractmethod
    def get(self, id_categoria_gasto: int) -> CategoriaGasto:
        pass