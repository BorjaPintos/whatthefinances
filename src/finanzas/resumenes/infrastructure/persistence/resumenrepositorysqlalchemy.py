import traceback
from typing import List
from sqlalchemy import func, and_

from src.finanzas.resumenes.domain.resumencuenta import ResumenCuenta
from src.finanzas.resumenes.domain.resumengasto import ResumenGasto
from src.finanzas.resumenes.domain.resumeningreso import ResumenIngreso
from src.finanzas.resumenes.domain.resumenmonedero import ResumenMonedero
from src.finanzas.resumenes.domain.resumenrepository import ResumenRepository
from src.finanzas.resumenes.domain.resumentotal import ResumenTotal
from src.finanzas.resumenes.domain.resumenvalorparticipacion import ResumenValorParticipacion
from src.finanzas.categorias.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.categorias.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.cuentas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.monederos.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.finanzas.cuentas.infrastructure.persistence.orm.movimientocuentaentity import MovimientoCuentaEntity
from src.finanzas.monederos.infrastructure.persistence.orm.movimientomonederoentity import MovimientoMonederoEntity
from src.finanzas.operaciones.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.finanzas.inversion.valorparticipacion.infrastructure.persistence.orm.valorparticipacionentity import ValorParticipacionEntity
from src.persistence.application.databasemanager import DatabaseManager
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class ResumenRepositorySQLAlchemy(ITransactionalRepository, ResumenRepository):

    def ingresos(self, criteria: Criteria) -> List[ResumenIngreso]:
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
                    element = {"año": int(row[0]),
                               "mes": int(row[1]),
                               "total": float(row[2]),
                               "id_categoria_ingreso": int(row[3]),
                               "descripcion_categoria_ingreso": row[4]
                               }
                    elements.append(ResumenIngreso(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def gastos(self, criteria: Criteria) -> List[ResumenGasto]:
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
                    element = {"año": int(row[0]),
                               "mes": int(row[1]),
                               "total": float(row[2]),
                               "id_categoria_gasto": int(row[3]),
                               "descripcion_categoria_gasto": row[4]
                               }
                    elements.append(ResumenGasto(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def cuentas(self, criteria: Criteria) -> List[ResumenCuenta]:
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
                    element = {"año": int(row[0]),
                               "mes": int(row[1]),
                               "total": float(row[2]),
                               "id_cuenta": int(row[3]),
                               "nombre_cuenta": row[4]
                               }
                    elements.append(ResumenCuenta(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def monederos(self, criteria: Criteria) -> List[ResumenMonedero]:
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
                    element = {"año": int(row[0]),
                               "mes": int(row[1]),
                               "total": float(row[2]),
                               "id_monedero": int(row[3]),
                               "nombre_monedero": row[4]
                               }
                    elements.append(ResumenMonedero(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def total(self, criteria: Criteria) -> List[ResumenTotal]:
        elements = []
        try:
            columnas = (
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha),
                func.sum(MovimientoCuentaEntity.cantidad)
            )

            query_builder = SQLAlchemyQueryBuilder(MovimientoCuentaEntity, self._session, selected_columns=columnas)
            query = query_builder.build_query(criteria) \
                .join(OperacionEntity, MovimientoCuentaEntity.id_operacion == OperacionEntity.id, isouter=True)
            query = query.group_by(
                DatabaseManager.get_database().year(OperacionEntity.fecha),
                DatabaseManager.get_database().month(OperacionEntity.fecha))
            query = query.order_by(DatabaseManager.get_database().year(OperacionEntity.fecha).desc(),
                                   DatabaseManager.get_database().month(OperacionEntity.fecha).desc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"año": int(row[0]),
                               "mes": int(row[1]),
                               "total": float(row[2])
                               }
                    elements.append(ResumenTotal(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def resumen_valor_participacion_meses(self, criteria: Criteria) -> List[ResumenValorParticipacion]:
        elements = []
        try:

            """
            select fvc.year, fvc.month, fvc.fecha, fvc.isin, fvc.valor
            FROM finanzas_valor_participaciones fvc
            join (SELECT fac.isin AS isin, max(fac.fecha) AS max_1, fac.year as year, fac.month as month FROM finanzas_valor_participaciones fac GROUP BY fac.isin, fac.year, fac.month) fvc2
            on fvc.isin = fvc2.isin and fvc.fecha = fvc2.max_1
            """

            columnas = (
                ValorParticipacionEntity.isin,
                func.max(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
            )


            subquery_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session, selected_columns=columnas)
            subquery = subquery_builder.build_query(Criteria())
            subquery = subquery.group_by(
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                ValorParticipacionEntity.isin).subquery()

            columnas2 = (
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                ValorParticipacionEntity.fecha,
                ValorParticipacionEntity.isin,
                ValorParticipacionEntity.valor
            )
            query_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session, selected_columns=columnas2)
            query = (query_builder.build_query(Criteria())
                     .join(subquery, and_(ValorParticipacionEntity.isin == subquery.columns[0],
                                          ValorParticipacionEntity.fecha == subquery.columns[1]), isouter=False))
            query = query.order_by(DatabaseManager.get_database().year(ValorParticipacionEntity.fecha).desc(),
                                   DatabaseManager.get_database().month(ValorParticipacionEntity.fecha).desc(),
                                   func.upper(ValorParticipacionEntity.isin).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"año": int(row[0]),
                               "mes": int(row[1]),
                               "fecha": row[2],
                               "isin": row[3],
                               "ultimo_valor": float(row[4]),
                               }
                    elements.append(ResumenValorParticipacion(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def resumen_valor_participacion_dias(self, criteria: Criteria) -> List[ResumenValorParticipacion]:
        elements = []
        try:
            """
            select fvc.year, fvc.month, fvc.fecha, fvc.isin, fvc.valor, fvc.day
            FROM finanzas_valor_participaciones fvc
            join (SELECT fac.isin AS isin, max(fac.fecha) AS max_1, fac.year as year, fac.month as month 
            FROM finanzas_valor_participaciones fac GROUP BY fac.isin, fac.year, fac.month, fac.day) fvc2
            on fvc.isin = fvc2.isin and fvc.fecha = fvc2.max_1
            """

            columnas = (
                ValorParticipacionEntity.isin,
                func.max(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().day(ValorParticipacionEntity.fecha),
            )


            subquery_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session, selected_columns=columnas)
            subquery = subquery_builder.build_query(Criteria())
            subquery = subquery.group_by(
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                ValorParticipacionEntity.isin).subquery()

            columnas2 = (
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                ValorParticipacionEntity.fecha,
                ValorParticipacionEntity.isin,
                ValorParticipacionEntity.valor,
                DatabaseManager.get_database().day(ValorParticipacionEntity.fecha)
            )
            query_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session, selected_columns=columnas2)
            query = (query_builder.build_query(Criteria())
                     .join(subquery, and_(ValorParticipacionEntity.isin == subquery.columns[0],
                                          ValorParticipacionEntity.fecha == subquery.columns[1]), isouter=False))
            query = query.order_by(DatabaseManager.get_database().year(ValorParticipacionEntity.fecha).desc(),
                                   DatabaseManager.get_database().month(ValorParticipacionEntity.fecha).desc(),
                                   func.upper(ValorParticipacionEntity.isin).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"año": int(row[0]),
                               "mes": int(row[1]),
                               "fecha": row[2],
                               "isin": row[3],
                               "ultimo_valor": float(row[4]),
                               "dia": row[5]
                               }
                    elements.append(ResumenValorParticipacion(element))
        except Exception as e:
            traceback.print_exc()

        return elements
