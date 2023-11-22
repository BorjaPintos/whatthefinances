import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.domain.cuenta import Cuenta
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class CuentaRepositorySQLAlchemy(ITransactionalRepository, CuentaRepository):

    def list(self, criteria: Criteria) -> List[Cuenta]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> Cuenta:
        try:
            entity = CuentaEntity(nombre=params.get("nombre"),
                                  cantidad_base=params.get("cantidad_base"),
                                  diferencia=params.get("diferencia"),
                                  ponderacion=params.get("ponderacion"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except IntegrityError as e:
            logger.info(e)
        except Exception as e:
            traceback.print_exc()
        return None

    def update(self, params: dict) -> Cuenta:
        try:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=params["id"]).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la cuenta con id:  {}".format(params["id"]))
            else:
                entity.update(params)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def get(self, id_cuenta: int) -> Cuenta:
        try:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_cuenta).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la cuenta con id:  {}".format(id_cuenta))
            else:
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

