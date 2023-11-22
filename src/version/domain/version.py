class Version:

    def __init__(self):
        self._version = 1.0

    def get_version(self) -> float:
        return self._version

    def get_dto(self) -> dict:
        return {"version": self._version}
