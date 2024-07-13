import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.inversion.bolsa.domain.bolsa import Bolsa
from src.finanzas.inversion.bolsa.domain.bolsarepository import BolsaRepository
from src.finanzas.inversion.bolsa.infrastructure.persistence.orm.bolsaentity import BolsaEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class BolsaRepositorySQLAlchemy(ITransactionalRepository, BolsaRepository):

    def list(self, criteria: Criteria) -> List[Bolsa]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(BolsaEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> Bolsa:
        try:
            entity = BolsaEntity(nombre=params.get("nombre"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except IntegrityError as e:
            logger.info(e)
        except Exception as e:
            traceback.print_exc()
        return None

    def update(self, bolsa: Bolsa) -> bool:
        try:

            query_builder = SQLAlchemyQueryBuilder(BolsaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=bolsa.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la bolsa con id:  {}".format(bolsa.get_id()))
            else:
                entity.update(bolsa)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def get(self, id_bolsa: int) -> Bolsa:
        try:
            query_builder = SQLAlchemyQueryBuilder(BolsaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_bolsa).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la bolsa con id:  {}".format(id_bolsa))
            else:
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None
