import traceback
from typing import List, Tuple

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.monederos.domain.movimientomonedero import MovimientoMonedero
from src.finanzas.monederos.domain.movimientomonederorepository import MovimientoMonederoRepository
from src.finanzas.monederos.infrastructure.persistence.orm.monederoentity import MonederoEntity
from src.finanzas.monederos.infrastructure.persistence.orm.movimientomonederoentity import MovimientoMonederoEntity
from src.finanzas.operaciones.infrastructure.persistence.orm.operacionentity import OperacionEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class MovimientoMonederoRepositorySQLAlchemy(ITransactionalRepository, MovimientoMonederoRepository):

    def list(self, criteria: Criteria) -> Tuple[List[MovimientoMonedero], int]:
        pass

    def get_by_id_operacion(self, id_operacion: int) -> List[MovimientoMonedero]:

        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(MovimientoMonederoEntity, self._session).build_base_query()
            query = query_builder.filter_by(id_operacion=id_operacion)
            result = query.all()
            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> bool:
        try:
            self.check_operacion(params.get("id_operacion"))
            self.check_monedero(params.get("id_monedero"))
            entity = MovimientoMonederoEntity(id_operacion=params.get("id_operacion"),
                                              id_monedero=params.get("id_monedero"),
                                              cantidad=params.get("cantidad"))

            self._session.add(entity)
            self._session.flush()
            return True
        except IntegrityError as e:
            logger.info(e)
        except Exception as e:
            traceback.print_exc()
        return False

    def delete(self, id_movimiento: int) -> bool:
        try:
            query_builder = SQLAlchemyQueryBuilder(MovimientoMonederoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_movimiento).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra el movimiento con id:  {}".format(id_movimiento))
            self._session.delete(entity)
            return True
        except Exception as e:
            traceback.print_exc()
        return False

    def check_monedero(self, id_monedero: int):
        query_builder = SQLAlchemyQueryBuilder(MonederoEntity, self._session).build_base_query()
        cuenta_entity = query_builder.filter_by(id=id_monedero).one_or_none()
        if cuenta_entity is None:
            raise NotFoundError("No se encuentra el monedero con id:  {}".format(id_monedero))

    def check_operacion(self, id_operacion: int):
        query_builder = SQLAlchemyQueryBuilder(OperacionEntity, self._session).build_base_query()
        cuenta_entity = query_builder.filter_by(id=id_operacion).one_or_none()
        if cuenta_entity is None:
            raise NotFoundError("No se encuentra la operacion con id:  {}".format(id_operacion))
