import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.domain.categoriagasto import CategoriaGasto
from src.finanzas.domain.categoriagastorepository import CategoriaGastoRepository
from src.finanzas.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class CategoriaGastoRepositorySQLAlchemy(ITransactionalRepository, CategoriaGastoRepository):

    def list(self, criteria: Criteria) -> List[CategoriaGasto]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(CategoriaGastoEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> CategoriaGasto:
        try:

            self.check_cuenta(params["id_cuenta_cargo_defecto"])
            self.check_monedero(params["id_monedero_defecto"])

            entity = CategoriaGastoEntity(descripcion=params.get("descripcion"),
                                          id_cuenta_cargo_defecto=params.get("id_cuenta_cargo_defecto"),
                                          id_monedero_defecto=params.get("id_monedero_defecto"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except IntegrityError as e:
            logger.info(e)
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def check_cuenta(self, id_cuenta: int):
        query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
        cuenta_entity = query_builder.filter_by(id=id_cuenta).one_or_none()
        if cuenta_entity is None:
            raise NotFoundError("No se encuentra la cuenta con id:  {}".format(id_cuenta))

    def check_monedero(self, id_monedero: int):
        query_builder = SQLAlchemyQueryBuilder(MonederoEntity, self._session).build_base_query()
        monedero_entity = query_builder.filter_by(id=id_monedero).one_or_none()
        if monedero_entity is None:
            raise NotFoundError("No se encuentra el monedero con id:  {}".format(id_monedero))

    def update(self, params: dict) -> CategoriaGasto:
        try:
            if "id_cuenta_cargo_defecto" in params and params["id_cuenta_cargo_defecto"]:
                self.check_cuenta(params["id_cuenta_cargo_defecto"])
            if "id_monedero_defecto" in params and params["id_monedero_defecto"]:
                self.check_monedero(params["id_monedero_defecto"])

            query_builder = SQLAlchemyQueryBuilder(CategoriaGastoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=params["id"]).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la categoria gasto con id:  {}".format(params["id"]))
            else:
                entity.update(params)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def get(self, id_categoria_gasto: int) -> CategoriaGasto:
        try:
            query_builder = SQLAlchemyQueryBuilder(CategoriaGastoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_categoria_gasto).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la categoria gasto con id:  {}".format(id_categoria_gasto))
            else:
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None
