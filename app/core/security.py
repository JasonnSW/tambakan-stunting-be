from jose import jwt, JWTError
from datetime import datetime, timedelta
from core import config
from .config import get_settings

settings = get_settings()

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    settings = get_settings()

    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

def verify_token(token: str):
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except JWTError:
        return None
