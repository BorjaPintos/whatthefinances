import traceback

from src.login.domain.user import User
from src.login.domain.userrepository import UserRepository
from src.login.infrastructure.persistence.orm.userentity import UserEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class UserRepositorySQLAlchemy(ITransactionalRepository, UserRepository):

    def get(self, criteria: Criteria) -> User:
        try:
            query_builder = SQLAlchemyQueryBuilder(UserEntity, self._session)
            query = query_builder.build_query(criteria)
            result = query.one_or_none()
            if result is not None:
                return result.convert_to_object_domain()
        except Exception as e:
            traceback.print_exc()
            return None
