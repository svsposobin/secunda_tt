from typing import Protocol


class DatabaseInterface(Protocol):
    def dsn(self) -> str:
        raise NotImplementedError()
