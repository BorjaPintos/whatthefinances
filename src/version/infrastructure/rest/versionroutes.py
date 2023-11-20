from src.shared.infraestructure.rest.response import serialize_response
from src.version.application.getversion import GetVersion


def import_routes(rootpath, app):
    version_use_case = GetVersion()

    @app.route(rootpath, methods=['GET'])
    @serialize_response
    def version():
        version = version_use_case.execute()
        return version.get_dto(), 200


