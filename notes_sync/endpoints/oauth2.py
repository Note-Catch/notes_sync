from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from notes_sync.config import get_settings
from notes_sync.database.connection import get_db
from notes_sync.schemas import Token
from notes_sync.utils import authenticate_user, create_access_token

api_router = APIRouter(prefix="/oauth2", tags=["Authorization"])


@api_router.post("/auth")
async def auth(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
