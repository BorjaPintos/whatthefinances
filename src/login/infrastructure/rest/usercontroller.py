from typing import Tuple, Any

from loguru import logger

from src.login.application.cambiarpassword import CambiarPassword
from src.login.application.getuser import GetUser
from src.login.infrastructure.persistence.userrepositorysqlalchemy import UserRepositorySQLAlchemy
from src.shared.domain.exceptions.messageerror import MessageError

user_repository = UserRepositorySQLAlchemy()
get_user_use_case = GetUser(user_repository=user_repository)
cambiar_password_use_case = CambiarPassword(user_repository=user_repository)


def get_user(id_user: int) -> Tuple[Any, int]:
    code = 200
    user = get_user_use_case.execute(id_user)
    if user:
        response = user.get_dto()
    else:
        code = 404
        logger.warning(
            "Por alguna razón no devuelve el usuario con id {} y no da la excepción de not found".format(id_user))
        raise MessageError("No se ha podido obtener el usuario con id: {}".format(id_user), code)
    return response, code


def change_password(params: dict) -> Tuple[Any, int]:
    code = 200
    __cast_params(params)
    user = cambiar_password_use_case.execute(params)
    if user:
        response = user.get_dto()
    else:
        raise MessageError("No se ha podido cambiar la contraseña: {}".format(user), code)
    return response, code


def __cast_params(params: dict):
    if params.get("id") is not None:
        params["id"] = int(params["id"])
