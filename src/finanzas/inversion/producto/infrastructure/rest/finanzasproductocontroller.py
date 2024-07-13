from typing import Any, Tuple
from loguru import logger

from src.finanzas.inversion.producto.application.createproducto import CreateProducto
from src.finanzas.inversion.producto.application.getproducto import GetProducto
from src.finanzas.inversion.producto.application.listproducto import ListProducto
from src.finanzas.inversion.producto.application.updateproducto import UpdateProducto
from src.finanzas.inversion.producto.domain.plataformaproductoenum import PlataformaProductoEnum
from src.finanzas.inversion.producto.infrastructure.persistence.productorepositorysqlalchemy import \
    ProductoRepositorySQLAlchemy
from src.shared.infraestructure.rest.commoncastparams import common_cast_params
from src.shared.utils.localeutils import apply_locale_int
from src.shared.domain.exceptions.messageerror import MessageError

producto_repository = ProductoRepositorySQLAlchemy()

list_productos_use_case = ListProducto(producto_repository=producto_repository)
get_producto_use_case = GetProducto(producto_repository=producto_repository)
create_producto_use_case = CreateProducto(producto_repository=producto_repository)
update_producto_use_case = UpdateProducto(producto_repository=producto_repository)


def list_productos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_productos_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_producto(id_producto: int) -> Tuple[Any, int]:
    code = 200
    producto = get_producto_use_case.execute(apply_locale_int(id_producto))
    if producto:
        response = producto.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve el producto con id {} y no da la excepción de not found".format(id_producto))
        raise MessageError("No se ha podido obtener el producto con id: {}".format(id_producto), code)
    return response, code


def create_producto(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    producto = create_producto_use_case.execute(params)
    if producto:
        response = producto.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")),
                           code)
    return response, code


def update_producto(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    producto = update_producto_use_case.execute(params)
    if producto:
        response = producto.get_dto()

    else:
        code = 409
        logger.warning("Ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un producto con ese nombre o isin: {}".format(params.get("nombre")),
                           code)
    return response, code


def list_plataformas() -> Tuple[Any, int]:
    code = 200
    response = PlataformaProductoEnum.get_all_dto()
    return response, code


def __cast_params(params: dict):
    common_cast_params(params)

    if params.get("id_plataforma") is not None:
        params["id_plataforma"] = apply_locale_int(params["id_plataforma"])
