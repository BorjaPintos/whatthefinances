from abc import ABC, abstractmethod
from typing import List
from src.finanzas.operaciones.domain.operacionfavorita import OperacionFavorita
from src.persistence.domain.criteria import Criteria


class OperacionFavoritaRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[OperacionFavorita]:
        pass

    @abstractmethod
    def new(self, params: dict) -> int:
        pass

    @abstractmethod
    def update(self, operacion_favorita: OperacionFavorita) -> bool:
        pass

    @abstractmethod
    def get(self, id_operacion_favorita: int) -> OperacionFavorita:
        pass

    @abstractmethod
    def delete(self, id_operacion: int) -> bool:
        pass
