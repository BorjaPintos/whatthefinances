from src.shared.infraestructure.rest.serializers.iserializer import ISerializer


class Serializer:
    def __init__(self, serializer_impl: ISerializer):
        self.serializer_impl = serializer_impl

    def parse(self, text: str):
        return self.serializer_impl.parse(text)

    def dumps(self, object_to_serialize: object):
        return self.serializer_impl.dumps(object_to_serialize)
