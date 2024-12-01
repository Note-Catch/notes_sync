from typing import TypeAlias

from pydantic import BaseModel
from fastapi import status


class ConfigLogsequenceEnable(BaseModel):
    name: str = "logsequence.enable"
    value: bool


ConfigValue: TypeAlias = ConfigLogsequenceEnable


class ConfigGetResponse(BaseModel):
    config: dict[str, object]

    @staticmethod
    def status_code() -> status:
        return status.HTTP_200_OK


class ConfigPutRequest(BaseModel):
    config: list[ConfigValue]
