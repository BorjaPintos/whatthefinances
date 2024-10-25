from src.finanzas.inversion.valorparticipacion.domain.valorparticipacion import ValorParticipacion
from src.finanzas.inversion.valorparticipacion.domain.valorparticipacionrepository import ValorParticipacionRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateValorParticipacion(TransactionalUseCase):

    def __init__(self, valor_participacion_repository: ValorParticipacionRepository):
        super().__init__([valor_participacion_repository])
        self._valor_participacion_repository = valor_participacion_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> ValorParticipacion:
        if "fecha_hora" not in params or params["fecha_hora"] is None:
            raise InvalidParamError("campo fecha_hora obligatorio")
        if "isin" not in params or params["isin"] is None:
            raise InvalidParamError("campo isin obligatorio")
        if "valor" not in params or params["valor"] is None:
            raise InvalidParamError("campo valor obligatorio")
        valor_participacion = self._valor_participacion_repository.new(params)
        return valor_participacion
