from typing import List

from src.finanzas.resumenes.domain.resumenposicionacumulada import ResumenPosicionAcumulada
from src.finanzas.resumenes.domain.resumenrepository import ResumenRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class ResumenPosicionesMesesAcumulada(TransactionalUseCase):

    def __init__(self, resumen_repository: ResumenRepository):
        super().__init__([resumen_repository])
        self._resumen_repository = resumen_repository

    @transactional(readonly=True)
    def execute(self, params: dict) -> List[ResumenPosicionAcumulada]:
        begin_fecha = params.get("begin_fecha")
        end_fecha = params.get("end_fecha")
        resumen_totales = self._resumen_repository.resumen_posiciones_meses_acumulada(
            begin_fecha=begin_fecha, end_fecha=end_fecha)
        return resumen_totales
