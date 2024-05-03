from loguru import logger

from src.finanzas.domain.dividendo import Dividendo
from src.finanzas.domain.dividendorepository import DividendoRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class UpdateDividendo(TransactionalUseCase):

    def __init__(self, dividendo_repository: DividendoRepository):
        super().__init__([dividendo_repository])
        self._dividendo_repository = dividendo_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> Dividendo:
        self._validate_params(params)
        dividendo = self._dividendo_repository.get(params["id"])
        """El usuario puede cambiar todo"""

        dividendo.set_isin(params.get("isin"))
        dividendo.set_fecha(params.get("fecha"))
        dividendo.set_dividendo_por_participacion(params.get("dividendo_por_participacion"))
        dividendo.set_retencion_por_participacion(params.get("retencion_por_participacion"))

        updated = self._dividendo_repository.update(dividendo)
        if updated:
            try:
                self._session.flush()
                return dividendo
            except Exception as e:
                logger.info(e)
        else:
            raise MessageError("Ocurrió un error durante la actualización", 500)

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
