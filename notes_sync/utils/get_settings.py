from os import environ

from notes_sync.config.default import DefaultSettings


def get_settings() -> DefaultSettings:
    env = environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()
    return DefaultSettings()
