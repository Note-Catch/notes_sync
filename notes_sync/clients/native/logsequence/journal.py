from pathlib import Path
from datetime import datetime


class JournalNotFound(RuntimeError):
    pass


class Journal:
    FILE_EXTENSION = "MD".lower()

    def __init__(self, path: Path, date: datetime, date_format: str, time_format: str):
        self.path = path / f"{date.strftime(date_format)}.{Journal.FILE_EXTENSION}"
        if not self.path.is_file():
            raise JournalNotFound()
        self.time_format = time_format

    def write_message(self, date: datetime, message: str):
        with open(self.path, "a") as file:
            print("\n-", date.strftime(self.time_format), file=file)
            print("\t-", message, file=file)
