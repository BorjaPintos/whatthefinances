import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased, Query

from src.finanzas.domain.operacionFavorita import OperacionFavorita
from src.finanzas.domain.operacionfavoritarepository import OperacionFavoritaRepository
from src.finanzas.infrastructure.persistence.operationsorderdefault import OperationsOrderDefault
from src.finanzas.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.finanzas.infrastructure.persistence.orm.operacionfavoritaentity import OperacionFavoritaEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class OperacionFavoritaRepositorySQLAlchemy(ITransactionalRepository, OperacionFavoritaRepository):

    def __get_complete_join_query(self, criteria: Criteria) -> Query:
        CuentaCargo = aliased(CuentaEntity, flat=True)
        CuentaAbono = aliased(CuentaEntity, flat=True)
        MonederoCargo = aliased(MonederoEntity, flat=True)
        MonederoAbono = aliased(MonederoEntity, flat=True)

        columnas = (
            OperacionFavoritaEntity.id, OperacionFavoritaEntity.nombre, OperacionFavoritaEntity.cantidad,
            OperacionFavoritaEntity.descripcion,
            OperacionFavoritaEntity.id_categoria_gasto, CategoriaGastoEntity.descripcion,
            OperacionFavoritaEntity.id_cuenta_cargo, CuentaCargo.nombre,
            OperacionFavoritaEntity.id_monedero_cargo, MonederoCargo.nombre,
            OperacionFavoritaEntity.id_categoria_ingreso, CategoriaIngresoEntity.descripcion,
            OperacionFavoritaEntity.id_cuenta_abono, CuentaAbono.nombre,
            OperacionFavoritaEntity.id_monedero_abono, MonederoAbono.nombre)

        query_builder = SQLAlchemyQueryBuilder(OperacionFavoritaEntity, self._session, selected_columns=columnas)
        query = query_builder.build_order_query(criteria, defaultOrder=OperationsOrderDefault()) \
            .join(CategoriaGastoEntity, OperacionFavoritaEntity.id_categoria_gasto == CategoriaGastoEntity.id,
                  isouter=True) \
            .join(CuentaCargo, OperacionFavoritaEntity.id_cuenta_cargo == CuentaCargo.id, isouter=True) \
            .join(MonederoCargo, OperacionFavoritaEntity.id_monedero_cargo == MonederoCargo.id, isouter=True) \
            .join(CategoriaIngresoEntity, OperacionFavoritaEntity.id_categoria_ingreso == CategoriaIngresoEntity.id,
                  isouter=True) \
            .join(CuentaAbono, OperacionFavoritaEntity.id_cuenta_abono == CuentaAbono.id, isouter=True) \
            .join(MonederoAbono, OperacionFavoritaEntity.id_monedero_abono == MonederoAbono.id, isouter=True)
        return query

    @staticmethod
    def __get_operation_favorita_from_complete_join_row(row) -> OperacionFavorita:
        params = {"id": row[0],
                  "nombre": row[1],
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
        return OperacionFavorita(params)

    def list(self, criteria: Criteria) -> List[OperacionFavorita]:
        elements = []
        try:
            query_elements = self.__get_complete_join_query(criteria)
            result = query_elements.all()
            if result is not None:
                for i in result:
                    elements.append(self.__get_operation_favorita_from_complete_join_row(result[i]))
            return elements
        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> int:
        try:

            self.check_cuenta(params.get("id_cuenta_cargo"))
            self.check_cuenta(params.get("id_cuenta_abono"))
            self.check_monedero(params.get("id_monedero_cargo"))
            self.check_monedero(params.get("id_monedero_abono"))
            self.check_categoria_ingreso(params.get("id_categoria_ingreso"))
            self.check_categoria_gasto(params.get("id_categoria_gasto"))

            entity = OperacionFavoritaEntity(nombre=params.get("nombre"),
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

    def delete(self, id_operacion_favorita: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(OperacionFavoritaEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_operacion_favorita).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la operación favorita con id:  {}".format(id_operacion_favorita))
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
