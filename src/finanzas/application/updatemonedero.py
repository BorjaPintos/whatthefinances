from loguru import logger
from src.finanzas.domain.monedero import Monedero
from src.finanzas.domain.monederorepository import MonederoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateMonedero(TransactionalUseCase):

    def __init__(self, monedero_repository: MonederoRepository):
        super().__init__([monedero_repository])
        self._monedero_repository = monedero_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Monedero:
        self.__validate_params(params)
        monedero = self._monedero_repository.get(params["id"])
        """El usuario solo puede cambiar, nombre y cantidad inicial"""
        monedero.set_nombre(params.get("nombre"))
        monedero.set_cantidad_inicial(params.get("cantidad_inicial", 0.0))
        updated = self._monedero_repository.update(monedero)
        if updated:
            try:
                self._session.flush()
                return monedero
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

    def __validate_params(self, params: dict):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id no puede estar vacío")
        if "nombre" not in params or params["nombre"] is None:
            raise InvalidParamError("campo nombre no puede estar vacío")
