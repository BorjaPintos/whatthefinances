"""Created on 12-09-2019."""
import json
import enum

from src.shared.infraestructure.rest.serializers.iserializer import ISerializer


class JsonSerializer(ISerializer):

    def parse(self, text: str) -> dict:
        return json.loads(text)

    def dumps(self, object_to_serialize: object) -> str:
        if object_to_serialize is None:
            return json.dumps({})
        else:
            return json.dumps(object_to_serialize, default=obj_type)

    def get_mimetype(self) -> str:
        return 'application/json'


def obj_type(obj: object):
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, enum.Enum):
        return obj._name_
    else:
        return obj.__dict__
