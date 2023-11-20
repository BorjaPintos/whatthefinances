from src.login.domain.user import User
from src.login.domain.userrepository import UserRepository
from src.persistence.application.transactionalusecase import transactional, TransactionalUseCase
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.simplefilter import WhereOperator, SimpleFilter


class GetUser(TransactionalUseCase):

    def __init__(self, user_repository: UserRepository):
        super().__init__([user_repository])
        self._user_repository = user_repository

    @transactional(readonly=True)
    def execute(self, id: int) -> User:
        filter_id = SimpleFilter("id", WhereOperator.EQUAL, id)
        criteria = Criteria(filter=filter_id)
        user = self._user_repository.get(criteria)
        return user
