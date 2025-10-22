from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class GlobalAppState:

    @staticmethod
    async def get_psql_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
        async with request.app.state.psql_session_factory() as session:
            try:
                yield session

            except SQLAlchemyError:  # При необходимости можно указать конкретные ошибки для микро-оптимизации
                await session.rollback()

                raise
