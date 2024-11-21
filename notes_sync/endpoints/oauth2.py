from typing import Union
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from notes_sync.config import get_settings
from notes_sync.database.connection import get_db
from notes_sync.database import models
from notes_sync.dependencies import admin_basic_auth
from notes_sync.schemas import (
    UserAlreadyExistsResponse,
    SignupRequest,
    User,
    SignupResponse,
    Token,
)
from notes_sync.utils import authenticate_user, create_access_token

api_router = APIRouter(prefix="/oauth2", tags=["Authorization"])


@api_router.post(
    "/signup",
    responses={
        UserAlreadyExistsResponse.status_code(): {"model": UserAlreadyExistsResponse},
        SignupResponse.status_code(): {"model": SignupResponse},
    },
    dependencies=[Depends(admin_basic_auth)],
)
async def signup(
    model: SignupRequest, db: Session = Depends(get_db)
) -> Union[SignupResponse, UserAlreadyExistsResponse]:
    new_user = models.User.from_request(model)
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError:
        return UserAlreadyExistsResponse()
    return SignupResponse(user=User(username=new_user.username))


@api_router.post("/auth")
async def auth(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = db.query(User).where(User.username == form.username).first()
    user = authenticate_user(user, form.password)
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
