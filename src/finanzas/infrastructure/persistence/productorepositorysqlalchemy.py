import traceback
from typing import List

from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.finanzas.domain.producto import Producto
from src.finanzas.domain.productorepository import ProductoRepository
from src.finanzas.infrastructure.persistence.orm.productoentity import ProductoEntity
from src.persistence.domain.criteria import Criteria
from src.persistence.domain.itransactionalrepository import ITransactionalRepository
from src.persistence.infrastructure.sqlalchmeyquerybuilder import SQLAlchemyQueryBuilder
from src.shared.domain.exceptions.notfounderror import NotFoundError


class ProductoRepositorySQLAlchemy(ITransactionalRepository, ProductoRepository):

    def list(self, criteria: Criteria) -> List[Producto]:
        elements = []
        try:
            query_builder = SQLAlchemyQueryBuilder(ProductoEntity, self._session)
            query = query_builder.build_order_query(criteria)
            result = query.all()

            if result is not None:
                for entity in result:
                    elements.append(entity.convert_to_object_domain())

        except Exception as e:
            traceback.print_exc()

        return elements

    def new(self, params: dict) -> Producto:
        try:
            entity = ProductoEntity(nombre=params.get("nombre"), isin=params.get("isin"))
            self._session.add(entity)
            self._session.flush()
            return entity.convert_to_object_domain()
        except IntegrityError as e:
            logger.info(e)
        except Exception as e:
            traceback.print_exc()
        return None

    def update(self, producto: Producto) -> bool:
        try:

            query_builder = SQLAlchemyQueryBuilder(ProductoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=producto.get_id()).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la producto con id:  {}".format(producto.get_id()))
            else:
                entity.update(producto)
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None

    def get(self, id_producto: int) -> Producto:
        try:
            query_builder = SQLAlchemyQueryBuilder(ProductoEntity, self._session).build_base_query()
            entity = query_builder.filter_by(id=id_producto).one_or_none()
            if entity is None:
                raise NotFoundError("No se encuentra la producto con id:  {}".format(id_producto))
            else:
                return entity.convert_to_object_domain()
        except NotFoundError as e:
            logger.info(e)
            raise e
        except Exception as e:
            traceback.print_exc()
        return None
