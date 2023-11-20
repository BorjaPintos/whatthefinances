from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.operacion import Operacion
from src.persistence.domain.criteria import Criteria


class OperacionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Operacion]:
        pass