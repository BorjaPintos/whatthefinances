from flask import request
from loguru import logger
from src.login.application.getuser import GetUser
from src.login.application.login import Login
from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from src.login.infrastructure.persistence.userrepositorysqlalchemy import UserRepositorySQLAlchemy
from src.shared.infraestructure.rest.response import serialize_response
from src.shared.infraestructure.rest.responseerror import Error
from src.shared.infraestructure.rest.tokenutils import create_token, decode_auth_token


def import_routes(rootpath, app):
    login_use_case = Login(user_repository=UserRepositorySQLAlchemy())
    getuser_use_case = GetUser(user_repository=UserRepositorySQLAlchemy())

    @app.route(rootpath, methods=['POST'])
    @serialize_response
    def login():
        username = request.json["name"]
        password = request.json["password"]
        try:
            user = login_use_case.execute(username, password)
            if user:
                token = create_token(user, app.config['token_secret'], app.config['token_login_hours_alive'])
                code = 200
                logger.info("El usuario " + username + " se ha logueado correctamente")
                response = {'token': token}
            else:
                raise UnauthorizedError()
            return response, code
        except UnauthorizedError as e:
            code = 404
            logger.warning("El usuario " + username + " no se puede loguear")
            response = Error("Invalid username or password", code)
            return response, code

    @app.login_manager.request_loader
    def load_user_from_request(request):
        token = request.headers.get('Authorization')
        try:
            if token:
                token = token.replace('Bearer ', '', 1)
                user_token = decode_auth_token(token, app.config['token_secret'])
                user = getuser_use_case.execute(user_token.get("user").get("id"))
                if user:
                    request.user = user
                    return user
        except:
            return None

    @app.login_manager.unauthorized_handler
    @serialize_response
    def unauthorized():
        response = Error("Unhautorized", 401)
        code = 401
        return response, code
