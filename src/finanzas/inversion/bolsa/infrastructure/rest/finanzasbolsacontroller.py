from typing import Any, Tuple
from loguru import logger

from src.finanzas.inversion.bolsa.application.createbolsa import CreateBolsa
from src.finanzas.inversion.bolsa.application.getbolsa import GetBolsa
from src.finanzas.inversion.bolsa.application.listbolsa import ListBolsa
from src.finanzas.inversion.bolsa.application.updatebolsa import UpdateBolsa
from src.finanzas.inversion.bolsa.infrastructure.persistence.bolsarepositorysqlalchemy import BolsaRepositorySQLAlchemy
from src.shared.infraestructure.rest.commoncastparams import common_cast_params
from src.shared.utils.localeutils import apply_locale_int
from src.shared.domain.exceptions.messageerror import MessageError

bolsa_repository = BolsaRepositorySQLAlchemy()

list_bolsas_use_case = ListBolsa(bolsa_repository=bolsa_repository)
get_bolsa_use_case = GetBolsa(bolsa_repository=bolsa_repository)
create_bolsa_use_case = CreateBolsa(bolsa_repository=bolsa_repository)
update_bolsa_use_case = UpdateBolsa(bolsa_repository=bolsa_repository)


def list_bolsas(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    elements = list_bolsas_use_case.execute(params)
    response = []
    for element in elements:
        response.append(element.get_dto())
    return response, code


def get_bolsa(id_bolsa: int) -> Tuple[Any, int]:
    code = 200
    bolsa = get_bolsa_use_case.execute(apply_locale_int(id_bolsa))
    if bolsa:
        response = bolsa.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve la bolsa con id {} y no da la excepción de not found".format(id_bolsa))
        raise MessageError("No se ha podido obtener la bolsa con id: {}".format(id_bolsa), code)
    return response, code


def create_bolsa(params: dict) -> Tuple[Any, int]:
    code = 201

    __cast_params(params)
    bolsa = create_bolsa_use_case.execute(params)
    if bolsa:
        response = bolsa.get_dto()
    else:
        code = 409
        logger.warning("Ya existe una bolsa con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una bolsa con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def update_bolsa(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    bolsa = update_bolsa_use_case.execute(params)
    if bolsa:
        response = bolsa.get_dto()

    else:
        code = 409
        logger.warning("Ya existe una bolsa con ese nombre: {}".format(params.get("nombre")))
        raise MessageError("Parece que ya existe una bolsa con ese nombre: {}".format(params.get("nombre")), code)
    return response, code


def __cast_params(params: dict):
    common_cast_params(params)
