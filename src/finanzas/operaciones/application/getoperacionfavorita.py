from src.finanzas.operaciones.domain.operacionfavorita import OperacionFavorita
from src.finanzas.operaciones.domain.operacionfavoritarepository import OperacionFavoritaRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase


class GetOperacionFavorita(TransactionalUseCase):

    def __init__(self, operacion_favorita_repository: OperacionFavoritaRepository):
        super().__init__([operacion_favorita_repository])
        self._operacion_favorita_repository = operacion_favorita_repository

    @transactional(readonly=True)
    def execute(self, id_operacion_favorita: int) -> OperacionFavorita:
        operacion_favorita = self._operacion_favorita_repository.get(id_operacion_favorita)
        return operacion_favorita
