from abc import ABC, abstractmethod
from typing import List, Tuple

from src.finanzas.monederos.domain.movimientomonedero import MovimientoMonedero
from src.persistence.domain.criteria import Criteria


class MovimientoMonederoRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> Tuple[List[MovimientoMonedero], int]:
        pass

    @abstractmethod
    def new(self, params: dict) -> bool:
        pass

    @abstractmethod
    def delete(self, id_movimiento: int) -> bool:
        pass
    @abstractmethod
    def get_by_id_operacion(self, id_operacion: int) -> List[MovimientoMonedero]:
        pass