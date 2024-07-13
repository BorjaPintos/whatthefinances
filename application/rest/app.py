import os
import ssl

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from loguru import logger
from werkzeug.security import safe_join

from src.finanzas.categorias.infrastructure.rest import finanzascategoriasgastorestroutes, \
    finanzascategoriasingresorestroutes, finanzascategoriasfrontroutes
from src.finanzas.cuentas.infrastructure.rest import finanzascuentasrestroutes, finanzascuentasfrontroutes
from src.finanzas.hacienda.infrastructure.rest import finanzashaciendafrontroutes
from src.finanzas.inversion.bolsa.infrastructure.rest import finanzasbolsarestroutes, finanzasbolsafrontroutes
from src.finanzas.inversion.broker.infrastructure.rest import finanzasbrokerrestroutes, finanzasbrokerfrontroutes
from src.finanzas.inversion.posiciones.infrastructure.rest import finanzasposicionesfrontroutes, \
    finanzasposicionesrestroutes
from src.finanzas.inversion.valorparticipacion.infrastructure.rest import finanzasvaloresparticipacionesrestroutes, \
    finanzasvaloresparticipacionesfrontroutes
from src.finanzas.inversion.dividendos.infrastructure.rest import finanzasdividendosrestroutes, \
    finanzasdividendosfrontroutes
from src.finanzas.inversion.producto.infrastructure.rest import finanzasproductorestroutes, finanzasproductofrontroutes
from src.finanzas.monederos.infrastructure.rest import finanzasmonederosrestroutes, finanzasmonederosfrontroutes
from src.finanzas.operaciones.infrastructure.rest import finanzasoperacionesrestroutes, \
    finanzasoperacionesfavoritasrestroutes, finanzasoperacionesfrontroutes
from src.finanzas.resumenes.infrastructure.rest import finanzasresumenesrestroutes, finanzasresumenesfrontroutes
from src.persistence.application.databasemanager import DatabaseManager
from application.iapp import IApp
from src.login.infrastructure.rest import loginroutes, userroutes, loginfrontroutes, userfrontroutes
from src.shared.infraestructure.rest import commonfrontroutes
from src.shared.utils.resources import resource_path
from src.version.infrastructure.rest import versionroutes


class Rest(IApp):

    def __init__(self, config: dict):
        super().__init__(config)
        root_dir = os.getcwd()
        if config["packet"]:
            logger.info("Templates_folder: {}".format(str(resource_path("templates"))))
            templates = str(resource_path("templates"))
        else:
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
        if not self.app.config['UVICORN']:
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
        commonfrontroutes.import_routes("/", self.app)
        versionroutes.import_routes("/version", self.app)
        loginroutes.import_routes("/login", self.app)
        loginfrontroutes.import_routes("/", self.app)
        userroutes.import_routes("/user", self.app)
        userfrontroutes.import_routes("/", self.app)
        self._init_finanzas_rest_routes("/finanzas")
        self._init_finanzas_front_routes("/")
        self._add_static_route(self.app)

    def _init_finanzas_rest_routes(self, finanzas_path: str):
        finanzascuentasrestroutes.import_routes(finanzas_path + "/cuenta", self.app)
        finanzasmonederosrestroutes.import_routes(finanzas_path + "/monedero", self.app)
        finanzascategoriasgastorestroutes.import_routes(finanzas_path + "/categoria_gasto", self.app)
        finanzascategoriasingresorestroutes.import_routes(finanzas_path + "/categoria_ingreso", self.app)
        finanzasoperacionesrestroutes.import_routes(finanzas_path + "/operacion", self.app)
        finanzasoperacionesfavoritasrestroutes.import_routes(finanzas_path + "/operacion_favorita", self.app)
        finanzasresumenesrestroutes.import_routes(finanzas_path + "/resumen", self.app)
        finanzasbolsarestroutes.import_routes(finanzas_path + "/bolsa", self.app)
        finanzasbrokerrestroutes.import_routes(finanzas_path + "/broker", self.app)
        finanzasproductorestroutes.import_routes(finanzas_path + "/producto", self.app)
        finanzasposicionesrestroutes.import_routes(finanzas_path + "/posicion", self.app)
        finanzasdividendosrestroutes.import_routes(finanzas_path + "/dividendo", self.app)
        finanzasvaloresparticipacionesrestroutes.import_routes(finanzas_path + "/valorparticipacion", self.app)

    def _init_finanzas_front_routes(self, front_path: str):
        finanzascuentasfrontroutes.import_routes(front_path, self.app)
        finanzasmonederosfrontroutes.import_routes(front_path, self.app)
        finanzascategoriasfrontroutes.import_routes(front_path, self.app)
        finanzasoperacionesfrontroutes.import_routes(front_path, self.app)
        finanzasresumenesfrontroutes.import_routes(front_path, self.app)
        finanzasbolsafrontroutes.import_routes(front_path, self.app)
        finanzasbrokerfrontroutes.import_routes(front_path, self.app)
        finanzasproductofrontroutes.import_routes(front_path, self.app)
        finanzasposicionesfrontroutes.import_routes(front_path, self.app)
        finanzasdividendosfrontroutes.import_routes(front_path, self.app)
        finanzasvaloresparticipacionesfrontroutes.import_routes(front_path, self.app)
        finanzashaciendafrontroutes.import_routes(front_path, self.app)

    def _add_static_route(self, app):
        root_dir = os.getcwd()

        if self._config["packet"]:
            logger.info("Static_folder: {}".format(resource_path("static")))
            static = str(resource_path("static"))
        else:
            static = safe_join(root_dir, "application/web/static")

        @app.route('/<path:path>', methods=['GET'])
        def _static(path):
            return send_from_directory(static, path)
