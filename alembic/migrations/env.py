import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from src.core.databases.base_models import BaseMeta
from src.core.root.config import base_config

# <Models for correct migration work>:
from src.domains.auth.core.models import AuthKeys  # noqa
from src.domains.organizations.core.models import (  # noqa
    Organizations,
    Phones,
    Buildings,
    Activities
)

config = context.config

config.set_main_option("sqlalchemy.url", base_config.postgres.dsn() + "?async_fallback=True")
config.set_main_option("prepend_sys_path", ".")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseMeta.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_server_default=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
