from flask import request
from flask_login import login_required
from loguru import logger
from src.login.application.getuser import GetUser
from src.login.application.login import Login
from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from src.login.infrastructure.persistence.userrepositorysqlalchemy import UserRepositorySQLAlchemy
from src.shared.domain.exceptions.notfounderror import NotFoundError
from src.shared.infraestructure.rest.response import serialize_response
from src.shared.infraestructure.rest.responseerror import Error
from src.shared.infraestructure.rest.tokenutils import create_token, decode_auth_token


def import_routes(rootpath, app):
    get_user_use_case = GetUser(user_repository=UserRepositorySQLAlchemy())

    @app.route(rootpath + "/<id_user>", methods=['GET'])
    @login_required
    @serialize_response
    def get_user(id_user: int):
        user = get_user_use_case.execute(id_user)
        if user:
            return user.get_dto(), 200
        raise NotFoundError()
