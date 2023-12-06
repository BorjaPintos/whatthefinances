from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Any

from src.finanzas.domain.operacion import Operacion
from src.persistence.domain.criteria import Criteria


class OperacionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> Tuple[List[Operacion], Union[bool, Any]]:
        pass

    @abstractmethod
    def new(self, params: dict) -> bool:
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
