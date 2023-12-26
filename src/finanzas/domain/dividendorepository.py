from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.dividendo import Dividendo
from src.persistence.domain.criteria import Criteria


class DividendoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Dividendo]:
        pass

    @abstractmethod
    def new(self, params: dict) -> Dividendo:
        pass

    @abstractmethod
    def update(self, dividendo: Dividendo) -> bool:
        pass

    @abstractmethod
    def get(self, id_dividendo: int) -> Dividendo:
        pass

    @abstractmethod
    def delete(self, id_dividendo: int) -> bool:
        pass
