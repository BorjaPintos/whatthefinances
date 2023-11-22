from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.operacion import Operacion
from src.persistence.domain.criteria import Criteria


class OperacionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Operacion]:
        pass

    @abstractmethod
    def new(self, params: dict) -> Operacion:
        pass

    @abstractmethod
    def update(self, params: dict) -> Operacion:
        pass

    @abstractmethod
    def get(self, id_operacion: int) -> Operacion:
        pass

    @abstractmethod
    def delete(self, id_operacion: int) -> bool:
        pass
