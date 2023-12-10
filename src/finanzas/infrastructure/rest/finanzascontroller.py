import locale
from datetime import datetime

from src.finanzas.application.resumengastos import ResumenGastos
from src.finanzas.application.resumeningresos import ResumenIngresos
from src.finanzas.infrastructure.persistence.resumenrepositorysqlalchemy import ResumenRepositorySQLAlchemy
from src.shared.infraestructure.rest.pagination import Pagination

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

from typing import Any, Tuple
from loguru import logger
from src.finanzas.application.createcategoriagasto import CreateCategoriaGasto
from src.finanzas.application.createcategoriaingreso import CreateCategoriaIngreso
from src.finanzas.application.createcuenta import CreateCuenta
from src.finanzas.application.createmonedero import CreateMonedero
from src.finanzas.application.createoperacion import CreateOperacion
from src.finanzas.application.deleteoperacion import DeleteOperacion
from src.finanzas.application.getcategoriagasto import GetCategoriaGasto
from src.finanzas.application.getcategoriaingreso import GetCategoriaIngreso
from src.finanzas.application.getcuenta import GetCuenta
from src.finanzas.application.getmonedero import GetMonedero
from src.finanzas.application.getoperacion import GetOperacion
from src.finanzas.application.listcategoriasgasto import ListCategoriasGasto
from src.finanzas.application.listcategoriasingreso import ListCategoriasIngreso
from src.finanzas.application.listcuentas import ListCuentas
from src.finanzas.application.listmonederos import ListMonederos
from src.finanzas.application.listoperaciones import ListOperaciones
from src.finanzas.application.updatecategoriagasto import UpdateCategoriaGasto
from src.finanzas.application.updatecategoriaingreso import UpdateCategoriaIngreso
from src.finanzas.application.updatecuenta import UpdateCuenta
from src.finanzas.application.updatemonedero import UpdateMonedero
from src.finanzas.application.updateoperacion import UpdateOperacion
from src.finanzas.infrastructure.persistence.categoriagastorepositorysqlalchemy import \
    CategoriaGastoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.categoriaingresorepositorysqlalchemy import \
    CategoriaIngresoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.cuentarepositorysqlalchemy import CuentaRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.monederorepositorysqlalchemy import MonederoRepositorySQLAlchemy
from src.finanzas.infrastructure.persistence.operacionrepositorysqlalchemy import OperacionRepositorySQLAlchemy
from src.shared.domain.exceptions.messageerror import MessageError

cuenta_repository = CuentaRepositorySQLAlchemy()
monedero_repository = MonederoRepositorySQLAlchemy()
categorias_ingreso_repository = CategoriaIngresoRepositorySQLAlchemy()
categorias_gasto_repository = CategoriaGastoRepositorySQLAlchemy()
operacion_repository = OperacionRepositorySQLAlchemy()
resumen_repository = ResumenRepositorySQLAlchemy()

list_cuentas_use_case = ListCuentas(cuenta_repository=cuenta_repository)
get_cuenta_use_case = GetCuenta(cuenta_repository=cuenta_repository)
create_cuenta_use_case = CreateCuenta(cuenta_repository=cuenta_repository)
update_cuenta_use_case = UpdateCuenta(cuenta_repository=cuenta_repository)

list_monederos_use_case = ListMonederos(monedero_repository=monedero_repository)
get_monedero_use_case = GetMonedero(monedero_repository=monedero_repository)
create_monedero_use_case = CreateMonedero(monedero_repository=monedero_repository)
update_monedero_use_case = UpdateMonedero(monedero_repository=monedero_repository)

list_categorias_ingreso_use_case = ListCategoriasIngreso(
    categoria_ingreso_repository=categorias_ingreso_repository)
get_categoria_ingreso_use_case = GetCategoriaIngreso(categoria_ingreso_repository=categorias_ingreso_repository)
create_categoria_ingreso_use_case = CreateCategoriaIngreso(
    categoria_ingreso_repository=categorias_ingreso_repository)
update_categoria_ingreso_use_case = UpdateCategoriaIngreso(
    categoria_ingreso_repository=categorias_ingreso_repository)

list_categorias_gasto_use_case = ListCategoriasGasto(categoria_gasto_repository=categorias_gasto_repository)
get_categoria_gasto_use_case = GetCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)
create_categoria_gasto_use_case = CreateCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)
update_categoria_gasto_use_case = UpdateCategoriaGasto(categoria_gasto_repository=categorias_gasto_repository)

list_operaciones_use_case = ListOperaciones(operacion_repository=operacion_repository)
get_operacion_use_case = GetOperacion(operacion_repository=operacion_repository)
create_operacion_use_case = CreateOperacion(operacion_repository=operacion_repository,
                                            monedero_repository=monedero_repository,
                                            cuenta_repository=cuenta_repository)
update_operacion_use_case = UpdateOperacion(operacion_repository=operacion_repository,
                                            monedero_repository=monedero_repository,
                                            cuenta_repository=cuenta_repository)
delete_operacion_use_case = DeleteOperacion(operacion_repository=operacion_repository,
                                            monedero_repository=monedero_repository,
                                            cuenta_repository=cuenta_repository)

resumen_ingresos_use_case = ResumenIngresos(resumen_repository=resumen_repository)
resumen_gastos_use_case = ResumenGastos(resumen_repository=resumen_repository)


def list_cuentas(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_cuentas_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_cuenta(id_cuenta: int) -> Tuple[Any, int]:
    code = 200
    cuenta = get_cuenta_use_case.execute(apply_locale_int(id_cuenta))
    if cuenta:
        response = cuenta.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la cuenta con id {} y no da la excepción de not found".format(id_cuenta))
        raise MessageError("No se ha podido obtener la cuenta con id: {}".format(id_cuenta), code)
    return response, code


def create_cuenta(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    cuenta = create_cuenta_use_case.execute(params)
    if cuenta:
        response = cuenta.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una cuenta con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una cuenta con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def update_cuenta(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    cuenta = update_cuenta_use_case.execute(params)
    if cuenta:
        response = cuenta.get_dto()

    else:
        code = 409
        logger.warning("Ya existe una cuenta con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una cuenta con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def list_monederos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_monederos_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_monedero(id_monedero: int) -> Tuple[Any, int]:
    code = 200
    monedero = get_monedero_use_case.execute(apply_locale_int(id_monedero))
    if monedero:
        response = monedero.get_dto()
    else:
        logger.warning(
            "Por alguna razón no devuelve el monedero con id {} y no da la excepción de not found".format(
                id_monedero))
        raise MessageError("No se ha podido obtener el monedero con id: {}".format(id_monedero), code)
    return response, code


def create_monedero(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    monedero = create_monedero_use_case.execute(params)
    if monedero:
        response = monedero.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un monedero con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un monedero con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def update_monedero(params: dict) -> Tuple[Any, int]:
    code = 200

    __cast_params(params)
    monedero = update_monedero_use_case.execute(params)
    if monedero:
        response = monedero.get_dto()
    else:
        code = 409
        logger.warning("Ya existe un monedero con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe un monedero con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


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


def list_operaciones(params: dict) -> Tuple[Pagination, int]:
    code = 200
    __cast_params(params)
    elements, total_elements = list_operaciones_use_case.execute(params)
    response_elements = []
    for element in elements:
        response_elements.append(element.get_dto())
    return Pagination(response_elements, params["offset"], params["count"], total_elements), code


def get_operacion(id_operacion: int) -> Tuple[Any, int]:
    code = 200
    operacion = get_operacion_use_case.execute(apply_locale_int(id_operacion))
    if operacion:
        response = operacion.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la operación con id {} y no da la excepción de not found".format(
                id_operacion))
        raise MessageError("No se ha podido obtener la operación con id: {}".format(id_operacion), code)
    return response, code


def create_operacion(params: dict) -> Tuple[Any, int]:
    code = 201
    __cast_params(params)
    created = create_operacion_use_case.execute(params)
    if created:
        response = {}
    else:
        code = 400
        logger.warning("Error al crear la operacion: {}".format(params.get("descripcion")))
        raise MessageError("Error al crear la operacion: {}".format(params.get("descripcion")), code)
    return response, code


def update_operacion(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    updated = update_operacion_use_case.execute(params)
    if updated:
        response = {}
    else:
        code = 400
        logger.warning("Error al actualizar la operación con id: {}".format(params.get("id")))
        raise MessageError("Error al actualizar la operación con id: {}".format(params.get("id")), code)
    return response, code


def delete_operacion(id_operacion: int) -> Tuple[Any, int]:
    code = 200
    operacion = delete_operacion_use_case.execute(apply_locale_int(id_operacion))
    if operacion:
        response = {}
    else:
        code = 400
        logger.warning("Error al eliminar la operación con id: {}".format(id_operacion))
        raise MessageError("Error al eliminar la operación con id: {}".format(id_operacion), code)
    return response, code


def resumen_ingresos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_ingresos_use_case.execute(params)
    response_elements = []
    # for element in elements:
    #    response_elements.append(element.get_dto())
    return response, code


def resumen_gastos(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    response = resumen_gastos_use_case.execute(params)
    response_elements = []
    # for element in elements:
    #    response_elements.append(element.get_dto())
    return response, code


def __cast_params(params: dict):
    if params.get("id") is not None:
        params["id"] = apply_locale_int(params["id"])
    if params.get("count") is not None:
        params["count"] = apply_locale_int(params["count"])
        if params["count"] <= 0:
            params["count"] = 1
    if params.get("offset") is not None:
        params["offset"] = apply_locale_int(params["offset"])
        if params["offset"] < 0:
            params["offset"] = 0
    if params.get("id_monedero_defecto") is not None:
        params["id_monedero_defecto"] = apply_locale_int(params["id_monedero_defecto"])
    if params.get("id_cuenta_abono_defecto") is not None:
        params["id_cuenta_abono_defecto"] = apply_locale_int(params["id_cuenta_abono_defecto"])
    if params.get("id_cuenta_cargo_defecto") is not None:
        params["id_cuenta_cargo_defecto"] = apply_locale_int(params["id_cuenta_cargo_defecto"])

    if params.get("id_monedero_cargo") is not None:
        params["id_monedero_cargo"] = apply_locale_int(params["id_monedero_cargo"])
    if params.get("id_cuenta_cargo") is not None:
        params["id_cuenta_cargo"] = apply_locale_int(params["id_cuenta_cargo"])

    if params.get("id_monedero_abono") is not None:
        params["id_monedero_abono"] = apply_locale_int(params["id_monedero_abono"])
    if params.get("id_cuenta_abono") is not None:
        params["id_cuenta_abono"] = apply_locale_int(params["id_cuenta_abono"])

    if params.get("id_categoria_gasto") is not None:
        params["id_categoria_gasto"] = apply_locale_int(params["id_categoria_gasto"])
    if params.get("id_categoria_ingreso") is not None:
        params["id_categoria_ingreso"] = apply_locale_int(params["id_categoria_ingreso"])

    if params.get("cantidad_inicial") is not None:
        params["cantidad_inicial"] = apply_locale_float(params["cantidad_inicial"])

    if params.get("cantidad") is not None:
        params["cantidad"] = apply_locale_float(params["cantidad"])
    if params.get("begin_cantidad") is not None:
        params["begin_cantidad"] = apply_locale_float(params["begin_cantidad"])
    if params.get("end_cantidad") is not None:
        params["end_cantidad"] = apply_locale_float(params["end_cantidad"])

    if params.get("ponderacion") is not None:
        params["ponderacion"] = apply_locale_float(params["ponderacion"])

    if params.get("fecha") is not None:
        params["fecha"] = apply_locale_date(params["fecha"])
    if params.get("begin_fecha") is not None:
        params["begin_fecha"] = apply_locale_date(params["begin_fecha"])
    if params.get("end_fecha") is not None:
        params["end_fecha"] = apply_locale_date(params["end_fecha"])


def apply_locale_float(value):
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        return locale.atof(value)


def apply_locale_int(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return locale.atoi(value)


def apply_locale_date(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, '%d/%m/%Y').date()
