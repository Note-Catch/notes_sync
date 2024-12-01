from pydantic import BaseModel


class MessagePostRequest(BaseModel):
    text: str
