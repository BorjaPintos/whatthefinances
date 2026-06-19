import traceback
from typing import List, Tuple, Type

from loguru import logger
from sqlalchemy import func, Subquery, and_, Label, or_, over
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.inversion.dividendos.domain.dividendo_rango import DividendoRango
from src.finanzas.inversion.posiciones.domain.posicion import Posicion
from src.finanzas.inversion.posiciones.domain.posicionrepository import PosicionRepository
from src.finanzas.inversion.bolsa.infrastructure.persistence.orm.bolsaentity import BolsaEntity
from src.finanzas.inversion.broker.infrastructure.persistence.orm.brokerentity import BrokerEntity
from src.finanzas.inversion.dividendos.infrastructure.persistence.orm.dividendoentity import DividendoEntity
from src.finanzas.inversion.posiciones.infrastructure.persistence.orm.posicionentity import PosicionEntity
from src.finanzas.inversion.producto.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.finanzas.inversion.valorparticipacion.infrastructure.persistence.orm.valorparticipacionentity import ValorParticipacionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class PosicionRepositorySQLAlchemy(ITransactionalRepository, PosicionRepository):

    def __get_subquery_valor_participacion(self) -> Subquery:

        subquery = (
            self._session.query(
                ValorParticipacionEntity.isin,
                ValorParticipacionEntity.fecha,
                ValorParticipacionEntity.valor,
                func.row_number().over(
                    partition_by=ValorParticipacionEntity.isin,
                    order_by=[
                        ValorParticipacionEntity.fecha.desc(),
                        ValorParticipacionEntity.id.desc()
                    ]
                ).label('rn')
            )
            .subquery()
        )

        result = (
            self._session.query(
                subquery.c.isin,
                subquery.c.fecha,
                subquery.c.valor
            )
            .filter(subquery.c.rn == 1)
        )

        return result.subquery()

    def __get_subquery_dividendo(self, alias: Type[PosicionEntity]) -> Label:
        columnas = (
            func.sum(DividendoEntity.dividendo_por_participacion),
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

    def __get_subquery_retencion(self, alias: Type[PosicionEntity]) -> Label:
        columnas = (
            func.sum(DividendoEntity.retencion_por_participacion),
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

        alias_posicion = PosicionEntity
        subquery_valor = self.__get_subquery_valor_participacion()
        dividendo_label = self.__get_subquery_dividendo(alias_posicion)
        retencion_label = self.__get_subquery_retencion(alias_posicion)

        columnas = (
            alias_posicion.id, ProductoEntity.nombre, alias_posicion.isin,
            alias_posicion.fecha_compra, alias_posicion.fecha_venta,
            alias_posicion.numero_participaciones, alias_posicion.id_bolsa, alias_posicion.id_broker,
            alias_posicion.precio_compra_sin_comision, alias_posicion.precio_venta_sin_comision,
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
    def __get_posicion_participacion_from_complete_join_row(row) -> Posicion:
        params = {"id": row[0],
                  "nombre": row[1],
                  "isin": row[2],
                  "fecha_compra": row[3],
                  "fecha_venta": row[4],
                  "numero_participaciones": row[5],
                  "id_bolsa": row[6],
                  "id_broker": row[7],
                  "precio_compra_sin_comision": row[8],
                  "precio_venta_sin_comision": row[9],
                  "comision_compra": row[10],
                  "otras_comisiones": row[11],
                  "comision_venta": row[12],
                  "abierta": row[13],
                  "nombre_bolsa": row[14],
                  "nombre_broker": row[15],
                  "valor_participacion": row[16],
                  "dividendos_por_participacion": row[17],
                  "retencion_por_participacion": row[18]
                  }
        return Posicion(params)

    def __get_complete_pagination_join_query(self, criteria: Criteria) -> Query:
        query = self.__get_complete_join_query(criteria)
        return query.offset(criteria.offset()).limit(criteria.limit())

    def list(self, criteria: Criteria) -> Tuple[List[Posicion], int]:
        elements = []
        try:
            query_elements = self.__get_complete_pagination_join_query(criteria)
            result = query_elements.all()
            n_elements = min(len(result), criteria.limit())
            if result is not None:
                for i in range(n_elements):
                    elements.append(self.__get_posicion_participacion_from_complete_join_row(result[i]))

            open_isins_brokers = list(set((p.get_isin(), p.get_id_broker()) for p in elements if p.is_abierta()))
            oldest_open_ids = self._get_oldest_open_ids_by_isin_and_broker(open_isins_brokers)
            for p in elements:
                if p.is_abierta():
                    if p.get_id_broker() is None:
                        p.set_es_cerrable(True)
                    else:
                        p.set_es_cerrable(oldest_open_ids.get((p.get_isin(), p.get_id_broker())) == p.get_id())
                else:
                    p.set_es_cerrable(False)

            return elements, self.count(criteria)
        except Exception as e:
            traceback.print_exc()

        return elements, 0


    def count(self, criteria: Criteria) -> int:
        try:
            query_builder = SQLAlchemyQueryBuilder(PosicionEntity, self._session)
            query = query_builder.build_order_query(criteria)
            return query.count()
        except Exception as e:
            traceback.print_exc()
        return 0

    def get(self, id_posicion: int) -> Posicion:
        try:
            query = self.__get_complete_join_query(
                Criteria(filter=SimpleFilter("id", WhereOperator.IS, id_posicion)))
            result = query.one_or_none()
            if result is None:
                raise NotFoundError("No se encuentra la Posicion con id:  {}".format(id_posicion))
            else:
                posicion = self.__get_posicion_participacion_from_complete_join_row(result)
                if posicion.is_abierta():
                    if posicion.get_id_broker() is None:
                        posicion.set_es_cerrable(True)
                    else:
                        oldest_open_ids = self._get_oldest_open_ids_by_isin_and_broker(
                            [(posicion.get_isin(), posicion.get_id_broker())])
                        posicion.set_es_cerrable(
                            oldest_open_ids.get((posicion.get_isin(), posicion.get_id_broker())) == posicion.get_id())
                else:
                    posicion.set_es_cerrable(False)
                return posicion
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def new(self, params: dict) -> Posicion:
        try:
            self.check_isin(params.get("isin"))
            self.check_broker(params.get("id_broker"))
            self.check_bolsa(params.get("id_bolsa"))

            entity = PosicionEntity(
                isin=params.get("isin"),
                fecha_compra=params.get("fecha_compra"),
                numero_participaciones=params.get("numero_participaciones"),
                id_bolsa=params.get("id_bolsa"),
                id_broker=params.get("id_broker"),
                precio_compra_sin_comision=params.get("precio_compra_sin_comision"),
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

    def update(self, posicion: Posicion) -> bool:
        try:

            self.check_isin(posicion.get_isin())
            self.check_broker(posicion.get_id_broker())
            self.check_bolsa(posicion.get_id_bolsa())

            query_builder = SQLAlchemyQueryBuilder(PosicionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=posicion.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la Posicion con id:  {}".format(posicion.get_id()))
            else:
                entity.update(posicion)
                return True
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return False

    def delete(self, id_posicion: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(PosicionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_posicion).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la Posicion con id:  {}".format(id_posicion))
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

    def get_oldest_open_by_isin_and_broker(self, isin: str, id_broker: int) -> Posicion:
        try:
            query_builder = SQLAlchemyQueryBuilder(PosicionEntity, self._session).build_base_query()
            query = query_builder.filter(
                PosicionEntity.isin == isin,
                PosicionEntity.abierta == True
            )
            if id_broker is not None:
                query = query.filter(PosicionEntity.id_broker == id_broker)
            entity = query.order_by(PosicionEntity.fecha_compra.asc()).first()
            if entity is None:
                return None
            return entity.convert_to_object_domain()
        except Exception as e:
            traceback.print_exc()
        return None

    def _get_oldest_open_ids_by_isin_and_broker(self, isins_brokers: list) -> dict:
        if not isins_brokers:
            return {}
        try:
            query = (self._session.query(
                PosicionEntity.isin,
                PosicionEntity.id_broker,
                func.min(PosicionEntity.id).label('oldest_id')
            ).filter(
                PosicionEntity.isin.in_([ib[0] for ib in isins_brokers]),
                PosicionEntity.abierta == True
            ).group_by(PosicionEntity.isin, PosicionEntity.id_broker).subquery())
            result = self._session.query(query).all()
            return {(row[0], row[1]): row[2] for row in result}
        except Exception as e:
            traceback.print_exc()
        return {}

    def check_isin(self, isin: str):
        if isin is not None:
            query_builder = SQLAlchemyQueryBuilder(ProductoEntity, self._session).build_base_query()
            producto_entity = query_builder.filter_by(isin=isin).one_or_none()
            if producto_entity is None:
                raise NotFoundError("No se encuentra el producto con isin:  {}".format(isin))
