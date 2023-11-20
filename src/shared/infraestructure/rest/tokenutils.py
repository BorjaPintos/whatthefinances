import datetime
import jwt

from src.login.domain.exceptions.unauthorizederror import UnauthorizedError
from src.login.domain.user import User


def decode_auth_token(token: str, token_secret: str) -> dict:
    try:
        payload = jwt.decode(token, token_secret, verify=True, algorithms=['HS256'])
        return {
            'user': payload['user']
        }

    except jwt.ExpiredSignatureError:
        raise UnauthorizedError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise UnauthorizedError('Invalid token. Please log in again.')
    except:
        raise UnauthorizedError('Invalid token. Please log in again.')


def create_token(user: User, token_secret: str, hours_alive: float) -> str:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=hours_alive),
        'iat': datetime.datetime.utcnow(),
        'sub': user.get_id(),
        'user': user.get_dto()
    }
    token = jwt.encode(payload, token_secret, algorithm='HS256')
    return token
