from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Any

from src.finanzas.domain.operacion import Operacion
from src.persistence.domain.criteria import Criteria


class ResumenRepository(ABC):

    @abstractmethod
    def ingresos(self, criteria):
        pass

    @abstractmethod
    def gastos(self, criteria):
        pass
