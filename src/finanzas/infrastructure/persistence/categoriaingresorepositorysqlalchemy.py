import traceback
from typing import List

from src.finanzas.domain.categoriaingreso import CategoriaIngreso
from src.finanzas.domain.categoriaingresorepository import CategoriaIngresoRepository
from src.finanzas.infrastructure.persistence.orm.categoriaingresoentity import CategoriaIngresoEntity
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class CategoriaIngresoRepositorySQLAlchemy(ITransactionalRepository, CategoriaIngresoRepository):

    def list(self, criteria: Criteria) -> List[CategoriaIngreso]:
        elements = []
        try:

            columnas = (CategoriaIngresoEntity.id, CategoriaIngresoEntity.descripcion,
                        CategoriaIngresoEntity.cuenta_abono_defecto,
                        CuentaEntity.nombre,
                        CategoriaIngresoEntity.monedero_defecto,
                        MonederoEntity.nombre)
            query_builder = SQLAlchemyQueryBuilder(CategoriaIngresoEntity, self._session, selected_columns=columnas)
            query = query_builder.build_order_query(criteria) \
                .join(CuentaEntity, CategoriaIngresoEntity.cuenta_abono_defecto == CuentaEntity.id) \
                .join(MonederoEntity, CategoriaIngresoEntity.monedero_defecto == MonederoEntity.id)
            result = query.all()

            if result is not None:
                for row in result:
                    params = {"id": row[0],
                              "descripcion": row[1],
                              "id_cuenta_abono_defecto": row[2],
                              "nombre_cuenta_abono_defecto": row[3],
                              "id_monedero_defecto": row[4],
                              "nombre_monedero_defecto": row[5]
                              }
                    elements.append(CategoriaIngreso(params))

        except Exception as e:
            traceback.print_exc()

        return elements
