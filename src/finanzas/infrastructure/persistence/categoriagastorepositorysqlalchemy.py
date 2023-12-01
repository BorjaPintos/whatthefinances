import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.domain.categoriagasto import CategoriaGasto
from src.finanzas.domain.categoriagastorepository import CategoriaGastoRepository
from src.finanzas.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class CategoriaGastoRepositorySQLAlchemy(ITransactionalRepository, CategoriaGastoRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:
        columnas = (
            CategoriaGastoEntity.id, CategoriaGastoEntity.descripcion,
            CategoriaGastoEntity.id_cuenta_cargo_defecto, CuentaEntity.nombre,
            CategoriaGastoEntity.id_monedero_defecto, MonederoEntity.nombre)

        query_builder = SQLAlchemyQueryBuilder(CategoriaGastoEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria) \
            .join(CuentaEntity, CategoriaGastoEntity.id_cuenta_cargo_defecto == CuentaEntity.id, isouter=True) \
            .join(MonederoEntity, CategoriaGastoEntity.id_monedero_defecto == MonederoEntity.id, isouter=True)
        return query

    def list(self, criteria: Criteria) -> List[CategoriaGasto]:
        elements = []
        try:
            query = self.__get_complete_join_query(criteria)
            result = query.all()

            if result is not None:
                for row in result:
                    elements.append(self.__get_categoria_gasto_from_complete_join_row(row))

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
        if id_cuenta:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
            cuenta_entity = query_builder.filter_by(id=id_cuenta).one_or_none()
            if cuenta_entity is None:
                raise NotFoundError("No se encuentra la cuenta con id:  {}".format(id_cuenta))

    def check_monedero(self, id_monedero: int):
        if id_monedero:
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
            query = self.__get_complete_join_query(
                Criteria(filter=SimpleFilter("id", WhereOperator.IS, id_categoria_gasto)))
            result = query.one_or_none()
            if result is None:
                raise NotFoundError("No se encuentra la categoria-ingreso con id:  {}".format(id_categoria_gasto))
            else:
                return self.__get_categoria_gasto_from_complete_join_row(result)
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    @staticmethod
    def __get_categoria_gasto_from_complete_join_row(row) -> CategoriaGasto:
        params = {"id": row[0],
                  "descripcion": row[1],
                  "id_cuenta_cargo_defecto": row[2],
                  "nombre_cuenta_cargo_defecto": row[3],
                  "id_monedero_defecto": row[4],
                  "nombre_monedero_defecto": row[5]
                  }
        return CategoriaGasto(params)
