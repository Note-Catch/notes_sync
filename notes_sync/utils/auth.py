from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from notes_sync.config import get_settings

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM


def hash_pass(plain: str):
    return crypt_context.hash(plain)


def authenticate_user(user: object, plain_pass: str):
    def verify_pass(plain: str, hash: str):
        return crypt_context.verify(plain, hash)

    if not user:
        return False
    if not verify_pass(plain_pass, user.pass_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(access_token: str) -> dict:
    return jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
