from src.finanzas.inversion.dividendos.domain.dividendo import Dividendo
from src.finanzas.inversion.dividendos.domain.dividendorepository import DividendoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError


class CreateDividendo(TransactionalUseCase):

    def __init__(self, dividendo_repository: DividendoRepository):
        super().__init__([dividendo_repository])
        self._dividendo_repository = dividendo_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Dividendo:
        self._validate_params(params)
        dividendo = self._dividendo_repository.new(params)
        return dividendo

    @staticmethod
    def _validate_params(params):
        if "fecha" not in params or params["fecha"] is None:
            raise InvalidParamError("campo fecha obligatorio")
        if "isin" not in params or params["isin"] is None:
            raise InvalidParamError("campo isin obligatorio")
        if "dividendo_por_participacion" not in params or params["dividendo_por_participacion"] is None:
            raise InvalidParamError("campo dividendo_por_participacion obligatorio")
        if "retencion_por_participacion" not in params or params["retencion_por_participacion"] is None:
            raise InvalidParamError("campo retencion_por_participacion obligatorio")
