from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from notes_sync.database import DeclarativeBase


class LogsequenceMessage(DeclarativeBase):
    __tablename__ = "logsequence_message"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    text = Column(String, nullable=False)

    user_obj = relationship("User", foreign_keys="LogsequenceMessage.user")
