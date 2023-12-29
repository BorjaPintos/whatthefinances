import traceback

from loguru import logger

from src.login.domain.user import User
from src.login.domain.userrepository import UserRepository
from src.login.infrastructure.persistence.orm.userentity import UserEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


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

    def update(self, user: User) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(UserEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=user.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el broker con id:  {}".format(user.get_id()))
            else:
                entity.update(user)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None