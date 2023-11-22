import pytest
from unittest.mock import MagicMock

from src.persistence.application.databasemanager import DatabaseManager


@pytest.fixture(autouse=True)
def before_test():
    DatabaseManager.__init_database = MagicMock()
    DatabaseManager.init({"type": "mock", "mock": {}})
