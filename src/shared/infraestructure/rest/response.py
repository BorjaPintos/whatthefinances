import traceback

from src.shared.infraestructure.rest.responseerror import Error
from src.shared.infraestructure.rest.serializer import Serializer
from src.shared.infraestructure.rest.serializers.jsonserializer import JsonSerializer

serializer = Serializer(JsonSerializer())

def serialize_response(func):
    def wrapper(*args, **kwargs):
        try:
            response, code = func(*args, **kwargs)
            return serializer.dumps(response), code
        except:
            traceback.print_exc()
            error = Error("Bad Request", 400)
            return serializer.dumps(error), error.get_code()
    wrapper.__name__ = func.__name__
    return wrapper