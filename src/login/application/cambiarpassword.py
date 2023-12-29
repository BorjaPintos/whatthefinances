from loguru import logger

from src.login.domain.user import User
from src.login.domain.userrepository import UserRepository
from src.persistence.application.transactionalusecase import TransactionalUseCase, transactional
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError


class CambiarPassword(TransactionalUseCase):

    def __init__(self, user_repository: UserRepository):
        super().__init__([user_repository])
        self._user_repository = user_repository

    @transactional(readonly=False)
    def execute(self, params: dict) -> User:
        self._validate_params(params)
        id = params["id"]
        old_password = params["password"]
        new_password = params["new_password"]
        filter_name = SimpleFilter("id", WhereOperator.EQUAL, id)
        criteria = Criteria(filter=filter_name)
        user = self._user_repository.get(criteria)
        if user:
            user.change_password(old_password, new_password)
            updated = self._user_repository.update(user)
            if updated:
                try:
                    self._session.flush()
                    return user
                except Exception as e:
                    logger.info(e)
            else:
                raise MessageError("Ocurrió un error durante la actualización", 500)

    @staticmethod
    def _validate_params(params):
        if "id" not in params or params["id"] is None:
            raise InvalidParamError("campo id obligatorio")
        if "password" not in params or params["password"] is None:
            raise InvalidParamError("campo password obligatorio")
        if "new_password" not in params or params["new_password"] is None:
            raise InvalidParamError("campo new_password obligatorio")
