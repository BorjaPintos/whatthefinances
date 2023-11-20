from abc import abstractmethod


class IApp:

    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def run(self):
        pass
