from src.login.domain.user import User
from src.login.domain.userrepository import UserRepository
from src.persistence.application.transactionalusecase import TransactionalUseCase, transactional
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator


class Login(TransactionalUseCase):

    def __init__(self, user_repository: UserRepository):
        super().__init__([user_repository])
        self._user_repository = user_repository

    @transactional(readonly=True)
    def execute(self, name: str, password: str) -> User:
        filter_name = SimpleFilter("name", WhereOperator.EQUAL, name)
        criteria = Criteria(filter=filter_name)
        user = self._user_repository.get(criteria)
        if user:
            user.login(password)
        return user
