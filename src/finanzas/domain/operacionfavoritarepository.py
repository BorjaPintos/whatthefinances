from abc import ABC, abstractmethod
from typing import List, Tuple
from src.finanzas.domain.operacionFavorita import OperacionFavorita
from src.persistence.domain.criteria import Criteria


class OperacionFavoritaRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[OperacionFavorita]:
        pass

    @abstractmethod
    def new(self, params: dict) -> int:
        pass

    @abstractmethod
    def delete(self, id_operacion: int) -> bool:
        pass
