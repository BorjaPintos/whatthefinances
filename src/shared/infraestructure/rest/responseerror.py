"""Created on 25-10-2019."""


class Error:
    """The Class Error."""

    def __init__(self, message, code):
        """Instancce new object."""
        self.message = message
        self.code = code

    def get_message(self):
        """Get message."""
        return self.message

    def get_code(self):
        """Get code."""
        return self.code

    def get_dto(self) -> dict:
        return {"message": self.message, "code": self.code}
