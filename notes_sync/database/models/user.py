from typing import Self

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from notes_sync.database import DeclarativeBase
from notes_sync.schemas import SignupRequest, ConfigValue
from notes_sync.utils.auth import hash_pass


class User(DeclarativeBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    pass_hash = Column(String, index=True)
    logsequence_enable = Column(Boolean, default=False, nullable=False)

    def get_config(self) -> dict[str, object]:
        return {"logsequence.enable": self.logsequence_enable}

    def update_config(self, new_config: list[ConfigValue]):
        has_update = False
        for config in new_config:
            if config.name == "logsequence.enable":
                self.logsequence_enable = config.value
                has_update = True
        return has_update

    @staticmethod
    def from_request(request: SignupRequest) -> Self:
        return User(username=request.login, pass_hash=hash_pass(request.password))
