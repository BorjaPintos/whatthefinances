
class ITransactionalRepository:

    def __init__(self):
        super().__init__()
        self._session = None

    def set_session(self, session):
        self._session = session

    def get_session(self):
        return self._session
