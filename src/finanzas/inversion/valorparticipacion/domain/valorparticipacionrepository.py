from abc import ABC, abstractmethod
from typing import List, Tuple

from src.finanzas.inversion.valorparticipacion.domain.valorparticipacion import ValorParticipacion
from src.persistence.domain.criteria import Criteria


class ValorParticipacionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> Tuple[List[ValorParticipacion], int]:
        pass

    @abstractmethod
    def count(self, criteria: Criteria) -> int:
        pass

    @abstractmethod
    def new(self, params: dict) -> ValorParticipacion:
        pass

    @abstractmethod
    def delete(self, id_valor_participacion: int) -> bool:
        pass
