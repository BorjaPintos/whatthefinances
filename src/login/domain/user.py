from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from src.shared.utils.securityutils import safe_check_password, encrypt_user_password


class User:

    def __init__(self, name: str, id: int, encrypted_password: str):
        self._id = id
        self._name = name
        self._encrypted_password = encrypted_password
        self._authenticated = False

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def login(self, password: str):
        if safe_check_password(self._encrypted_password, password):
            self._authenticated = True
        else:
            self._authenticated = False
            raise UnauthorizedError("Invalid password")

    def get_dto(self) -> dict:
        return {"id": self._id,
                "name": self._name}

    """flask-login"""

    def is_authenticated(self) -> bool:
        return self._authenticated

    def is_active(self) -> bool:
        "No hay desactivacion, por lo que siempre lo pondremos a true"
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_encrypted_password(self) -> str:
        return self._encrypted_password

    def change_password(self, old_password: str, new_password: str):
        if safe_check_password(self._encrypted_password, old_password):
            self._encrypted_password = encrypt_user_password(new_password)
        else:
            raise UnauthorizedError("Invalid password")
