from typing import Optional

from pydantic import BaseModel


class DatabaseSchema(BaseModel):
    HOST: str
    PORT: str
    USER: str
    PASSWORD: Optional[str]
    DATABASE: str


class PoolSettings(BaseModel):
    pool_size: int
    max_overflow: int
    pool_timeout: int
    pool_recycle: int
    echo: bool
