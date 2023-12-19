from loguru import logger

from src.finanzas.application.commonoperacion import revert_cantidad_cuentas, revert_cantidad_monederos
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.movimientocuentarepository import MovimientoCuentaRepository
from src.finanzas.domain.movimientomonederorepository import MovimientoMonederoRepository
from src.finanzas.domain.operacionrepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.messageerror import MessageError


class DeleteOperacion(TransactionalUseCase):

    def __init__(self, operacion_repository: OperacionRepository,
                 monedero_repository: MonederoRepository,
                 movimiento_monedero_repository: MovimientoMonederoRepository,
                 cuenta_repository: CuentaRepository,
                 movimiento_cuenta_repository: MovimientoCuentaRepository
                 ):
        super().__init__([operacion_repository,
                          monedero_repository, movimiento_monedero_repository,
                          cuenta_repository, movimiento_cuenta_repository])
        self._operacion_repository = operacion_repository
        self._monedero_repository = monedero_repository
        self._movimiento_monedero_repository = movimiento_monedero_repository
        self._cuenta_repository = cuenta_repository
        self._movimiento_cuenta_repository = movimiento_cuenta_repository

    @transactional(readonly=False)
    def execute(self, id_operacion: int) -> bool:

        operacion = self._operacion_repository.get(id_operacion)
        "reverts necesarios de la operacion"
        revert_cantidad_cuentas(self._cuenta_repository, self._movimiento_cuenta_repository, operacion)
        revert_cantidad_monederos(self._monedero_repository, self._movimiento_monedero_repository, operacion)
        deleted = self._operacion_repository.delete(id_operacion)
        if deleted:
            try:
                self._session.flush()
                return deleted
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante el borrado", 500)
