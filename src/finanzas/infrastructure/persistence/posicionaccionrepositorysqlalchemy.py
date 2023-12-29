import traceback
from typing import List, Tuple, Type

from loguru import logger
from sqlalchemy import func, Subquery, and_, Label, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.domain.dividendo_rango import DividendoRango
from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.finanzas.infrastructure.persistence.orm.bolsaentity import BolsaEntity
from src.finanzas.infrastructure.persistence.orm.brokerentity import BrokerEntity
from src.finanzas.infrastructure.persistence.orm.dividendoentity import DividendoEntity
from src.finanzas.infrastructure.persistence.orm.posicionaccionentity import PosicionAccionEntity
from src.finanzas.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.finanzas.infrastructure.persistence.orm.valoraccionentity import ValorAccionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class PosicionAccionRepositorySQLAlchemy(ITransactionalRepository, PosicionAccionRepository):

    def __get_subquery_valor_accion(self) -> Subquery:

        """
        select fvc.isin, fvc.fecha, fvc.valor
        FROM finanzas_valor_acciones fvc
        join (SELECT fac.isin AS isin, max(fac.fecha) AS max_1 FROM finanzas_valor_acciones fac GROUP BY fac.isin) fvc2
        on fvc.isin = fvc2.isin and fvc.fecha = fvc2.max_1
        """

        columnas = (ValorAccionEntity.isin, func.max(ValorAccionEntity.fecha))
        subquery_builder = SQLAlchemyQueryBuilder(ValorAccionEntity, self._session, selected_columns=columnas)
        subquery = subquery_builder.build_query(Criteria())
        subquery = subquery.group_by(ValorAccionEntity.isin).subquery()

        columnas2 = (ValorAccionEntity.isin, ValorAccionEntity.fecha, ValorAccionEntity.valor)
        subquery_builder2 = SQLAlchemyQueryBuilder(ValorAccionEntity, self._session, selected_columns=columnas2)
        subquery2 = (subquery_builder2.build_query(Criteria())
                     .join(subquery, and_(ValorAccionEntity.isin == subquery.columns[0],
                                          ValorAccionEntity.fecha == subquery.columns[1]), isouter=False))

        return subquery2.subquery()

    def __get_subquery_dividendo(self, alias: Type[PosicionAccionEntity]) -> Label:
        columnas = (
            func.sum(DividendoEntity.dividendo_por_accion),
        )
        subquery_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session, selected_columns=columnas)
        subquery = ((subquery_builder.build_query(Criteria())).
                    where(or_(and_(DividendoEntity.fecha > alias.fecha_compra,
                                   DividendoEntity.isin == alias.isin,
                                   alias.abierta == True),
                              and_(DividendoEntity.fecha > alias.fecha_compra,
                                   DividendoEntity.fecha < alias.fecha_venta,
                                   DividendoEntity.isin == alias.isin,
                                   alias.abierta == False)
                              )
                          ))
        return subquery.label('dividendo')

    def __get_subquery_retencion(self, alias: Type[PosicionAccionEntity]) -> Label:
        columnas = (
            func.sum(DividendoEntity.retencion_por_accion),
        )
        subquery_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session, selected_columns=columnas)
        subquery = ((subquery_builder.build_query(Criteria())).
                    where(or_(and_(DividendoEntity.fecha > alias.fecha_compra,
                                   DividendoEntity.isin == alias.isin,
                                   alias.abierta == True),
                              and_(DividendoEntity.fecha > alias.fecha_compra,
                                   DividendoEntity.fecha < alias.fecha_venta,
                                   DividendoEntity.isin == alias.isin,
                                   alias.abierta == False)
                              )
                          ))
        return subquery.label('retencion')

    def __get_complete_join_query(self, criteria: Criteria) -> Query:

        alias_posicion = PosicionAccionEntity
        subquery_valor = self.__get_subquery_valor_accion()
        dividendo_label = self.__get_subquery_dividendo(alias_posicion)
        retencion_label = self.__get_subquery_retencion(alias_posicion)

        columnas = (
            alias_posicion.id, ProductoEntity.nombre, alias_posicion.isin,
            alias_posicion.fecha_compra, alias_posicion.fecha_venta,
            alias_posicion.numero_acciones, alias_posicion.id_bolsa, alias_posicion.id_broker,
            alias_posicion.precio_accion_sin_comision, alias_posicion.precio_venta_sin_comision,
            alias_posicion.comision_compra, alias_posicion.otras_comisiones,
            alias_posicion.comision_venta, alias_posicion.abierta,
            BolsaEntity.nombre, BrokerEntity.nombre, subquery_valor.columns[2],
            dividendo_label, retencion_label
        )

        query_builder = SQLAlchemyQueryBuilder(alias_posicion, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria) \
            .join(ProductoEntity, alias_posicion.isin == ProductoEntity.isin, isouter=False) \
            .join(BrokerEntity, alias_posicion.id_broker == BrokerEntity.id, isouter=False) \
            .join(BolsaEntity, alias_posicion.id_bolsa == BolsaEntity.id, isouter=False) \
            .join(subquery_valor, alias_posicion.isin == subquery_valor.columns[0], isouter=True)

        return query

    @staticmethod
    def __get_posicion_accion_from_complete_join_row(row) -> PosicionAccion:
        params = {"id": row[0],
                  "nombre": row[1],
                  "isin": row[2],
                  "fecha_compra": row[3],
                  "fecha_venta": row[4],
                  "numero_acciones": row[5],
                  "id_bolsa": row[6],
                  "id_broker": row[7],
                  "precio_accion_sin_comision": row[8],
                  "precio_venta_sin_comision": row[9],
                  "comision_compra": row[10],
                  "otras_comisiones": row[11],
                  "comision_venta": row[12],
                  "abierta": row[13],
                  "nombre_bolsa": row[14],
                  "nombre_broker": row[15],
                  "valor_accion": row[16],
                  "dividendos_por_accion": row[17],
                  "retencion_por_accion": row[18]
                  }
        return PosicionAccion(params)

    def __get_complete_pagination_join_query(self, criteria: Criteria) -> Query:
        query = self.__get_complete_join_query(criteria)
        return query.offset(criteria.offset()).limit(criteria.limit())

    def list(self, criteria: Criteria) -> Tuple[List[PosicionAccion], int]:
        elements = []
        try:
            query_elements = self.__get_complete_pagination_join_query(criteria)
            result = query_elements.all()
            n_elements = min(len(result), criteria.limit())
            if result is not None:
                for i in range(n_elements):
                    elements.append(self.__get_posicion_accion_from_complete_join_row(result[i]))
            return elements, self.count(criteria)
        except Exception as e:
            traceback.print_exc()

        return elements, 0

    @staticmethod
    def __get_dividendo_rango_from_complete_join_row(row) -> DividendoRango:
        params = {"isin": row[0],
                  "dividendo": row[1],
                  "retencion": row[2]
                  }
        return DividendoRango(params)

    def __get_join_query_dividendo_rango(self, criteria: Criteria) -> Query:

        columnas = (
            PosicionAccionEntity.isin,
            func.sum(DividendoEntity.dividendo_por_accion * PosicionAccionEntity.numero_acciones),
            func.sum(DividendoEntity.retencion_por_accion * PosicionAccionEntity.numero_acciones)
        )
        query_builder = SQLAlchemyQueryBuilder(DividendoEntity, self._session, selected_columns=columnas)
        query = query_builder.build_query(criteria) \
            .join(PosicionAccionEntity, DividendoEntity.isin == PosicionAccionEntity.isin) \
            .where(DividendoEntity.fecha > PosicionAccionEntity.fecha_compra) \
            .where(or_(PosicionAccionEntity.abierta == True, and_(PosicionAccionEntity.abierta == False,
                                                                  DividendoEntity.fecha < PosicionAccionEntity.fecha_venta))) \
            .group_by(PosicionAccionEntity.isin)

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

    def count(self, criteria: Criteria) -> int:
        try:
            query_builder = SQLAlchemyQueryBuilder(PosicionAccionEntity, self._session)
            query = query_builder.build_order_query(criteria)
            return query.count()
        except Exception as e:
            traceback.print_exc()
        return 0

    def get(self, id_posicion_accion: int) -> PosicionAccion:
        try:
            query = self.__get_complete_join_query(
                Criteria(filter=SimpleFilter("id", WhereOperator.IS, id_posicion_accion)))
            result = query.one_or_none()
            if result is None:
                raise NotFoundError("No se encuentra la PosicionAccion con id:  {}".format(id_posicion_accion))
            else:
                return self.__get_posicion_accion_from_complete_join_row(result)
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def new(self, params: dict) -> PosicionAccion:
        try:
            self.check_isin(params.get("isin"))
            self.check_broker(params.get("id_broker"))
            self.check_bolsa(params.get("id_bolsa"))

            entity = PosicionAccionEntity(
                isin=params.get("isin"),
                fecha_compra=params.get("fecha_compra"),
                numero_acciones=params.get("numero_acciones"),
                id_bolsa=params.get("id_bolsa"),
                id_broker=params.get("id_broker"),
                precio_accion_sin_comision=params.get("precio_accion_sin_comision"),
                comision_compra=params.get("comision_compra"),
                otras_comisiones=params.get("otras_comisiones"),
                abierta=params.get("abierta")
            )
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

    def update(self, posicion_accion: PosicionAccion) -> bool:
        try:

            self.check_isin(posicion_accion.get_isin())
            self.check_broker(posicion_accion.get_id_broker())
            self.check_bolsa(posicion_accion.get_id_bolsa())

            query_builder = SQLAlchemyQueryBuilder(PosicionAccionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=posicion_accion.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la PosicionAccion con id:  {}".format(posicion_accion.get_id()))
            else:
                entity.update(posicion_accion)
                return True
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return False

    def delete(self, id_posicion_accion: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(PosicionAccionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_posicion_accion).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la PosicionAccion con id:  {}".format(id_posicion_accion))
            self._session.delete(entity)
            return True
        except Exception as e:
            traceback.print_exc()
        return False

    def check_broker(self, id_broker: int):
        if id_broker is not None:
            query_builder = SQLAlchemyQueryBuilder(BrokerEntity, self._session).build_base_query()
            broker_entity = query_builder.filter_by(id=id_broker).one_or_none()
            if broker_entity is None:
                raise NotFoundError("No se encuentra el broker con id:  {}".format(id_broker))

    def check_bolsa(self, id_bolsa: int):
        if id_bolsa is not None:
            query_builder = SQLAlchemyQueryBuilder(BolsaEntity, self._session).build_base_query()
            bolsa_entity = query_builder.filter_by(id=id_bolsa).one_or_none()
            if bolsa_entity is None:
                raise NotFoundError("No se encuentra la bolsa con id:  {}".format(id_bolsa))

    def check_isin(self, isin: str):
        if isin is not None:
            query_builder = SQLAlchemyQueryBuilder(ProductoEntity, self._session).build_base_query()
            producto_entity = query_builder.filter_by(isin=isin).one_or_none()
            if producto_entity is None:
                raise NotFoundError("No se encuentra el producto con isin:  {}".format(isin))
