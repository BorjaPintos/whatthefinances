from abc import ABC, abstractmethod
from typing import List

from src.finanzas.resumenes.domain.resumencuenta import ResumenCuenta
from src.finanzas.resumenes.domain.resumengasto import ResumenGasto
from src.finanzas.resumenes.domain.resumeningreso import ResumenIngreso
from src.finanzas.resumenes.domain.resumenmonedero import ResumenMonedero
from src.finanzas.resumenes.domain.resumenposicion import ResumenPosicion
from src.finanzas.resumenes.domain.resumenposicionacumulada import ResumenPosicionAcumulada
from src.finanzas.resumenes.domain.resumentotal import ResumenTotal
from src.finanzas.resumenes.domain.resumenvalorparticipacion import ResumenValorParticipacion
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

    @abstractmethod
    def resumen_posiciones_meses(self, criteria: Criteria) -> List[ResumenPosicion]:
        pass

    @abstractmethod
    def resumen_posiciones_dias(self, criteria: Criteria) -> List[ResumenPosicion]:
        pass

    @abstractmethod
    def resumen_posiciones_meses_acumulada(self, criteria: Criteria) -> List[ResumenPosicionAcumulada]:
        pass