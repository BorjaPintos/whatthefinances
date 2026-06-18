import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.cuentas.domain.cuenta import Cuenta
from src.finanzas.cuentas.domain.cuentarepository import CuentaRepository
from src.finanzas.cuentas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.messageerror import MessageError
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
                                  cantidad_inicial=params.get("cantidad_inicial"),
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

    def update(self, cuenta: Cuenta) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=cuenta.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la cuenta con id:  {}".format(cuenta.get_id()))
            else:
                entity.update(cuenta)
                return True
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return False

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

    def delete(self, id_cuenta: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_cuenta).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la cuenta con id:  {}".format(id_cuenta))
            total = entity.cantidad_inicial + entity.diferencia
            if abs(total) > 0.01:
                raise MessageError("No se puede eliminar la cuenta porque no está vacía. Saldo actual: {}".format(round(total, 2)), 400)
            if entity.ponderacion is not None and entity.ponderacion != 0:
                raise MessageError("No se puede eliminar la cuenta porque tiene ponderación asignada: {}".format(entity.ponderacion), 400)
            entity.eliminado = True
            return True
        except NotFoundError as e:
            logger.info(e)
            raise e
        except MessageError as e:
            raise e
        except Exception as e:
            traceback.print_exc()
        return False

    def restore(self, id_cuenta: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_cuenta).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la cuenta con id:  {}".format(id_cuenta))
            if not entity.eliminado:
                raise MessageError("La cuenta no está eliminada", 400)
            entity.eliminado = False
            return True
        except NotFoundError as e:
            logger.info(e)
            raise e
        except MessageError as e:
            raise e
        except Exception as e:
            traceback.print_exc()
        return False
