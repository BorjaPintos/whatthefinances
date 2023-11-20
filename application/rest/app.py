import os

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from loguru import logger
from src.persistence.application.databasemanager import DatabaseManager
from application.iapp import IApp
from src.finanzas.infrastructure.rest import finanzasroutes
from src.login.infrastructure.rest import loginroutes
from src.version.infrastructure.rest import versionroutes


def _add_headers(app):
    @app.after_request
    def add_headers(resp):
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Server'] = app.config.get('server_info', '')
        if app.config['use_ssl']:
            resp.headers['Strict-Transport-Security'] = 'max-age=31536000; \
                includeSubDomains'
        return resp


class Rest(IApp):

    def __init__(self, config: dict):
        super().__init__(config)
        self.app = Flask(__name__)
        self.app.config.update(config["flask_config"])
        self.cors = CORS(self.app)
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.database_client = self.__init_database(self._config["database"])
        self.init_app()

    def run(self):
        logger.info("Start run")
        asgi_app = WsgiToAsgi(self.app)
        if self.app.config['use_ssl']:
            uvicorn.run(asgi_app, host=self.app.config['HOST'],
                        port=self.app.config['PORT'],
                        ssl_certfile=self.app.config['ssl'].get('cert_path'),
                        ssl_keyfile=self.app.config['ssl'].get('key_path'),
                        ssl_keyfile_password=self.app.config['ssl'].get('passphrase'),
                        server_header=False
                        )
        else:
            uvicorn.run(asgi_app, host=self.app.config['HOST'], port=self.app.config['PORT'], server_header=False)

        logger.info("End run")

    def _need_execution(self):
        """Esta funcion sirve para saber si flask se va a reiniciar,
        con lo que en la primera ejecucion podemos evitar ejecutar cosas, como un thread"""
        return os.environ.get("WERKZEUG_RUN_MAIN") is not None or self.app.config['DEBUG'] is False

    def init_app(self):
        _add_headers(self.app)
        self._init_routes()

    @staticmethod
    def __init_database(config_database: dict):
        client = DatabaseManager.init(config_database)
        DatabaseManager.init_tables(config_database["init"])
        DatabaseManager.init_data(config_database["init"])
        return client

    def _init_routes(self):
        versionroutes.import_routes("/version", self.app)
        loginroutes.import_routes("/login", self.app)
        finanzasroutes.import_routes("/finanzas", self.app)
