from enum import IntEnum

from fastapi.responses import JSONResponse
from pydantic import BaseModel, model_validator


class GenericSuccessResponseItems(BaseModel):
    count: int
    items: list[dict]

    @model_validator(mode="after")
    def must_be_exactly_count_items(self):
        if len(self.items) == self.count:
            raise ValueError(
                f"Wrong items count: len(items) != count ({len(self.items)} != {self.count})"
            )
        return self


class GenericSuccessResponse(BaseModel, JSONResponse):
    response: GenericSuccessResponseItems


class ErrorCode(IntEnum):
    USER_ALREADY_EXISTS = 0


class GenericErrorResponse(BaseModel, JSONResponse):
    error_code: ErrorCode
    error_message: str = ""
