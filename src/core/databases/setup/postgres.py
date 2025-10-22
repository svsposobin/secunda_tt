from typing import Optional

from src.core.databases.interface import DatabaseInterface
from src.core.databases.schemas import DatabaseSchema


class PostgreSQL(DatabaseInterface):
    def __init__(self, db: DatabaseSchema, driver: str = "psycopg") -> None:
        # PSQL - ENV
        self._HOST: str = db.HOST
        self._PORT: str = db.PORT
        self._USER: str = db.USER
        self._PASSWORD: Optional[str] = db.PASSWORD
        self._DATABASE: str = db.DATABASE
        # DSN - ENV
        self._DRIVER: str = driver

    def dsn(self) -> str:
        return f"postgresql+{self._DRIVER}://{self._USER}:{self._PASSWORD}@{self._HOST}:{self._PORT}/{self._DATABASE}"
