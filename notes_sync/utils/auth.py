from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from notes_sync.config import get_settings
from notes_sync.database.models import User

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ALGORITHM


def verify_pass(plain: str, hash: str):
    return crypt_context.verify(plain, hash)


def hash_pass(plain: str):
    return crypt_context.hash(plain)


def authenticate_user(db: Session, username: str, plain_pass: str):
    user = db.query(User).where(User.username == username).first()
    if not user:
        return False
    if not verify_pass(plain_pass, user.pass_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
