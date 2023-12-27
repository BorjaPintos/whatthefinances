import traceback
from typing import List, Tuple

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.domain.valoraccion import ValorAccion
from src.finanzas.domain.valoraccionrepository import ValorAccionRepository
from src.finanzas.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.finanzas.infrastructure.persistence.orm.valoraccionentity import ValorAccionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class ValorAccionRepositorySQLAlchemy(ITransactionalRepository, ValorAccionRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:
        columnas = (
            ValorAccionEntity.id, ValorAccionEntity.isin,
            ValorAccionEntity.fecha, ValorAccionEntity.valor,
            ProductoEntity.nombre
        )

        query_builder = SQLAlchemyQueryBuilder(ValorAccionEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria) \
            .join(ProductoEntity, ValorAccionEntity.isin == ProductoEntity.isin, isouter=False)
        return query

    def __get_complete_pagination_join_query(self, criteria: Criteria) -> Query:
        query = self.__get_complete_join_query(criteria)
        return query.offset(criteria.offset()).limit(criteria.limit())

    @staticmethod
    def __get_valor_accion_from_complete_join_row(row) -> ValorAccion:
        params = {"id": row[0],
                  "isin": row[1],
                  "fecha": row[2],
                  "valor": row[3],
                  "nombre": row[4]
                  }

        return ValorAccion(params)

    def list(self, criteria: Criteria) -> Tuple[List[ValorAccion], int]:
        elements = []
        try:
            query_elements = self.__get_complete_pagination_join_query(criteria)
            result = query_elements.all()
            n_elements = min(len(result), criteria.limit())
            if result is not None:
                for i in range(n_elements):
                    elements.append(self.__get_valor_accion_from_complete_join_row(result[i]))
            return elements, self.count(criteria)
        except Exception as e:
            traceback.print_exc()
        return elements, 0

    def count(self, criteria: Criteria) -> int:
        try:
            query = self.__get_complete_join_query(criteria)
            return query.count()
        except Exception as e:
            traceback.print_exc()
        return 0

    def new(self, params: dict) -> ValorAccion:
        try:
            self.check_isin(params.get("isin"))
            entity = ValorAccionEntity(fecha=params.get("fecha"),
                                       isin=params.get("isin"),
                                       valor=params.get("valor"))
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

    def delete(self, id_valor_accion: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(ValorAccionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_valor_accion).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el valor acción con id:  {}".format(id_valor_accion))
            self._session.delete(entity)
            return True
        except Exception as e:
            traceback.print_exc()
        return False

    def check_isin(self, isin: str):
        if isin is not None:
            query_builder = SQLAlchemyQueryBuilder(ProductoEntity, self._session).build_base_query()
            producto_entity = query_builder.filter_by(isin=isin).one_or_none()
            if producto_entity is None:
                raise NotFoundError("No se encuentra el producto con isin:  {}".format(isin))