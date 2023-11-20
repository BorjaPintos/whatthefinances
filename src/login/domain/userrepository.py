

from abc import ABC, abstractmethod
from src.login.domain.user import User
from src.persistence.domain.criteria import Criteria


class UserRepository(ABC):

    @abstractmethod
    def get(self, criteria: Criteria) -> User:
        pass
