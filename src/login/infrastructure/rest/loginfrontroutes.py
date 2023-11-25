from flask import request, render_template
from loguru import logger
from src.login.application.getuser import GetUser
from src.login.application.login import Login
from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from src.login.infrastructure.persistence.userrepositorysqlalchemy import UserRepositorySQLAlchemy
from src.shared.infraestructure.rest.response import serialize_response
from src.shared.infraestructure.rest.responseerror import Error
from src.shared.infraestructure.rest.tokenutils import create_token, decode_auth_token


def import_routes(rootpath, app):

    @app.route(rootpath, methods=['GET'])
    def get_login_template():
        return render_template('/index.html', name="Borja")



