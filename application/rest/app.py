import os
import ssl

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from loguru import logger
from werkzeug.security import safe_join

from src.persistence.application.databasemanager import DatabaseManager
from application.iapp import IApp
from src.finanzas.infrastructure.rest import finanzasrestroutes, finanzasfrontroutes
from src.login.infrastructure.rest import loginroutes, userroutes, loginfrontroutes
from src.version.infrastructure.rest import versionroutes


class Rest(IApp):

    def __init__(self, config: dict):
        super().__init__(config)
        root_dir = os.getcwd()
        templates = safe_join(root_dir, "./application/web/templates")
        self.app = Flask(__name__, template_folder=templates)
        self.app.config.update(config["flask_config"])
        self.cors = CORS(self.app)
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        self.database_client = self.__init_database(self._config["database"])
        self._add_headers(self.app)
        self._init_routes()

    def run(self):
        logger.info("Start run")
        if self.app.config['DEBUG']:
            self._run_flask()
        else:
            self._run_uvicorn()
        logger.info("End run")

    def _run_uvicorn(self):

        asgi_app = WsgiToAsgi(self.app)
        if self.app.config['use_ssl']:
            uvicorn.run(asgi_app, host=self.app.config['HOST'],
                        port=self.app.config['PORT'],
                        ssl_certfile=self.app.config['ssl'].get('cert_path'),
                        ssl_keyfile=self.app.config['ssl'].get('key_path'),
                        ssl_keyfile_password=self.app.config['ssl'].get('passphrase'),
                        server_header=False)
        else:
            uvicorn.run(asgi_app, host=self.app.config['HOST'], port=self.app.config['PORT'], server_header=False)



    def _run_flask(self):
        secure_context = None
        if self.app.config['use_ssl']:
            secure_context = ssl.SSLContext()
            secure_context.load_cert_chain(certfile=self.app.config['ssl'].get('cert_path'),
                                           keyfile=self.app.config['ssl'].get('key_path'),
                                           password=self.app.config['ssl'].get('passphrase'))
        self.app.run(host=self.app.config['HOST'],
                     port=self.app.config['PORT'],
                     ssl_context=secure_context)

    @staticmethod
    def _add_headers(app):
        @app.after_request
        def add_headers(resp):
            if app.config['use_ssl']:
                resp.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            resp.headers["X-Frame-Options"] = "deny"
            resp.headers["X-Content-Type-Options"] = "nosniff"
            resp.headers["Referrer-Policy"] = "no-referrer"
            resp.headers["Cache-Control"] = "no-store, max-age=0"
            resp.headers[
                "Content-Security-Policy"] = "default-src 'self'; form-action 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content"
            return resp

    @staticmethod
    def __init_database(config_database: dict):
        client = DatabaseManager.init(config_database)
        DatabaseManager.init_tables(config_database["init"])
        DatabaseManager.init_data(config_database["init"])
        return client

    def _init_routes(self):
        versionroutes.import_routes("/version", self.app)
        loginroutes.import_routes("/login", self.app)
        loginfrontroutes.import_routes("/", self.app)
        userroutes.import_routes("/user", self.app)
        finanzasrestroutes.import_routes("/finanzas", self.app)
        finanzasfrontroutes.import_routes("/", self.app)
        self._add_static_route(self.app)

    @staticmethod
    def _add_static_route(app):
        root_dir = os.getcwd()
        static = safe_join(root_dir, "./application/web/static")

        @app.route('/<path:path>', methods=['GET'])
        def _static(path):
            return send_from_directory(static, path)
