from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Any

from src.finanzas.domain.operacion import Operacion
from src.finanzas.domain.resumencuenta import ResumenCuenta
from src.finanzas.domain.resumengasto import ResumenGasto
from src.finanzas.domain.resumeningreso import ResumenIngreso
from src.finanzas.domain.resumenmonedero import ResumenMonedero
from src.finanzas.domain.resumentotal import ResumenTotal
from src.finanzas.domain.resumenvalorparticipacion import ResumenValorParticipacion
from src.persistence.domain.criteria import Criteria


class ResumenRepository(ABC):

    @abstractmethod
    def ingresos(self, criteria: Criteria) -> List[ResumenIngreso]:
        pass

    @abstractmethod
    def gastos(self, criteria: Criteria) -> List[ResumenGasto]:
        pass

    @abstractmethod
    def cuentas(self, criteria: Criteria) -> List[ResumenCuenta]:
        pass

    @abstractmethod
    def monederos(self, criteria: Criteria) -> List[ResumenMonedero]:
        pass

    @abstractmethod
    def total(self, criteria: Criteria) -> List[ResumenTotal]:
        pass

    @abstractmethod
    def resumen_valor_participacion_meses(self, criteria: Criteria) -> List[ResumenValorParticipacion]:
        pass

    @abstractmethod
    def resumen_valor_participacion_dias(self, criteria: Criteria) -> List[ResumenValorParticipacion]:
        pass