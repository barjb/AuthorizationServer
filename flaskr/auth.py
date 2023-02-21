import jwt
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from decouple import config


ACCESS_KEY = config('ACCESS_KEY')
REFRESH_KEY = config('REFRESH_KEY')


class JWT(Enum):
    ACCESS = auto()
    REFRESH = auto()


def encode(user: str, type: JWT):
    if type == JWT.ACCESS:
        payload = {'user': user, 'iat': datetime.now(tz=timezone.utc
                                                     ), 'exp': datetime.now(tz=timezone.utc)+timedelta(minutes=5), 'nbf': datetime.now(timezone.utc)}
        return jwt.encode(payload, ACCESS_KEY, algorithm="HS256")
    elif type == JWT.REFRESH:
        payload = {'user': user, 'iat': datetime.now(tz=timezone.utc), 'exp': datetime.now(tz=timezone.utc) +
                   timedelta(days=90), 'nbf': datetime.now(tz=timezone.utc)}
        return jwt.encode(payload, REFRESH_KEY, algorithm="HS256")


def isValid(token: str, type: JWT) -> bool:
    if type == JWT.ACCESS:
        decoded_token = decode(token, JWT.ACCESS)
    elif type == JWT.REFRESH:
        decoded_token = decode(token, JWT.REFRESH)
    if decoded_token == None:
        return False
    return True


def isValidButExpired(token: str):
    try:
        jwt.decode(token, ACCESS_KEY, 'HS256')
    except jwt.exceptions.DecodeError:
        return False
    except jwt.exceptions.ExpiredSignatureError:
        return True
    return False


def decode(token: str, type: JWT):
    try:
        if type == JWT.ACCESS:
            decoded_token = jwt.decode(token, ACCESS_KEY, 'HS256')
        elif type == JWT.REFRESH:
            decoded_token = jwt.decode(token, REFRESH_KEY, 'HS256')
    except jwt.exceptions.InvalidTokenError:
        return None
    return decoded_token
