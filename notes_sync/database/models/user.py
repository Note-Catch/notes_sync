from sqlalchemy import Column, Integer, String

from notes_sync.database import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    pass_hash = Column(String, index=True)
