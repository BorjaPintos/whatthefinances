

import argparse
import sys
from application.rest.app import Rest
from loguru import logger

from src.configuration.infrastruture.loadjsonconfiguration import LoadJsonConfiguration

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')

parser_run = subparsers.add_parser('run', help='running mode')
parser_run.add_argument('-c', '--configuration', action='store', type=str, required=False,
                        help='Configuration file to use', default="config.json")


def run(configuration: str):
    config = LoadJsonConfiguration().load_from_file(configuration)
    logger.remove()
    logger.add(sys.stderr, level=config.get("log_level", "DEBUG"))
    logger.info("Loaded {} file as configuration".format(configuration))
    app = Rest(config)
    app.run()


if __name__ == "__main__":
    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')](**kwargs)
