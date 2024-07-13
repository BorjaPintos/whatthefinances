from loguru import logger
from src.finanzas.cuentas.domain.cuenta import Cuenta
from src.finanzas.cuentas.domain.cuentarepository import CuentaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateCuenta(TransactionalUseCase):

    def __init__(self, cuenta_repository: CuentaRepository):
        super().__init__([cuenta_repository])
        self._cuenta_repository = cuenta_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Cuenta:
        self.__validate_params(params)
        cuenta = self._cuenta_repository.get(params["id"])
        """El usuario solo puede cambiar, nombre, cantidad inicial y ponderación"""
        cuenta.set_nombre(params.get("nombre"))
        cuenta.set_cantidad_inicial(params.get("cantidad_inicial", 0.0))
        cuenta.set_ponderacion(params.get("ponderacion", 0.0))
        updated = self._cuenta_repository.update(cuenta)
        if updated:
            try:
                self._session.flush()
                return cuenta
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def __validate_params(self, params: dict):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id no puede estar vacío")
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre no puede estar vacío")
