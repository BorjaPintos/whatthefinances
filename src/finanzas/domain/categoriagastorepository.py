from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.categoriagasto import CategoriaGasto
from src.persistence.domain.criteria import Criteria


class CategoriaGastoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[CategoriaGasto]:
        pass