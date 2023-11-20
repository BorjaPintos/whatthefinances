"""Created on 11-11-2019."""
import argparse
import sys
from application.rest.app import Rest
from src.configuration.infrastruture.load_configuration import LoadConfiguration
from loguru import logger

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')

parser_run = subparsers.add_parser('run', help='running mode')
parser_run.add_argument('-c', '--configuration', action='store', type=str, required=True,
                        help='Configuration file to use')


def run(configuration):
    config = LoadConfiguration.load_from_file_json(configuration)
    logger.remove()
    logger.add(sys.stderr, level=config.get("log_level", "DEBUG"))
    app = Rest(config)
    app.run()


if __name__ == "__main__":
    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')](**kwargs)
