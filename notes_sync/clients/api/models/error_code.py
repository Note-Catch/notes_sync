from enum import IntEnum


class ErrorCode(IntEnum):
    VALUE_0 = 0

    def __str__(self) -> str:
        return str(self.value)
