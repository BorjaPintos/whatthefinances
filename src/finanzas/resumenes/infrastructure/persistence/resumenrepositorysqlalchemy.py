import traceback
from typing import List
from sqlalchemy import func, and_, asc

from src.finanzas.inversion.posiciones.infrastructure.persistence.orm.posicionentity import PosicionEntity
from src.finanzas.resumenes.domain.resumencuenta import ResumenCuenta
from src.finanzas.resumenes.domain.resumengasto import ResumenGasto
from src.finanzas.resumenes.domain.resumeningreso import ResumenIngreso
from src.finanzas.resumenes.domain.resumenmonedero import ResumenMonedero
from src.finanzas.resumenes.domain.resumenposicion import ResumenPosicion
from src.finanzas.resumenes.domain.resumenposicionacumulada import ResumenPosicionAcumulada
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
from src.finanzas.inversion.valorparticipacion.infrastructure.persistence.orm.valorparticipacionentity import \
    ValorParticipacionEntity
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

            subquery_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session,
                                                      selected_columns=columnas)
            subquery = subquery_builder.build_query(criteria)
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

            subquery_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session,
                                                      selected_columns=columnas)
            subquery = subquery_builder.build_query(Criteria())
            subquery = subquery.group_by(
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().day(ValorParticipacionEntity.fecha),
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
            query = (query_builder.build_query(criteria)
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

    def resumen_posiciones_meses(self, criteria: Criteria) -> List[ResumenPosicion]:
        elements = []
        try:

            """
                select fp.isin, sum(fp.numero_participaciones) as suma_participaciones, fvc2.valor, fvc2.max_1,  
                STRFTIME("%Y", fvc2.max_1) as year, STRFTIME("%m", fvc2.max_1) as month
                from finanzas_posiciones fp
                join (SELECT fac.isin AS isin, fac.valor as valor ,max(fac.fecha) AS max_1, STRFTIME("%Y", fac.fecha), STRFTIME("%m", fac.fecha) 
                FROM finanzas_valor_participaciones fac 
                GROUP BY fac.isin, STRFTIME("%Y", fac.fecha),  STRFTIME("%m", fac.fecha)) fvc2
                on fp.isin = fvc2.isin and fp.fecha_compra < fvc2.max_1
                GROUP BY fp.isin, fvc2.max_1
                order by fvc2.max_1
            """
            columnas_subquery = (
                ValorParticipacionEntity.isin,
                ValorParticipacionEntity.valor,
                func.max(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha)
            )

            subquery_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session,
                                                      selected_columns=columnas_subquery)
            subquery = subquery_builder.build_query(criteria)
            subquery = subquery.group_by(
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                ValorParticipacionEntity.isin).subquery()

            columnas2 = (
                PosicionEntity.isin,
                func.sum(PosicionEntity.numero_participaciones),
                subquery.columns[1],
                subquery.columns[2],
                subquery.columns[3],
                subquery.columns[4]
            )

            query_builder = SQLAlchemyQueryBuilder(PosicionEntity, self._session, selected_columns=columnas2)
            query = (query_builder.build_query(Criteria())
                     .join(subquery, and_(PosicionEntity.isin == subquery.columns[0],
                                          PosicionEntity.fecha_compra <= subquery.columns[2]), isouter=False))
            query = query.group_by(PosicionEntity.isin, subquery.columns[2])
            query = query.order_by(subquery.columns[3].desc(),
                                   subquery.columns[4].desc(),
                                   func.upper(PosicionEntity.isin).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"isin": row[0],
                               "suma_participaciones": float(row[1]),
                               "valor": float(row[2]),
                               "fecha": row[3],
                               "año": int(row[4]),
                               "mes": int(row[5]),
                               }

                    elements.append(ResumenPosicion(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def resumen_posiciones_dias(self, criteria: Criteria) -> List[ResumenPosicion]:
        elements = []
        try:

            """
                select fp.isin, sum(fp.numero_participaciones) as suma_participaciones, fvc2.valor, fvc2.max_1,  
                STRFTIME("%Y", fvc2.max_1) as year, STRFTIME("%m", fvc2.max_1) as month, STRFTIME("%d", fvc2.max_1) as day
                from finanzas_posiciones fp
                join (SELECT fac.isin AS isin, fac.valor as valor ,max(fac.fecha) AS max_1, STRFTIME("%Y", fac.fecha), STRFTIME("%m", fac.fecha) 
                FROM finanzas_valor_participaciones fac 
                GROUP BY fac.isin, STRFTIME("%Y", fac.fecha),  STRFTIME("%m", fac.fecha)) fvc2
                on fp.isin = fvc2.isin and fp.fecha_compra < fvc2.max_1
                GROUP BY fp.isin, fvc2.max_1
                order by fvc2.max_1
            """
            columnas_subquery = (
                ValorParticipacionEntity.isin,
                ValorParticipacionEntity.valor,
                func.max(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().day(ValorParticipacionEntity.fecha)
            )

            subquery_builder = SQLAlchemyQueryBuilder(ValorParticipacionEntity, self._session,
                                                      selected_columns=columnas_subquery)
            subquery = subquery_builder.build_query(Criteria())
            subquery = subquery.group_by(
                DatabaseManager.get_database().year(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().month(ValorParticipacionEntity.fecha),
                DatabaseManager.get_database().day(ValorParticipacionEntity.fecha),
                ValorParticipacionEntity.isin).subquery()

            columnas2 = (
                PosicionEntity.isin,
                func.sum(PosicionEntity.numero_participaciones),
                subquery.columns[1],
                func.max(subquery.columns[2]),
                DatabaseManager.get_database().year(subquery.columns[2]),
                DatabaseManager.get_database().month(subquery.columns[2]),
                DatabaseManager.get_database().day(subquery.columns[2])
            )

            query_builder = SQLAlchemyQueryBuilder(PosicionEntity, self._session, selected_columns=columnas2)
            query = (query_builder.build_query(criteria)
                     .join(subquery, and_(PosicionEntity.isin == subquery.columns[0],
                                          PosicionEntity.fecha_compra <= subquery.columns[2]), isouter=False))
            query = query.order_by(DatabaseManager.get_database().year(subquery.columns[2]).desc(),
                                   DatabaseManager.get_database().month(subquery.columns[2]).desc(),
                                   DatabaseManager.get_database().day(subquery.columns[2]).desc(),
                                   func.upper(PosicionEntity.isin).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"isin": row[0],
                               "suma": float(row[1]),
                               "valor": float(row[2]),
                               "fecha": row[3],
                               "año": int(row[4]),
                               "mes": int(row[5]),
                               "dia": int(row[6])
                               }

                    elements.append(ResumenPosicion(element))
        except Exception as e:
            traceback.print_exc()

        return elements

    def resumen_posiciones_meses_acumulada(self, criteria: Criteria) -> List[ResumenPosicionAcumulada]:
        elements = []
        try:

            """
                select  
                posiciones_mes.isin, 
                posiciones_mes.suma_participaciones_de_ese_dia, 
                posiciones_mes.precio_compra, 
                posiciones_mes.año, 
                posiciones_mes.mes, 
                sum(posiciones_mes.suma_participaciones_de_ese_dia) over (PARTITION BY posiciones_mes.isin ORDER BY fecha asc) as participaciones_acumuladadas, 
                sum(posiciones_mes.precio_compra) over (PARTITION BY posiciones_mes.isin ORDER BY fecha asc) as precio_compra_acumulado from 
                (select 
                posiciones_dia.isin as isin,  
                sum(posiciones_dia.numero_partipaciones) as suma_participaciones_de_ese_dia,  
                sum(posiciones_dia.precio_compra) as precio_compra,   
                max(posiciones_dia.fecha) as fecha, 
                STRFTIME("%Y", posiciones_dia.fecha) as año,  
                STRFTIME("%m", posiciones_dia.fecha) as mes from 
                (select fp2.isin as isin,  
                fp2.numero_participaciones as numero_partipaciones, 
                fp2.numero_participaciones*fp2.precio_compra_sin_comision as precio_compra, 
                max(fp2.fecha_compra) as fecha, STRFTIME("%Y", fp2.fecha_compra) as año,  
                STRFTIME("%m", fp2.fecha_compra) as mes 
                from finanzas_posiciones fp2 
                group by fp2.isin, STRFTIME("%Y", fp2.fecha_compra), STRFTIME("%m", fp2.fecha_compra), STRFTIME("%d", fp2.fecha_compra) 
                order by fp2.fecha_compra desc, fp2.isin desc) posiciones_dia 
                group by posiciones_dia.isin, posiciones_dia.año, posiciones_dia.mes 
                order by posiciones_dia.fecha desc, posiciones_dia.isin desc) posiciones_mes 
                group by posiciones_mes.isin, posiciones_mes.año, posiciones_mes.mes 
                order by posiciones_mes.fecha desc, posiciones_mes.isin desc
            """
            columnas_subquery_precios_compra_dia = (
                PosicionEntity.isin,
                PosicionEntity.numero_participaciones,
                PosicionEntity.numero_participaciones * PosicionEntity.precio_compra_sin_comision,
                func.max(PosicionEntity.fecha_compra),
                DatabaseManager.get_database().year(PosicionEntity.fecha_compra),
                DatabaseManager.get_database().month(PosicionEntity.fecha_compra),
                DatabaseManager.get_database().day(PosicionEntity.fecha_compra)
            )

            subquery_precios_compra_dia_builder = SQLAlchemyQueryBuilder(PosicionEntity, self._session,
                                                                         selected_columns=columnas_subquery_precios_compra_dia)
            subquery_precios_compra_dia_query = subquery_precios_compra_dia_builder.build_query(Criteria())
            subquery_precios_compra_dia_query = subquery_precios_compra_dia_query.group_by(
                PosicionEntity.isin,
                DatabaseManager.get_database().year(PosicionEntity.fecha_compra),
                DatabaseManager.get_database().month(PosicionEntity.fecha_compra),
                DatabaseManager.get_database().day(PosicionEntity.fecha_compra)).subquery()

            columns_subquery_precios_compra_mes_query = (
                subquery_precios_compra_dia_query.columns[0],
                func.sum(subquery_precios_compra_dia_query.columns[1]),
                func.sum(subquery_precios_compra_dia_query.columns[2]),
                func.max(subquery_precios_compra_dia_query.columns[3]),
                subquery_precios_compra_dia_query.columns[4],
                subquery_precios_compra_dia_query.columns[5]
            )

            subquery_precios_compra_mes_builder = SQLAlchemyQueryBuilder(subquery_precios_compra_dia_query,
                                                                         self._session,
                                                                         selected_columns=columns_subquery_precios_compra_mes_query)

            subquery_precios_compra_mes_query = subquery_precios_compra_mes_builder.build_query(Criteria())

            subquery_precios_compra_mes_query = subquery_precios_compra_mes_query.group_by(
                subquery_precios_compra_dia_query.columns[0],
                subquery_precios_compra_dia_query.columns[4],
                subquery_precios_compra_dia_query.columns[5]).subquery()

            columns_query_acumulados = (
                subquery_precios_compra_mes_query.columns[0],
                subquery_precios_compra_mes_query.columns[1],
                subquery_precios_compra_mes_query.columns[2],
                subquery_precios_compra_mes_query.columns[4],
                subquery_precios_compra_mes_query.columns[5],
                func.sum(subquery_precios_compra_mes_query.columns[1]).over(partition_by=subquery_precios_compra_mes_query.columns[0], order_by=asc(subquery_precios_compra_mes_query.columns[3])),
                func.sum(subquery_precios_compra_mes_query.columns[2]).over(partition_by=subquery_precios_compra_mes_query.columns[0], order_by=asc(subquery_precios_compra_mes_query.columns[3])),
            )


            query_builder = SQLAlchemyQueryBuilder(subquery_precios_compra_mes_query,
                                             self._session,
                                             selected_columns=columns_query_acumulados)
            query = query_builder.build_query(Criteria())
            query = query.group_by(subquery_precios_compra_mes_query.columns[0],
                                   subquery_precios_compra_mes_query.columns[4],
                                   subquery_precios_compra_mes_query.columns[5])
            query = query.order_by(subquery_precios_compra_mes_query.columns[4].desc(),
                                   subquery_precios_compra_mes_query.columns[5].desc(),
                                   func.upper(subquery_precios_compra_mes_query.columns[0]).asc())

            result = query.all()
            if result is not None:
                for row in result:
                    element = {"isin": row[0],
                               "participaciones_mes": float(row[1]),
                               "precio_compra_mes": float(row[2]),
                               "año": int(row[3]),
                               "mes": int(row[4]),
                               "participaciones_acumuladas":float(row[5]),
                               "precio_compra_acumulado":float(row[6])
                               }

                    elements.append(ResumenPosicionAcumulada(element))
        except Exception as e:
            traceback.print_exc()

        return elements
