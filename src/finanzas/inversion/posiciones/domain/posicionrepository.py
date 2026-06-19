from abc import ABC, abstractmethod
from typing import List, Tuple

from src.finanzas.inversion.dividendos.domain.dividendo_rango import DividendoRango
from src.finanzas.inversion.posiciones.domain.posicion import Posicion
from src.persistence.domain.criteria import Criteria


class PosicionRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> Tuple[List[Posicion], int]:
        pass

    @abstractmethod
    def count(self, criteria: Criteria) -> int:
        pass

    @abstractmethod
    def new(self, params: dict) -> Posicion:
        pass

    @abstractmethod
    def update(self, posicion: Posicion) -> bool:
        pass

    @abstractmethod
    def get(self, id_posicion: int) -> Posicion:
        pass

    @abstractmethod
    def delete(self, id_posicion: int) -> bool:
        pass

    @abstractmethod
    def get_oldest_open_by_isin_and_broker(self, isin: str, id_broker: int) -> Posicion:
        pass
