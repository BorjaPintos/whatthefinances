import traceback
from typing import List

from src.finanzas.domain.cuenta import Cuenta
from src.finanzas.domain.cuentarepository import CuentaRepository
from src.finanzas.infrastructure.persistence.orm.cuentaentity import CuentaEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class CuentaRepositorySQLAlchemy(ITransactionalRepository, CuentaRepository):

    def list(self, criteria: Criteria) -> List[Cuenta]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(CuentaEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements
