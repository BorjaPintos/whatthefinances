from loguru import logger

from src.finanzas.operaciones.application.commonoperacion import revert_cantidad_cuentas, revert_cantidad_monederos
from src.finanzas.cuentas.domain.cuentarepository import CuentaRepository
from src.finanzas.monederos.domain.monederorepository import MonederoRepository
from src.finanzas.cuentas.domain.movimientocuentarepository import MovimientoCuentaRepository
from src.finanzas.monederos.domain.movimientomonederorepository import MovimientoMonederoRepository
from src.finanzas.operaciones.domain.operacion import Operacion
from src.finanzas.operaciones.domain.operacionrepository import OperacionRepository
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
        self.__check_monederos_not_deleted(operacion)
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

    def __check_monederos_not_deleted(self, operacion: Operacion):
        id_cargo = operacion.get_id_monedero_cargo()
        id_abono = operacion.get_id_monedero_abono()
        if id_cargo is not None:
            monedero = self._monedero_repository.get(id_cargo)
            if monedero and monedero.get_eliminado():
                raise MessageError(
                    "No se puede eliminar la operación porque el monedero de cargo '{}' está eliminado. Restaure el monedero primero.".format(
                        monedero.get_nombre()), 400)
        if id_abono is not None:
            monedero = self._monedero_repository.get(id_abono)
            if monedero and monedero.get_eliminado():
                raise MessageError(
                    "No se puede eliminar la operación porque el monedero de abono '{}' está eliminado. Restaure el monedero primero.".format(
                        monedero.get_nombre()), 400)
