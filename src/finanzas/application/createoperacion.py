from src.finanzas.application.commonoperacion import update_cantidad_cuentas, update_cantidad_monederos, validate_params
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.operacionrepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateOperacion(TransactionalUseCase):

    def __init__(self, operacion_repository: OperacionRepository,
                 monedero_repository: MonederoRepository,
                 cuenta_repository: CuentaRepository):
        super().__init__([operacion_repository, monedero_repository, cuenta_repository])
        self._operacion_repository = operacion_repository
        self._monedero_repository = monedero_repository
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> bool:

        validate_params(params)
        created = self._operacion_repository.new(params)
        update_cantidad_cuentas(self._cuenta_repository, params)
        update_cantidad_monederos(self._monedero_repository, params)
        return created


