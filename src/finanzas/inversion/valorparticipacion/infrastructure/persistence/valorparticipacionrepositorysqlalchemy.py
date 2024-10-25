import traceback
from typing import List, Tuple

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.inversion.valorparticipacion.domain.valorparticipacion import ValorParticipacion
from src.finanzas.inversion.valorparticipacion.domain.valorparticipacionrepository import ValorParticipacionRepository
from src.finanzas.inversion.producto.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.finanzas.inversion.valorparticipacion.infrastructure.persistence.orm.valorparticipacionentity import ValorParticipacionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class ValorParticipacionRepositorySQLAlchemy(ITransactionalRepository, ValorParticipacionRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:
        columnas = (
            ValorParticipacionEntity.id, ValorParticipacionEntity.isin,
            ValorParticipacionEntity.fecha, ValorParticipacionEntity.valor,
            ProductoEntity.nombre
        )

        query_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria) \
            .join(ProductoEntity, ValorParticipacionEntity.isin == ProductoEntity.isin, isouter=False)
        return query

    def __get_complete_pagination_join_query(self, criteria: Criteria) -> Query:
        query = self.__get_complete_join_query(criteria)
        return query.offset(criteria.offset()).limit(criteria.limit())

    @staticmethod
    def __get_valor_participacion_from_complete_join_row(row) -> ValorParticipacion:
        params = {"id": row[0],
                  "isin": row[1],
                  "fecha": row[2],
                  "valor": row[3],
                  "nombre": row[4]
                  }

        return ValorParticipacion(params)

    def list(self, criteria: Criteria) -> Tuple[List[ValorParticipacion], int]:
        elements = []
        try:
            query_elements = self.__get_complete_pagination_join_query(criteria)
            result = query_elements.all()
            n_elements = min(len(result), criteria.limit())
            if result is not None:
                for i in range(n_elements):
                    elements.append(self.__get_valor_participacion_from_complete_join_row(result[i]))
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

    def new(self, params: dict) -> ValorParticipacion:
        try:
            self.check_isin(params.get("isin"))
            entity = ValorParticipacionEntity(fecha=params.get("fecha_hora"),
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

    def delete(self, id_valor_participacion: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_valor_participacion).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el valor participacion con id:  {}".format(id_valor_participacion))
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