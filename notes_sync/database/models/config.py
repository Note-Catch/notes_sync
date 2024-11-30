from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from notes_sync.database import DeclarativeBase


class ConfigDefaults(DeclarativeBase):
    __tablename__ = "config_defaults"

    name = Column(String, primary_key=True, index=True)
    value = Column(String)


class Config(DeclarativeBase):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    value = Column(String)
    user = Column(
        Integer, ForeignKey("user.id"), primary_key=True, index=True, nullable=False
    )

    # Relationship to the User model
    user = relationship(
        "User", back_populates="configs"
    )  # Establish bidirectional relationship
