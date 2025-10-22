from dataclasses import dataclass, field
from os import getenv
from typing import Dict

from src.core.common.constants import DEFAULT_POOL_KEY
from src.core.databases.setup.postgres import PostgreSQL
from dotenv import load_dotenv, find_dotenv

from src.core.databases.schemas import PoolSettings, DatabaseSchema

load_dotenv(find_dotenv(".env.test"))


@dataclass(frozen=True)
class Config:
    postgres: PostgreSQL
    pools_setting: Dict[str, PoolSettings] = field(default_factory=dict)


base_config: Config = Config(
    postgres=PostgreSQL(
        db=DatabaseSchema(
            HOST=getenv("DB_HOST"),  # type: ignore
            PORT=getenv("DB_PORT"),  # type: ignore
            USER=getenv("DB_USER"),  # type: ignore
            PASSWORD=getenv("DB_PASSWORD"),  # type: ignore
            DATABASE=getenv("DB_NAME"),  # type: ignore
        )  # Автосериализация
    ),
    pools_setting={
        DEFAULT_POOL_KEY: PoolSettings(
            pool_size=getenv("MAX_POOL_SIZE"),  # type: ignore
            max_overflow=getenv("MAX_OVERFLOW"),  # type: ignore
            pool_timeout=getenv("POOL_TIMEOUT"),  # type: ignore
            pool_recycle=getenv("POOL_RECYCLE"),  # type: ignore
            echo=False
        )
    }
)
