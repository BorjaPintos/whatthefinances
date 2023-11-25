class MessageError(ValueError):
    "MessageError"

    def __init__(self, msg: str, code: int):
        super().__init__(msg)
        self._msg = msg
        self._code = code

    def get_msg(self) -> str:
        return self._msg

    def get_code(self) -> int:
        return self._code
