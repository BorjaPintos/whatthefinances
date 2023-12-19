from loguru import logger

from src.finanzas.application.commonoperacion import revert_cantidad_cuentas, revert_cantidad_monederos
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.movimientocuentarepository import MovimientoCuentaRepository
from src.finanzas.domain.movimientomonederorepository import MovimientoMonederoRepository
from src.finanzas.domain.operacionrepository import OperacionRepository
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeletePosicionAccion(TransactionalUseCase):

    def __init__(self, posicion_accion_repository: PosicionAccionRepository
                 ):
        super().__init__([posicion_accion_repository])
        self._posicion_accion_repository_repository = posicion_accion_repository

    @transactional(readonly=False)
    def execute(self, id_posicion_accion: int) -> bool:

        deleted = self._posicion_accion_repository_repository.delete(id_posicion_accion)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
