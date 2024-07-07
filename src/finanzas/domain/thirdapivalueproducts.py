from abc import abstractmethod
from datetime import datetime


class ThirdApiValueProducts:

    def __init__(self, config: dict):
        self._config = config

    @staticmethod
    @abstractmethod
    def get_last_price(url: str) -> (float, datetime):
        pass
