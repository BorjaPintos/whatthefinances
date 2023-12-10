import traceback
from typing import List
from sqlalchemy import func
from src.finanzas.domain.resumenrepository import ResumenRepository
from src.finanzas.infrastructure.persistence.operationsorderdefault import OperationsOrderDefault
from src.finanzas.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class ResumenRepositorySQLAlchemy(ITransactionalRepository, ResumenRepository):

    def ingresos(self, criteria) -> List[dict]:
        elements = []
        try:
            columnas = (
                func.strftime("%Y", OperacionEntity.fecha),
                func.strftime("%m", OperacionEntity.fecha),
                func.sum(OperacionEntity.cantidad),
                OperacionEntity.id_categoria_ingreso,
                CategoriaIngresoEntity.descripcion
            )

            query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session, selected_columns=columnas)
            query = query_builder.build_query(criteria) \
                .join(CategoriaIngresoEntity, OperacionEntity.id_categoria_ingreso == CategoriaIngresoEntity.id,
                      isouter=False)
            query = query.group_by(
                func.strftime("%Y", OperacionEntity.fecha),
                func.strftime("%m", OperacionEntity.fecha),
                OperacionEntity.id_categoria_ingreso)
            query = query.order_by(func.strftime("%Y", OperacionEntity.fecha).desc(),
                           func.strftime("%m", OperacionEntity.fecha).desc(),
                           func.upper(CategoriaIngresoEntity.descripcion).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"año": row[0],
                               "mes": row[1],
                               "total": row[2],
                               "id_categoria_ingreso": row[3],
                               "descripcion_categoria_ingreso": row[4]
                               }
                    elements.append(element)
        except Exception as e:
            traceback.print_exc()

        return elements

    def gastos(self, criteria) -> List[dict]:
        elements = []
        try:
            columnas = (
                func.strftime("%Y", OperacionEntity.fecha),
                func.strftime("%m", OperacionEntity.fecha),
                func.sum(OperacionEntity.cantidad),
                OperacionEntity.id_categoria_gasto,
                CategoriaGastoEntity.descripcion
            )

            query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session, selected_columns=columnas)
            query = query_builder.build_query(criteria) \
                .join(CategoriaGastoEntity, OperacionEntity.id_categoria_gasto == CategoriaGastoEntity.id,
                      isouter=False)
            query = query.group_by(
                func.strftime("%Y", OperacionEntity.fecha),
                func.strftime("%m", OperacionEntity.fecha),
                OperacionEntity.id_categoria_gasto)
            query = query.order_by(func.strftime("%Y", OperacionEntity.fecha).desc(),
                           func.strftime("%m", OperacionEntity.fecha).desc(),
                           func.upper(CategoriaGastoEntity.descripcion).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"año": row[0],
                               "mes": row[1],
                               "total": row[2],
                               "id_categoria_gasto": row[3],
                               "descripcion_categoria_gasto": row[4]
                               }
                    elements.append(element)
        except Exception as e:
            traceback.print_exc()

        return elements
