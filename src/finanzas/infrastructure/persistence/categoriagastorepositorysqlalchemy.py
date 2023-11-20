import traceback
from typing import List

from src.finanzas.domain.categoriagasto import CategoriaGasto
from src.finanzas.domain.categoriagastorepository import CategoriaGastoRepository
from src.finanzas.infrastructure.persistence.orm.categoriagastoentity import CategoriaGastoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class CategoriaGastoRepositorySQLAlchemy(ITransactionalRepository, CategoriaGastoRepository):

    def list(self, criteria: Criteria) -> List[CategoriaGasto]:
        elements = []
        try:

            columnas = (CategoriaGastoEntity.id, CategoriaGastoEntity.descripcion,
                        CategoriaGastoEntity.cuenta_cargo_defecto,
                        CuentaEntity.nombre,
                        CategoriaGastoEntity.monedero_defecto,
                        MonederoEntity.nombre)
            query_builder = SQLAlchemyQueryBuilder(CategoriaGastoEntity, self._session, selected_columns=columnas)
            query = query_builder.build_order_query(criteria) \
                .join(CuentaEntity, CategoriaGastoEntity.cuenta_cargo_defecto == CuentaEntity.id) \
                .join(MonederoEntity, CategoriaGastoEntity.monedero_defecto == MonederoEntity.id)
            result = query.all()

            if result is not None:
                for row in result:
                    params = {"id": row[0],
                              "descripcion": row[1],
                              "id_cuenta_cargo_defecto": row[2],
                              "nombre_cuenta_cargo_defecto": row[3],
                              "id_monedero_defecto": row[4],
                              "nombre_monedero_defecto": row[5]
                              }
                    elements.append(CategoriaGasto(params))

        except Exception as e:
            traceback.print_exc()

        return elements
