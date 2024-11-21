from typing import Self

from sqlalchemy import Column, Integer, String

from notes_sync.database import DeclarativeBase
from notes_sync.schemas import SignupRequest
from notes_sync.utils.auth import hash_pass


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    pass_hash = Column(String, index=True)

    @staticmethod
    def from_request(request: SignupRequest) -> Self:
        return User(username=request.username, pass_hash=hash_pass(request.password))
