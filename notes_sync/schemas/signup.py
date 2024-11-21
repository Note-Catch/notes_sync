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
    def __init__(self):
        self.status_code = self.status_code()
        self.error_code = ErrorCode.USER_ALREADY_EXISTS
        self.error_message = "User with given username already exists"

    @staticmethod
    def status_code() -> status:
        return status.HTTP_400_BAD_REQUEST


class User(BaseModel):
    username: str


class SignupResponse(GenericSuccessResponse):
    def __init__(self, user: User):
        self.status_code = self.status_code()
        self.response = GenericSuccessResponseItems(count=1, items=[user])

    @staticmethod
    def status_code() -> status:
        return status.HTTP_200_OK
