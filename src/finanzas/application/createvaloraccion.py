from src.finanzas.domain.valoraccion import ValorAccion
from src.finanzas.domain.valoraccionrepository import ValorAccionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateValorAccion(TransactionalUseCase):

    def __init__(self, valor_accion_repository: ValorAccionRepository):
        super().__init__([valor_accion_repository])
        self._valor_accion_repository = valor_accion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> ValorAccion:
        if "fecha" not in params or params["fecha"] is None:
            raise InvalidParamError("campo fecha obligatorio")
        if "isin" not in params or params["isin"] is None:
            raise InvalidParamError("campo isin obligatorio")
        if "valor" not in params or params["valor"] is None:
            raise InvalidParamError("campo valor obligatorio")
        valor_accion = self._valor_accion_repository.new(params)
        return valor_accion
