from abc import ABC, abstractmethod
from typing import List, Tuple

from src.finanzas.domain.valoraccion import ValorAccion
from src.persistence.domain.criteria import Criteria


class ValorAccionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> Tuple[List[ValorAccion], int]:
        pass

    @abstractmethod
    def count(self, criteria: Criteria) -> int:
        pass

    @abstractmethod
    def new(self, params: dict) -> ValorAccion:
        pass

    @abstractmethod
    def delete(self, id_valor_accion: int) -> bool:
        pass
