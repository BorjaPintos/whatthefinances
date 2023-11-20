from src.version.domain.version import Version


class GetVersion:

    def __init__(self):
        pass

    def execute(self) -> Version:
        return Version()
