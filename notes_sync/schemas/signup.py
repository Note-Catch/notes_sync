from pydantic import BaseModel

from fastapi import status

from notes_sync.schemas.generic_response import ErrorCode, GenericErrorResponse
from notes_sync.schemas.generic_response import (
    GenericSuccessResponseItems,
    GenericSuccessResponse,
)


class SignupRequest(BaseModel):
    login: str
    password: str


class UserAlreadyExistsResponse(GenericErrorResponse):
    error_code: ErrorCode = ErrorCode.USER_ALREADY_EXISTS
    error_message: str = "User with given username already exists"

    @staticmethod
    def status_code() -> status:
        return status.HTTP_400_BAD_REQUEST


class User(BaseModel):
    username: str


class SignupResponse(GenericSuccessResponse):
    def __init__(self, user: User):
        super().__init__(
            response=GenericSuccessResponseItems(count=1, items=[dict(user)])
        )

    @staticmethod
    def status_code() -> status:
        return status.HTTP_200_OK
