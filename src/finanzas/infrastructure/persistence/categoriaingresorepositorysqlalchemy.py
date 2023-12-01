import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.domain.categoriaingreso import CategoriaIngreso
from src.finanzas.domain.categoriaingresorepository import CategoriaIngresoRepository
from src.finanzas.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class CategoriaIngresoRepositorySQLAlchemy(ITransactionalRepository, CategoriaIngresoRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:
        columnas = (
            CategoriaIngresoEntity.id, CategoriaIngresoEntity.descripcion,
            CategoriaIngresoEntity.id_cuenta_abono_defecto, CuentaEntity.nombre,
            CategoriaIngresoEntity.id_monedero_defecto, MonederoEntity.nombre)

        query_builder = SQLAlchemyQueryBuilder(CategoriaIngresoEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria) \
            .join(CuentaEntity, CategoriaIngresoEntity.id_cuenta_abono_defecto == CuentaEntity.id, isouter=True) \
            .join(MonederoEntity, CategoriaIngresoEntity.id_monedero_defecto == MonederoEntity.id, isouter=True)
        return query

    def list(self, criteria: Criteria) -> List[CategoriaIngreso]:
        elements = []
        try:
            query = self.__get_complete_join_query(criteria)
            result = query.all()

            if result is not None:
                for row in result:
                    elements.append(self.__get_categoria_ingreso_from_complete_join_row(row))

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> CategoriaIngreso:
        try:

            self.check_cuenta(params["id_cuenta_abono_defecto"])
            self.check_monedero(params["id_monedero_defecto"])

            entity = CategoriaIngresoEntity(descripcion=params.get("descripcion"),
                                            id_cuenta_abono_defecto=params.get("id_cuenta_abono_defecto"),
                                            id_monedero_defecto=params.get("id_monedero_defecto"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except IntegrityError as e:
            logger.info(e)
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

    def update(self, params: dict) -> CategoriaIngreso:
        try:
            if "id_cuenta_abono_defecto" in params and params["id_cuenta_abono_defecto"]:
                self.check_cuenta(params["id_cuenta_abono_defecto"])
            if "id_monedero_defecto" in params and params["id_monedero_defecto"]:
                self.check_monedero(params["id_monedero_defecto"])

            query_builder = SQLAlchemyQueryBuilder(CategoriaIngresoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=params["id"]).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la categoria ingreso con id:  {}".format(params["id"]))
            else:
                entity.update(params)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def get(self, id_categoria_ingreso: int) -> CategoriaIngreso:
        try:
            query = self.__get_complete_join_query(
                Criteria(filter=SimpleFilter("id", WhereOperator.IS, id_categoria_ingreso)))
            result = query.one_or_none()
            if result is None:
                raise NotFoundError("No se encuentra la categoria-ingreso con id:  {}".format(id_categoria_ingreso))
            else:
                return self.__get_categoria_ingreso_from_complete_join_row(result)
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    @staticmethod
    def __get_categoria_ingreso_from_complete_join_row(row) -> CategoriaIngreso:
        params = {"id": row[0],
                  "descripcion": row[1],
                  "id_cuenta_abono_defecto": row[2],
                  "nombre_cuenta_abono_defecto": row[3],
                  "id_monedero_defecto": row[4],
                  "nombre_monedero_defecto": row[5]
                  }
        return CategoriaIngreso(params)
