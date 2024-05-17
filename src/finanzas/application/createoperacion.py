from src.finanzas.application.commonoperacion import update_cantidad_cuentas, update_cantidad_monederos, validate_params
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.movimientocuentarepository import MovimientoCuentaRepository
from src.finanzas.domain.movimientomonederorepository import MovimientoMonederoRepository
from src.finanzas.domain.operacionrepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class CreateOperacion(TransactionalUseCase):

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
    def execute(self, params: dict) -> bool:
        validate_params(params)
        id_operacion = self._operacion_repository.new(params)
        params["id_operacion"] = id_operacion
        update_cantidad_cuentas(self._cuenta_repository, self._movimiento_cuenta_repository, params)
        update_cantidad_monederos(self._monedero_repository, self._movimiento_monedero_repository, params)
        return True
