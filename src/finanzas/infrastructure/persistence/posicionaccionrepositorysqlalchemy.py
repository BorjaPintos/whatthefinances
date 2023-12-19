import traceback
from typing import List, Tuple

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from src.finanzas.domain.posicionaccion import PosicionAccion
from src.finanzas.domain.posicionaccionrepository import PosicionAccionRepository
from src.finanzas.infrastructure.persistence.orm.bolsaentity import BolsaEntity
from src.finanzas.infrastructure.persistence.orm.brokerentity import BrokerEntity
from src.finanzas.infrastructure.persistence.orm.posicionaccionentity import PosicionAccionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class PosicionAccionRepositorySQLAlchemy(ITransactionalRepository, PosicionAccionRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:

        columnas = (
            PosicionAccionEntity.id, PosicionAccionEntity.nombre, PosicionAccionEntity.isin,
            PosicionAccionEntity.fecha_compra, PosicionAccionEntity.fecha_venta,
            PosicionAccionEntity.numero_acciones, PosicionAccionEntity.id_bolsa, PosicionAccionEntity.id_broker,
            PosicionAccionEntity.precio_accion_sin_comision, PosicionAccionEntity.precio_venta_sin_comision,
            PosicionAccionEntity.comision_compra, PosicionAccionEntity.otras_comisiones,
            PosicionAccionEntity.comision_venta, PosicionAccionEntity.abierta,
            BolsaEntity.nombre, BrokerEntity.nombre
        )

        query_builder = SQLAlchemyQueryBuilder(PosicionAccionEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria) \
            .join(BrokerEntity, PosicionAccionEntity.id_broker == BrokerEntity.id, isouter=False) \
            .join(BolsaEntity, PosicionAccionEntity.id_bolsa == BolsaEntity.id, isouter=True)

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
            query = self.__get_complete_join_query(Criteria(filter=SimpleFilter("id", WhereOperator.IS, id_posicion_accion)))
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

            self.check_broker(params.get("id_broker"))
            self.check_bolsa(params.get("id_bolsa"))

            entity = PosicionAccionEntity(
                nombre=params.get("nombre"),
                isin=params.get("isin"),
                fecha_compra=params.get("fecha_compra"),
                numero_acciones=params.get("numero_acciones"),
                id_bolsa=params.get("id_bolsa"),
                id_broker=params.get("id_broker"),
                precio_accion_sin_comision=params.get("precio_accion_sin_comision"),
                comision_compra=params.get("comision_compra"),
                otras_comisiones=params.get("otras_comisiones")
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