import traceback
from typing import List, Tuple

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased, Query

from src.finanzas.operaciones.domain.operacion import Operacion
from src.finanzas.operaciones.domain.operacionrepository import OperacionRepository
from src.finanzas.operaciones.infrastructure.persistence.operationsorderdefault import OperationsOrderDefault
from src.finanzas.categorias.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.categorias.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.cuentas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.monederos.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.finanzas.operaciones.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.domain.simplefilter import SimpleFilter, WhereOperator
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class OperacionRepositorySQLAlchemy(ITransactionalRepository, OperacionRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:
        CuentaCargo = aliased(CuentaEntity, flat=True)
        CuentaAbono = aliased(CuentaEntity, flat=True)
        MonederoCargo = aliased(MonederoEntity, flat=True)
        MonederoAbono = aliased(MonederoEntity, flat=True)

        columnas = (
            OperacionEntity.id, OperacionEntity.fecha, OperacionEntity.cantidad, OperacionEntity.descripcion,
            OperacionEntity.id_categoria_gasto, CategoriaGastoEntity.descripcion,
            OperacionEntity.id_cuenta_cargo, CuentaCargo.nombre,
            OperacionEntity.id_monedero_cargo, MonederoCargo.nombre,
            OperacionEntity.id_categoria_ingreso, CategoriaIngresoEntity.descripcion,
            OperacionEntity.id_cuenta_abono, CuentaAbono.nombre,
            OperacionEntity.id_monedero_abono, MonederoAbono.nombre)

        query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria, defaultOrder=OperationsOrderDefault()) \
            .join(CategoriaGastoEntity, OperacionEntity.id_categoria_gasto == CategoriaGastoEntity.id, isouter=True) \
            .join(CuentaCargo, OperacionEntity.id_cuenta_cargo == CuentaCargo.id, isouter=True) \
            .join(MonederoCargo, OperacionEntity.id_monedero_cargo == MonederoCargo.id, isouter=True) \
            .join(CategoriaIngresoEntity, OperacionEntity.id_categoria_ingreso == CategoriaIngresoEntity.id,
                  isouter=True) \
            .join(CuentaAbono, OperacionEntity.id_cuenta_abono == CuentaAbono.id, isouter=True) \
            .join(MonederoAbono, OperacionEntity.id_monedero_abono == MonederoAbono.id, isouter=True)
        return query

    def __get_complete_pagination_join_query(self, criteria: Criteria) -> Query:
        query = self.__get_complete_join_query(criteria)
        return query.offset(criteria.offset()).limit(criteria.limit())

    @staticmethod
    def __get_operation_from_complete_join_row(row) -> Operacion:
        params = {"id": row[0],
                  "fecha": row[1],
                  "cantidad": row[2],
                  "descripcion": row[3],
                  "id_categoria_gasto": row[4],
                  "descripcion_categoria_gasto": row[5],
                  "id_cuenta_cargo": row[6],
                  "nombre_cuenta_cargo": row[7],
                  "id_monedero_cargo": row[8],
                  "nombre_monedero_cargo": row[9],
                  "id_categoria_ingreso": row[10],
                  "descripcion_categoria_ingreso": row[11],
                  "id_cuenta_abono": row[12],
                  "nombre_cuenta_abono": row[13],
                  "id_monedero_abono": row[14],
                  "nombre_monedero_abono": row[15]
                  }
        return Operacion(params)

    def list(self, criteria: Criteria) -> Tuple[List[Operacion], int]:
        elements = []
        try:
            query_elements = self.__get_complete_pagination_join_query(criteria)
            result = query_elements.all()
            n_elements = min(len(result), criteria.limit())
            if result is not None:
                for i in range(n_elements):
                    elements.append(self.__get_operation_from_complete_join_row(result[i]))
            return elements, self.count(criteria)
        except Exception as e:
            traceback.print_exc()

        return elements, 0

    def get(self, id_operacion: int) -> Operacion:
        try:

            query = self.__get_complete_join_query(Criteria(filter=SimpleFilter("id", WhereOperator.IS, id_operacion)))
            result = query.one_or_none()
            if result is None:
                raise NotFoundError("No se encuentra la operación con id:  {}".format(id_operacion))
            else:
                return self.__get_operation_from_complete_join_row(result)
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def count(self, criteria: Criteria) -> int:
        try:
            query = self.__get_complete_join_query(criteria)
            return query.count()
        except Exception as e:
            traceback.print_exc()
        return 0

    def new(self, params: dict) -> int:
        try:

            self.check_cuenta(params.get("id_cuenta_cargo"))
            self.check_cuenta(params.get("id_cuenta_abono"))
            self.check_monedero(params.get("id_monedero_cargo"))
            self.check_monedero(params.get("id_monedero_abono"))
            self.check_categoria_ingreso(params.get("id_categoria_ingreso"))
            self.check_categoria_gasto(params.get("id_categoria_gasto"))

            entity = OperacionEntity(fecha=params.get("fecha"),
                                     cantidad=params.get("cantidad"),
                                     descripcion=params.get("descripcion"),
                                     id_categoria_gasto=params.get("id_categoria_gasto"),
                                     id_categoria_ingreso=params.get("id_categoria_ingreso"),
                                     id_cuenta_cargo=params.get("id_cuenta_cargo"),
                                     id_cuenta_abono=params.get("id_cuenta_abono"),
                                     id_monedero_cargo=params.get("id_monedero_cargo"),
                                     id_monedero_abono=params.get("id_monedero_abono"))
            self._session.add(entity)
            self._session.flush()
            return entity.id
        except IntegrityError as e:
            logger.info(e)
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def update(self, operacion: Operacion) -> bool:
        try:
            self.check_cuenta(operacion.get_id_cuenta_cargo())
            self.check_cuenta(operacion.get_id_cuenta_abono())
            self.check_monedero(operacion.get_id_monedero_cargo())
            self.check_monedero(operacion.get_id_monedero_abono())
            self.check_categoria_ingreso(operacion.get_id_categoria_ingreso())
            self.check_categoria_gasto(operacion.get_id_categoria_gasto())

            query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=operacion.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la operation con id:  {}".format(operacion.get_id()))
            else:
                entity.update(operacion)
                return True
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return False

    def delete(self, id_operacion: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_operacion).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la operación con id:  {}".format(id_operacion))
            self._session.delete(entity)
            return True
        except Exception as e:
            traceback.print_exc()
        return False

    def check_cuenta(self, id_cuenta: int):
        if id_cuenta is not None:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session).build_base_query()
            cuenta_entity = query_builder.filter_by(id=id_cuenta).one_or_none()
            if cuenta_entity is None:
                raise NotFoundError("No se encuentra la cuenta con id:  {}".format(id_cuenta))

    def check_monedero(self, id_monedero: int):
        if id_monedero is not None:
            query_builder = SQLAlchemyQueryBuilder(MonederoEntity, self._session).build_base_query()
            monedero_entity = query_builder.filter_by(id=id_monedero).one_or_none()
            if monedero_entity is None:
                raise NotFoundError("No se encuentra el monedero con id:  {}".format(id_monedero))

    def check_categoria_ingreso(self, id_categoria_ingreso: int):
        if id_categoria_ingreso is not None:
            query_builder = SQLAlchemyQueryBuilder(CategoriaIngresoEntity, self._session).build_base_query()
            categoria_ingreso_entity = query_builder.filter_by(id=id_categoria_ingreso).one_or_none()
            if categoria_ingreso_entity is None:
                raise NotFoundError("No se encuentra la categoría ingreso con id:  {}".format(id_categoria_ingreso))

    def check_categoria_gasto(self, id_categoria_gasto: int):
        if id_categoria_gasto is not None:
            query_builder = SQLAlchemyQueryBuilder(CategoriaGastoEntity, self._session).build_base_query()
            categoria_gasto_entity = query_builder.filter_by(id=id_categoria_gasto).one_or_none()
            if categoria_gasto_entity is None:
                raise NotFoundError("No se encuentra la categoría gasto con id:  {}".format(id_categoria_gasto))
