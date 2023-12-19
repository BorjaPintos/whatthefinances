from abc import ABC, abstractmethod
from typing import List

from src.finanzas.domain.broker import Broker
from src.persistence.domain.criteria import Criteria


class BrokerRepository(ABC):

    @abstractmethod
    def list(self, criteria: Criteria) -> List[Broker]:
        pass

    @abstractmethod
    def new(self, params: dict) -> Broker:
        pass

    @abstractmethod
    def update(self, broker: Broker) -> bool:
        pass

    @abstractmethod
    def get(self, id_broker: int) -> Broker:
        pass