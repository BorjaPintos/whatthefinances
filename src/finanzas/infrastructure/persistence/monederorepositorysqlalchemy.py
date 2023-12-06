import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.domain.monedero import Monedero
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class MonederoRepositorySQLAlchemy(ITransactionalRepository, MonederoRepository):

    def list(self, criteria: Criteria) -> List[Monedero]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(MonederoEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> Monedero:
        try:
            entity = MonederoEntity(nombre=params.get("nombre"),
                                    cantidad_inicial=params.get("cantidad_inicial"),
                                    diferencia=params.get("diferencia"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except IntegrityError as e:
            logger.info(e)
        except Exception as e:
            traceback.print_exc()
        return None

    def update(self, monedero: Monedero) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(MonederoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=monedero.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el monedero con id:  {}".format(monedero.get_id()))
            else:
                entity.update(monedero)
                return True
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return False

    def get(self, id_monedero: int) -> Monedero:
        try:
            query_builder = SQLAlchemyQueryBuilder(MonederoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_monedero).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el monedero con id:  {}".format(id_monedero))
            else:
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None
