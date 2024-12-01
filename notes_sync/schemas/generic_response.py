from enum import IntEnum

from fastapi import status
from pydantic import BaseModel


class GenericSuccessResponseItems(BaseModel):
    count: int
    items: list[dict]


class GenericSuccessResponse(BaseModel):
    response: GenericSuccessResponseItems


class ErrorCode(IntEnum):
    USER_ALREADY_EXISTS = 0
    BROKER_NOT_RESPONDING = 2


class GenericErrorResponse(BaseModel):
    error_code: ErrorCode
    error_message: str = ""


class EmptyOkResponse(GenericSuccessResponse):
    def __init__(self):
        super().__init__(response=GenericSuccessResponseItems(count=0, items=[]))

    @staticmethod
    def status_code() -> status:
        return status.HTTP_200_OK
