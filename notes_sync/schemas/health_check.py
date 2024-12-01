from pydantic import BaseModel
from fastapi import status

from notes_sync.schemas.generic_response import ErrorCode, GenericErrorResponse


class PingResponse(BaseModel):
    message: str = "Pong!"

    @staticmethod
    def status_code() -> status:
        return status.HTTP_200_OK


class BrokerNotResponding(GenericErrorResponse):
    error_code: ErrorCode = ErrorCode.BROKER_NOT_RESPONDING
    error_message: str = "Message broker is not responding"

    @staticmethod
    def status_code() -> status:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
