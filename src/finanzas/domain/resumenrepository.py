from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Any

from src.finanzas.domain.operacion import Operacion
from src.finanzas.domain.resumencuenta import ResumenCuenta
from src.finanzas.domain.resumengasto import ResumenGasto
from src.finanzas.domain.resumeningreso import ResumenIngreso
from src.finanzas.domain.resumenmonedero import ResumenMonedero
from src.persistence.domain.criteria import Criteria


class ResumenRepository(ABC):

    @abstractmethod
    def ingresos(self, criteria) -> List[ResumenIngreso]:
        pass

    @abstractmethod
    def gastos(self, criteria) -> List[ResumenGasto]:
        pass

    @abstractmethod
    def cuentas(self, criteria) -> List[ResumenCuenta]:
        pass
    @abstractmethod
    def monederos(self, criteria) -> List[ResumenMonedero]:
        pass