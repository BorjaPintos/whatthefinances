from abc import ABC, abstractmethod
from typing import List, Tuple

from src.finanzas.domain.dividendo_rango import DividendoRango
from src.finanzas.domain.isinnombre import IsinNombre
from src.finanzas.domain.posicionaccion import PosicionAccion
from src.persistence.domain.criteria import Criteria


class PosicionAccionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> Tuple[List[PosicionAccion], int]:
        pass
    @abstractmethod
    def dividendo_rango(self, criteria: Criteria) -> List[DividendoRango]:
        pass

    @abstractmethod
    def count(self, criteria: Criteria) -> int:
        pass

    @abstractmethod
    def new(self, params: dict) -> PosicionAccion:
        pass

    @abstractmethod
    def update(self, posicion_accion: PosicionAccion) -> bool:
        pass

    @abstractmethod
    def get(self, id_posicion_accion: int) -> PosicionAccion:
        pass

    @abstractmethod
    def delete(self, id_posicion_accion: int) -> bool:
        pass
