from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.categoriaingreso import CategoriaIngreso
from src.persistence.domain.criteria import Criteria


class CategoriaIngresoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[CategoriaIngreso]:
        pass

    @abstractmethod
    def new(self, params: dict) -> CategoriaIngreso:
        pass

    @abstractmethod
    def update(self, categoria_ingreso: CategoriaIngreso) -> bool:
        pass

    @abstractmethod
    def get(self, id_categoria_ingreso: int) -> CategoriaIngreso:
        pass