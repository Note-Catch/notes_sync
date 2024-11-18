from sqlalchemy import Column, Integer, String

from notes_sync.database import DeclarativeBase


class LogsequenceMessage(DeclarativeBase):
    __tablename__ = "logsequence_message"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, index=True)
    message = Column(String, nullable=False)
