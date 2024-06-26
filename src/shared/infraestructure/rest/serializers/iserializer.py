from abc import ABC, abstractmethod


class ISerializer(ABC):

    @abstractmethod
    def parse(self, text) -> dict:
        raise NotImplementedError

    @abstractmethod
    def dumps(self, objectToSerialize) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_mimetype(self) -> str:
        raise NotImplementedError
