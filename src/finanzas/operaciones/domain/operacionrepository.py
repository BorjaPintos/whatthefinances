from abc import ABC, abstractmethod
from typing import List, Tuple

from src.finanzas.operaciones.domain.operacion import Operacion
from src.persistence.domain.criteria import Criteria


class OperacionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> Tuple[List[Operacion], int]:
        pass

    @abstractmethod
    def count(self, criteria: Criteria) -> int:
        pass

    @abstractmethod
    def new(self, params: dict) -> int:
        pass

    @abstractmethod
    def update(self, operacion: Operacion) -> bool:
        pass

    @abstractmethod
    def get(self, id_operacion: int) -> Operacion:
        pass

    @abstractmethod
    def delete(self, id_operacion: int) -> bool:
        pass
