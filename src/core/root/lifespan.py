from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from src.core.common.constants import DEFAULT_POOL_KEY
from src.core.root.config import base_config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    default_engine: AsyncEngine = create_async_engine(
        url=base_config.postgres.dsn(),
        **base_config.pools_setting.get(DEFAULT_POOL_KEY).model_dump()  # type: ignore
    )
    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=default_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    app.state.psql_session_factory = session_factory  # noqa

    yield

    await default_engine.dispose()
