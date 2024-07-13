from abc import ABC, abstractmethod
from typing import List

from src.finanzas.inversion.bolsa.domain.bolsa import Bolsa
from src.persistence.domain.criteria import Criteria


class BolsaRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Bolsa]:
        pass

    @abstractmethod
    def new(self, params: dict) -> Bolsa:
        pass

    @abstractmethod
    def update(self, broker: Bolsa) -> bool:
        pass

    @abstractmethod
    def get(self, id_bolsa: int) -> Bolsa:
        pass