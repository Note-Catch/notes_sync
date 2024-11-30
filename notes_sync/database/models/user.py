from typing import Self

from sqlalchemy import event, DDL, Column, Integer, String
from sqlalchemy.orm import relationship

from notes_sync.database import DeclarativeBase
from notes_sync.schemas import SignupRequest
from notes_sync.utils.auth import hash_pass


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    pass_hash = Column(String, index=True)

    # Relationship to Config model
    configs = relationship("Config", back_populates="user")

    @staticmethod
    def from_request(request: SignupRequest) -> Self:
        return User(username=request.username, pass_hash=hash_pass(request.password))


setup_user_config_trigger = DDL(
    R"CREATE TRIGGER IF NOT EXISTS setup_user_config AFTER INSERT ON user "
    R"BEGIN "
    R"INSERT INTO config(name, value, user) "
    R"  SELECT (config_defaults.name, config_defaults.value, NEW.id) FROM config_defaults"
    R"END;"
)


event.listen(User.__table__, "after_create", setup_user_config_trigger)
