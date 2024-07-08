from typing import Any, Tuple
from loguru import logger
from src.finanzas.application.createcategoriagasto import CreateCategoriaGasto
from src.finanzas.application.getcategoriagasto import GetCategoriaGasto
from src.finanzas.application.listcategoriasgasto import ListCategoriasGasto
from src.finanzas.application.updatecategoriagasto import UpdateCategoriaGasto
from src.finanzas.infrastructure.persistence.categoriagastorepositorysqlalchemy import \
    CategoriaGastoRepositorySQLAlchemy
from src.shared.utils.localeutils import apply_locale_int
from src.shared.domain.exceptions.messageerror import MessageError

categorias_gasto_repository = CategoriaGastoRepositorySQLAlchemy()

list_categorias_gasto_use_case = ListCategoriasGasto(categoria_gasto_repository=categorias_gasto_repository)
get_categoria_gasto_use_case = GetCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)
create_categoria_gasto_use_case = CreateCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)
update_categoria_gasto_use_case = UpdateCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)


def list_categorias_gasto(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_categorias_gasto_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_categoria_gasto(id_categoria_gasto: int) -> Tuple[Any, int]:
    code = 200
    categoria_gasto = get_categoria_gasto_use_case.execute(apply_locale_int(id_categoria_gasto))
    if categoria_gasto:
        response = categoria_gasto.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la categoría gasto con id {} y no da la excepción de not found".format(
                id_categoria_gasto))
        raise MessageError("No se ha podido obtener la categoría gasto con id: {}".format(id_categoria_gasto), code)
    return response, code


def create_categoria_gasto(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    categoria_gasto = create_categoria_gasto_use_case.execute(params)
    if categoria_gasto:
        response = categoria_gasto.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")))
        raise MessageError(
            "Parece que ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")),
            code)
    return response, code


def update_categoria_gasto(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    categoria_gasto = update_categoria_gasto_use_case.execute(params)
    if categoria_gasto:
        response = categoria_gasto.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")))
        raise MessageError(
            "Parece que ya existe una categoría gasto con esa descripción: {}".format(params.get("descripcion")),
            code)
    return response, code


def __cast_params(params: dict):
    if params.get("id") is not None:
        params["id"] = apply_locale_int(params["id"])

    if params.get("id_monedero_defecto") is not None:
        params["id_monedero_defecto"] = apply_locale_int(params["id_monedero_defecto"])
    if params.get("id_cuenta_cargo_defecto") is not None:
        params["id_cuenta_cargo_defecto"] = apply_locale_int(params["id_cuenta_cargo_defecto"])

    if params.get("id_categoria_gasto") is not None:
        params["id_categoria_gasto"] = apply_locale_int(params["id_categoria_gasto"])
