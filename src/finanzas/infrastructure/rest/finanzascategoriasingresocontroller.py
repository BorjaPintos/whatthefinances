from typing import Any, Tuple
from loguru import logger
from src.finanzas.application.createcategoriaingreso import CreateCategoriaIngreso
from src.finanzas.application.getcategoriaingreso import GetCategoriaIngreso
from src.finanzas.application.listcategoriasingreso import ListCategoriasIngreso
from src.finanzas.application.updatecategoriaingreso import UpdateCategoriaIngreso
from src.finanzas.infrastructure.persistence.categoriaingresorepositorysqlalchemy import \
    CategoriaIngresoRepositorySQLAlchemy
from src.finanzas.infrastructure.rest.localeutils import apply_locale_int
from src.shared.domain.exceptions.messageerror import MessageError

categorias_ingreso_repository = CategoriaIngresoRepositorySQLAlchemy()

list_categorias_ingreso_use_case = ListCategoriasIngreso(
    categoria_ingreso_repository=categorias_ingreso_repository)
get_categoria_ingreso_use_case = GetCategoriaIngreso(categoria_ingreso_repository=categorias_ingreso_repository)
create_categoria_ingreso_use_case = CreateCategoriaIngreso(
    categoria_ingreso_repository=categorias_ingreso_repository)
update_categoria_ingreso_use_case = UpdateCategoriaIngreso(
    categoria_ingreso_repository=categorias_ingreso_repository)


def list_categorias_ingreso(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    elements = list_categorias_ingreso_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_categoria_ingreso(id_categoria_ingreso: int) -> Tuple[Any, int]:
    code = 200
    categoria_ingreso = get_categoria_ingreso_use_case.execute(apply_locale_int(id_categoria_ingreso))
    if categoria_ingreso:
        response = categoria_ingreso.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la categoría ingreso con id {} y no da la excepción de not found".format(
                id_categoria_ingreso))
        raise MessageError("No se ha podido obtener la categoría ingreso con id: {}".format(id_categoria_ingreso),
                           code)
    return response, code


def create_categoria_ingreso(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    categoria_ingreso = create_categoria_ingreso_use_case.execute(params)
    if categoria_ingreso:
        response = categoria_ingreso.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")))
        raise MessageError(
            "Parece que ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")),
            code)
    return response, code


def update_categoria_ingreso(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    categoria_ingreso = update_categoria_ingreso_use_case.execute(params)
    if categoria_ingreso:
        response = categoria_ingreso.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")))
        raise MessageError(
            "Parece que ya existe una categoría ingreso con esa descripción: {}".format(params.get("descripcion")),
            code)
    return response, code


def __cast_params(params: dict):
    if params.get("id") is not None:
        params["id"] = apply_locale_int(params["id"])

    if params.get("id_monedero_defecto") is not None:
        params["id_monedero_defecto"] = apply_locale_int(params["id_monedero_defecto"])
    if params.get("id_cuenta_abono_defecto") is not None:
        params["id_cuenta_abono_defecto"] = apply_locale_int(params["id_cuenta_abono_defecto"])

    if params.get("id_categoria_ingreso") is not None:
        params["id_categoria_ingreso"] = apply_locale_int(params["id_categoria_ingreso"])
