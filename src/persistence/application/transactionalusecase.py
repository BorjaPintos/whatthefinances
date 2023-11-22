import traceback

from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from src.persistence.application.baseusecase import BaseUseCase
from src.persistence.application.databasemanager import DatabaseManager
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.notfounderror import NotFoundError


class TransactionalUseCase(BaseUseCase):

    def __init__(self, transactional_repositories=None):
        self._session = None
        self._transactional_repositories = transactional_repositories

    def set_session(self, session):
        self._session = session

    def get_session(self):
        return self._session

    def get_transactional_repositories(self):
        return self._transactional_repositories


def transactional(readonly=False):
    def transactional_decorator(function):
        def transactional_function(*args, **kwargs):
            try:
                if readonly:
                    with DatabaseManager.get_readonly_session_scope() as session:
                        set_sessions(args[0], session)
                        return function(*args, **kwargs)
                else:
                    with DatabaseManager.get_session_scope() as session:
                        set_sessions(args[0], session)
                        return function(*args, **kwargs)

            except UnauthorizedError as e:
                raise e
            except NotFoundError as e:
                raise e
            except InvalidParamError as e:
                raise e
            except Exception as e:
                traceback.print_exc()
        return transactional_function

    return transactional_decorator


def set_sessions(transactionalUseCase, session):
    transactionalUseCase.set_session(session)
    if transactionalUseCase.get_transactional_repositories():
        for repository in transactionalUseCase.get_transactional_repositories():
            repository.set_session(session)
