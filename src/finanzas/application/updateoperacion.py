from loguru import logger

from src.finanzas.application.commonoperacion import update_cantidad_cuentas, update_cantidad_monederos, \
    revert_cantidad_cuentas, revert_cantidad_monederos, validate_params
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.domain.operacion import Operacion
from src.finanzas.domain.operacionrepository import OperacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateOperacion(TransactionalUseCase):

    def __init__(self, operacion_repository: OperacionRepository,
                 monedero_repository: MonederoRepository,
                 cuenta_repository: CuentaRepository):
        super().__init__([operacion_repository, monedero_repository, cuenta_repository])
        self._operacion_repository = operacion_repository
        self._monedero_repository = monedero_repository
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Operacion:
        validate_params(params)

        operacion = self._operacion_repository.get(params["id"])

        "reverts necesarios por si cambia la cantidad,monederos o cuentas"
        revert_cantidad_cuentas(self._cuenta_repository, operacion)
        revert_cantidad_monederos(self._monedero_repository, operacion)
        self._session.flush()
        update_cantidad_cuentas(self._cuenta_repository, params)
        update_cantidad_monederos(self._monedero_repository, params)

        "El usuario puede cambiar todo"
        operacion.set_descripcion(params.get("descripcion"))
        operacion.set_id_cuenta_abono(params.get("id_cuenta_abono"))
        operacion.set_id_monedero_abono(params.get("id_monedero_abono"))
        operacion.set_id_categoria_ingreso(params.get("id_categoria_ingreso"))
        operacion.set_id_cuenta_cargo(params.get("id_cuenta_cargo"))
        operacion.set_id_monedero_cargo(params.get("id_monedero_cargo"))
        operacion.set_id_categoria_gasto(params.get("id_categoria_gasto"))
        operacion.set_cantidad(params.get("cantidad"))
        operacion.set_fecha(params.get("fecha"))

        updated = self._operacion_repository.update(operacion)

        if updated:
            try:
                self._session.flush()
                return operacion
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)
