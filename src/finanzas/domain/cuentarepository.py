from abc import ABC, abstractmethod
from typing import List
from src.finanzas.domain.cuenta import Cuenta
from src.persistence.domain.criteria import Criteria


class CuentaRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Cuenta]:
        pass

    @abstractmethod
    def new(self, params: dict) -> Cuenta:
        pass

    @abstractmethod
    def update(self, cuenta: Cuenta) -> bool:
        pass

    @abstractmethod
    def get(self, id_cuenta: int) -> Cuenta:
        pass
