import traceback
from typing import List
from sqlalchemy import func

from src.finanzas.domain.resumencuenta import ResumenCuenta
from src.finanzas.domain.resumengasto import ResumenGasto
from src.finanzas.domain.resumeningreso import ResumenIngreso
from src.finanzas.domain.resumenmonedero import ResumenMonedero
from src.finanzas.domain.resumenrepository import ResumenRepository
from src.finanzas.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.finanzas.infrastructure.persistence.orm.movimientocuentaentity import MovimientoCuentaEntity
from src.finanzas.infrastructure.persistence.orm.movimientomonederoentity import MovimientoMonederoEntity
from src.finanzas.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.persistence.application.databasemanager import DatabaseManager
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class ResumenRepositorySQLAlchemy(ITransactionalRepository, ResumenRepository):

    def ingresos(self, criteria) -> List[ResumenIngreso]:
        elements = []
        try:
            columnas = (
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                func.sum(OperacionEntity.cantidad),
                OperacionEntity.id_categoria_ingreso,
                CategoriaIngresoEntity.descripcion
            )

            query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session, selected_columns=columnas)
            query = query_builder.build_query(criteria) \
                .join(CategoriaIngresoEntity, OperacionEntity.id_categoria_ingreso == CategoriaIngresoEntity.id,
                      isouter=False)
            query = query.group_by(
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                OperacionEntity.id_categoria_ingreso,
                CategoriaIngresoEntity.descripcion)
            query = query.order_by(DatabaseManager.get_database().year(OperacionEntity.fecha).desc(),
                                   DatabaseManager.get_database().month(OperacionEntity.fecha).desc(),
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
                    elements.append(ResumenIngreso(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def gastos(self, criteria) -> List[ResumenGasto]:
        elements = []
        try:
            columnas = (
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                func.sum(OperacionEntity.cantidad),
                OperacionEntity.id_categoria_gasto,
                CategoriaGastoEntity.descripcion
            )

            query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session, selected_columns=columnas)
            query = query_builder.build_query(criteria) \
                .join(CategoriaGastoEntity, OperacionEntity.id_categoria_gasto == CategoriaGastoEntity.id,
                      isouter=False)
            query = query.group_by(
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                OperacionEntity.id_categoria_gasto,
                CategoriaGastoEntity.descripcion)
            query = query.order_by(DatabaseManager.get_database().year(OperacionEntity.fecha).desc(),
                                   DatabaseManager.get_database().month(OperacionEntity.fecha).desc(),
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
                    elements.append(ResumenGasto(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def cuentas(self, criteria) -> List[ResumenCuenta]:
        elements = []
        try:
            columnas = (
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                func.sum(MovimientoCuentaEntity.cantidad),
                MovimientoCuentaEntity.id_cuenta,
                CuentaEntity.nombre
            )

            query_builder = SQLAlchemyQueryBuilder(MovimientoCuentaEntity, self._session, selected_columns=columnas)
            query = query_builder.build_query(criteria) \
                .join(OperacionEntity, MovimientoCuentaEntity.id_operacion == OperacionEntity.id, isouter=True) \
                .join(CuentaEntity, MovimientoCuentaEntity.id_cuenta == CuentaEntity.id, isouter=True)
            query = query.group_by(
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                MovimientoCuentaEntity.id_cuenta,
                CuentaEntity.nombre)
            query = query.order_by(DatabaseManager.get_database().year(OperacionEntity.fecha).desc(),
                                   DatabaseManager.get_database().month(OperacionEntity.fecha).desc(),
                                   func.upper(CuentaEntity.nombre).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"año": row[0],
                               "mes": row[1],
                               "total": row[2],
                               "id_cuenta": row[3],
                               "nombre_cuenta": row[4]
                               }
                    elements.append(ResumenCuenta(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def monederos(self, criteria) -> List[ResumenMonedero]:
        elements = []
        try:
            columnas = (
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                func.sum(MovimientoMonederoEntity.cantidad),
                MovimientoMonederoEntity.id_monedero,
                MonederoEntity.nombre
            )

            query_builder = SQLAlchemyQueryBuilder(MovimientoMonederoEntity, self._session, selected_columns=columnas)
            query = query_builder.build_query(criteria) \
                .join(OperacionEntity, MovimientoMonederoEntity.id_operacion == OperacionEntity.id, isouter=True) \
                .join(MonederoEntity, MovimientoMonederoEntity.id_monedero == MonederoEntity.id, isouter=True)
            query = query.group_by(
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                MovimientoMonederoEntity.id_monedero,
                MonederoEntity.nombre)
            query = query.order_by(DatabaseManager.get_database().year(OperacionEntity.fecha).desc(),
                                   DatabaseManager.get_database().month(OperacionEntity.fecha).desc(),
                                   func.upper(MonederoEntity.nombre).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"año": row[0],
                               "mes": row[1],
                               "total": row[2],
                               "id_monedero": row[3],
                               "nombre_monedero": row[4]
                               }
                    elements.append(ResumenMonedero(element))
        except Exception as e:
            traceback.print_exc()

        return elements