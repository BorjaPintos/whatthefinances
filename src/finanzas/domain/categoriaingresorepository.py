from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.categoriaingreso import CategoriaIngreso
from src.persistence.domain.criteria import Criteria


class CategoriaIngresoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[CategoriaIngreso]:
        pass