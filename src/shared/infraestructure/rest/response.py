import traceback

from flask import Response

from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from src.shared.domain.exceptions.invalidparamerror import InvalidParamError
from src.shared.domain.exceptions.messageerror import MessageError
from src.shared.domain.exceptions.notfounderror import NotFoundError
from src.shared.infraestructure.rest.responseerror import Error
from src.shared.infraestructure.rest.serializer import Serializer
from src.shared.infraestructure.rest.serializers.jsonserializer import JsonSerializer

serializer = Serializer(JsonSerializer())


def serialize_response(func):
    def wrapper(*args, **kwargs):
        try:
            resp, code = func(*args, **kwargs)
            return Response(serializer.dumps(resp), code, mimetype=serializer.get_mimetype())
        except InvalidParamError as e:
            error = Error(str(e), 400)
        except UnauthorizedError as e:
            error = Error("No autorizado", 401)
        except NotFoundError as e:
            error = Error(str(e), 404)
        except MessageError as e:
            error = Error(e.get_msg(), e.get_code())
        except ValueError as e:
            error = Error(str(e), 400)
        except:
            traceback.print_exc()
            error = Error("Bad Request", 400)
        return serializer.dumps(error), error.get_code()

    wrapper.__name__ = func.__name__
    return wrapper
