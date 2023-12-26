import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.domain.broker import Broker
from src.finanzas.domain.brokerrepository import BrokerRepository
from src.finanzas.domain.dividendo import Dividendo
from src.finanzas.domain.dividendorepository import DividendoRepository
from src.finanzas.infrastructure.persistence.orm.brokerentity import BrokerEntity
from src.finanzas.infrastructure.persistence.orm.dividendos import DividendoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class DividendoRepositorySQLAlchemy(ITransactionalRepository, DividendoRepository):

    def list(self, criteria: Criteria) -> List[Dividendo]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> Dividendo:
        try:
            entity = DividendoEntity(fecha=params.get("fecha"),
                                     isin=params.get("isin"),
                                     dividendo_por_accion=params.get("dividendo_por_accion"),
                                     retencion_por_accion=params.get("retencion_por_accion"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except IntegrityError as e:
            logger.info(e)
        except Exception as e:
            traceback.print_exc()
        return None

    def update(self, dividendo: Dividendo) -> bool:
        try:

            query_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=dividendo.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el dividendo con id:  {}".format(dividendo.get_id()))
            else:
                entity.update(dividendo)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def get(self, id_dividendo: int) -> Dividendo:
        try:
            query_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_dividendo).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el dividendo con id:  {}".format(id_dividendo))
            else:
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def delete(self, id_dividendo: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_dividendo).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el dividendo con id:  {}".format(id_dividendo))
            self._session.delete(entity)
            return True
        except Exception as e:
            traceback.print_exc()
        return False
