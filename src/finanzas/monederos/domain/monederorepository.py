from abc import ABC, abstractmethod
from typing import List

from src.finanzas.monederos.domain.monedero import Monedero
from src.persistence.domain.criteria import Criteria


class MonederoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Monedero]:
        pass

    @abstractmethod
    def new(self, params: dict) -> Monedero:
        pass

    @abstractmethod
    def update(self, monedero: Monedero) -> True:
        pass

    @abstractmethod
    def get(self, id_cuenta: int) -> Monedero:
        pass

    @abstractmethod
    def delete(self, id_monedero: int) -> bool:
        pass

    @abstractmethod
    def restore(self, id_monedero: int) -> bool:
        pass