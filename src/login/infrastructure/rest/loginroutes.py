import json

from flask import request, Response
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
    def login():
        try:
            username = request.json["name"]
            password = request.json["password"]

            user = login_use_case.execute(username, password)
            if user:
                token = create_token(user, app.config['token_secret'], app.config['token_login_hours_alive'])
                code = 200
                logger.info("El usuario " + username + " se ha logueado correctamente")
                msg = {'token': token}
                response = Response(json.dumps(msg), 200, mimetype='application/json')
                response.set_cookie("token", token,
                                    max_age=app.config['token_login_hours_alive']*60*60,
                                    httponly = True)
                return response, code
            else:
                raise UnauthorizedError()
        except:
            logger.info("Usuario o contraseña incorrectos")
            msg = Error("Usuario o contraseña incorrectos", 401).__dict__
            return Response(json.dumps(msg), 401, mimetype='application/json')


    @app.login_manager.request_loader
    def load_user_from_request(request):
        token = request.headers.get('Authorization')
        if token:
            token = token.replace('Bearer ', '', 1)
        else:
            token = request.cookies.get("token")
        try:
            if token:
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
