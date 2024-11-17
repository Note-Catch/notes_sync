import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from notes_sync.config import get_settings

http_basic = HTTPBasic()


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
