import traceback
from typing import List

from sqlalchemy.orm import aliased

from src.finanzas.domain.operacion import Operacion
from src.finanzas.domain.operacionresorepository import OperacionRepository
from src.finanzas.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.finanzas.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class OperacionRepositorySQLAlchemy(ITransactionalRepository, OperacionRepository):

    def list(self, criteria: Criteria) -> List[Operacion]:
        elements = []
        try:

            CuentaCargo = aliased(CuentaEntity, flat=True)
            CuentaAbono = aliased(CuentaEntity, flat=True)
            MonederoCargo = aliased(MonederoEntity, flat=True)
            MonederoAbono = aliased(MonederoEntity, flat=True)

            columnas = (
                OperacionEntity.id, OperacionEntity.id, OperacionEntity.cantidad, OperacionEntity.descripcion,
                OperacionEntity.categoria_gasto, CategoriaGastoEntity.descripcion,
                OperacionEntity.cuenta_cargo, CuentaCargo.nombre,
                OperacionEntity.monedero_cargo, MonederoCargo.nombre,
                OperacionEntity.categoria_ingreso, CategoriaIngresoEntity.descripcion,
                OperacionEntity.cuenta_abono, CuentaAbono.nombre,
                OperacionEntity.monedero_abono, MonederoAbono.nombre)

            query_builder = SQLAlchemyQueryBuilder(CategoriaIngresoEntity, self._session, selected_columns=columnas)
            query = query_builder.build_order_query(criteria) \
                .join(CategoriaGastoEntity, OperacionEntity.categoria_gasto == CategoriaGastoEntity.id, isouter=False) \
                .join(CuentaCargo, OperacionEntity.cuenta_cargo == CuentaCargo.id, isouter=False) \
                .join(MonederoCargo, OperacionEntity.monedero_cargo == MonederoCargo.id, isouter=False) \
                .join(CategoriaIngresoEntity, OperacionEntity.categoria_ingreso == CategoriaIngresoEntity.id, isouter=False) \
                .join(CuentaAbono, OperacionEntity.cuenta_abono == CuentaAbono.id, isouter=False) \
                .join(MonederoAbono, OperacionEntity.monedero_abono == MonederoAbono.id, isouter=False)
            result = query.all()

            if result is not None:
                for row in result:
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
                    elements.append(Operacion(params))

        except Exception as e:
            traceback.print_exc()

        return elements
