from abc import abstractmethod, ABC
from typing import Dict


class LoadConfiguration(ABC):


    def __init__(self):
        self.conf = {}

    @abstractmethod
    def load_from_file(self, configuration_path: str) -> Dict:
        pass

    @abstractmethod
    def load_from_str(self, configuration: str) -> Dict:
        pass
