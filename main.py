import argparse
import sys
import threading
import traceback
from multiprocessing import Process
from time import sleep

from application.rest.app import Rest
from loguru import logger
import webview
from src.configuration.infrastruture.loadjsonconfiguration import LoadJsonConfiguration

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')

parser_run = subparsers.add_parser('run', help='running mode')
parser_run.add_argument('-c', '--configuration', action='store', type=str, required=False,
                        help='Configuration file to use', default="config.json")


def run(configuration: str):
    try:
        config = LoadJsonConfiguration().load_from_file(configuration)
        logger.remove()
        logger.add(sys.stderr, level=config.get("log_level", "DEBUG"))
        logger.info("Loaded {} file as configuration".format(configuration))

        if config.get("desktop_app", True):
            logger.info("Desktop app")
            webview.create_window(title="Finanzas", url=
            '{}://localhost:{}/'.format(
                "https" if config.get("flask_config", {}).get("use_ssl", False) else "http",
                config.get("flask_config", {}).get("PORT", 9090)),
                                  fullscreen=False, zoomable=True, text_select=True,
                                  confirm_close=False,
                                  maximized=True)

            app_process = Process(target=run_app, args=(config,))
            app_process.start()

            sleep(2)
            webview.start()

            app_process.terminate()
            app_process.join()
        else:
            logger.info("Rest app")
            app = Rest(config)
            app.run()
    except Exception as e:
        logger.error("Error")
        logger.exception(e)
        traceback.print_exc()

def run_app(config):
    app = Rest(config)
    app.run()


if __name__ == "__main__":
    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')](**kwargs)
