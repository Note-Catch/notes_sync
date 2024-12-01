import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from notes_sync.config import get_settings
from notes_sync.database.models import User
from notes_sync.database.connection import db_context
from notes_sync.utils import decode_access_token

http_basic = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def admin_basic_auth(credentials: HTTPBasicCredentials = Depends(http_basic)):
    current_username = credentials.username.encode("utf8")
    correct_username = get_settings().ADMIN_LOGIN.encode("utf8")
    current_pass = credentials.password.encode("utf8")
    correct_pass = get_settings().ADMIN_PASSWORD.encode("utf8")

    is_correct_username = secrets.compare_digest(current_username, correct_username)
    is_correct_pass = secrets.compare_digest(current_pass, correct_pass)

    if not (is_correct_username and is_correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def oauth2(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username: str = decode_access_token(token).get("sub")
        if username is None:
            raise credentials_exception
        with db_context() as db:
            user = db.query(User).where(User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except InvalidTokenError:
        raise credentials_exception
