import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.inversion.broker.domain.broker import Broker
from src.finanzas.inversion.broker.domain.brokerrepository import BrokerRepository
from src.finanzas.inversion.broker.infrastructure.persistence.orm.brokerentity import BrokerEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class BrokerRepositorySQLAlchemy(ITransactionalRepository, BrokerRepository):

    def list(self, criteria: Criteria) -> List[Broker]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(BrokerEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> Broker:
        try:
            entity = BrokerEntity(nombre=params.get("nombre"),
                                  extranjero=params.get("extranjero"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except IntegrityError as e:
            logger.info(e)
        except Exception as e:
            traceback.print_exc()
        return None

    def update(self, broker: Broker) -> bool:
        try:

            query_builder = SQLAlchemyQueryBuilder(BrokerEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=broker.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el broker con id:  {}".format(broker.get_id()))
            else:
                entity.update(broker)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def get(self, id_broker: int) -> Broker:
        try:
            query_builder = SQLAlchemyQueryBuilder(BrokerEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_broker).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el broker con id:  {}".format(id_broker))
            else:
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None
