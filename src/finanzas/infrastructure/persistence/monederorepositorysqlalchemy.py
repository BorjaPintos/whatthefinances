import traceback
from typing import List

from src.finanzas.domain.monedero import Monedero
from src.finanzas.domain.monederorepository import MonederoRepository
from src.finanzas.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder


class MonederoRepositorySQLAlchemy(ITransactionalRepository, MonederoRepository):

    def list(self, criteria: Criteria) -> List[Monedero]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(MonederoEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements
