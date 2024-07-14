import traceback
from typing import List

from loguru import logger
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.inversion.dividendos.domain.dividendo import Dividendo
from src.finanzas.inversion.dividendos.domain.dividendo_rango import DividendoRango
from src.finanzas.inversion.dividendos.domain.dividendorepository import DividendoRepository
from src.finanzas.inversion.dividendos.infrastructure.persistence.orm.dividendoentity import DividendoEntity
from src.finanzas.inversion.posiciones.infrastructure.persistence.orm.posicionentity import PosicionEntity
from src.finanzas.inversion.producto.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class DividendoRepositorySQLAlchemy(ITransactionalRepository, DividendoRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:
        columnas = (
            DividendoEntity.id, DividendoEntity.isin, DividendoEntity.fecha,
            DividendoEntity.dividendo_por_participacion, DividendoEntity.retencion_por_participacion, ProductoEntity.nombre
        )

        query_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria) \
            .join(ProductoEntity, DividendoEntity.isin == ProductoEntity.isin, isouter=False)
        return query

    @staticmethod
    def __get_dividendo_from_complete_join_row(row) -> Dividendo:
        params = {"id": row[0],
                  "isin": row[1],
                  "fecha": row[2],
                  "dividendo_por_participacion": row[3],
                  "retencion_por_participacion": row[4],
                  "nombre": row[5],
                  }
        return Dividendo(params)

    def list(self, criteria: Criteria) -> List[Dividendo]:
        elements = []
        try:
            query = self.__get_complete_join_query(criteria)
            result = query.all()

            if result is not None:
                for row in result:
                    elements.append(self.__get_dividendo_from_complete_join_row(row))

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> Dividendo:
        try:
            self.check_isin(params.get("isin"))
            entity = DividendoEntity(fecha=params.get("fecha"),
                                     isin=params.get("isin"),
                                     dividendo_por_participacion=params.get("dividendo_por_participacion"),
                                     retencion_por_participacion=params.get("retencion_por_participacion"))
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
            self.check_isin(dividendo.get_isin())
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

    def check_isin(self, isin: str):
        if isin is not None:
            query_builder = SQLAlchemyQueryBuilder(ProductoEntity, self._session).build_base_query()
            producto_entity = query_builder.filter_by(isin=isin).one_or_none()
            if producto_entity is None:
                raise NotFoundError("No se encuentra el producto con isin:  {}".format(isin))

    @staticmethod
    def __get_dividendo_rango_from_complete_join_row(row) -> DividendoRango:
        params = {"isin": row[0],
                  "dividendo": row[1],
                  "retencion": row[2]
                  }
        return DividendoRango(params)

    def __get_join_query_dividendo_rango(self, criteria: Criteria) -> Query:

        columnas = (
            PosicionEntity.isin,
            func.sum(DividendoEntity.dividendo_por_participacion * PosicionEntity.numero_participaciones),
            func.sum(DividendoEntity.retencion_por_participacion * PosicionEntity.numero_participaciones)
        )
        query_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session, selected_columns=columnas)
        query = query_builder.build_query(criteria) \
            .join(PosicionEntity, DividendoEntity.isin == PosicionEntity.isin) \
            .where(DividendoEntity.fecha > PosicionEntity.fecha_compra) \
            .where(or_(PosicionEntity.abierta == True, and_(PosicionEntity.abierta == False,
                                                            DividendoEntity.fecha < PosicionEntity.fecha_venta))) \
            .group_by(PosicionEntity.isin)

        return query

    def dividendo_rango(self, criteria: Criteria) -> List[DividendoRango]:
        elements = []
        try:
            query_elements = self.__get_join_query_dividendo_rango(criteria)
            result = query_elements.all()
            n_elements = min(len(result), criteria.limit())
            if result is not None:
                for i in range(n_elements):
                    elements.append(self.__get_dividendo_rango_from_complete_join_row(result[i]))
            return elements
        except Exception as e:
            traceback.print_exc()

        return elements