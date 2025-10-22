from typing import Optional

from fastapi import HTTPException, status, Depends, Header
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.common.encryptor import EncryptorProcessor
from src.core.common.state import GlobalAppState
from src.domains.auth.core.constants import AUTH_HEADER_KEY
from src.domains.auth.core.models import AuthKeys


class AuthDependenciesRepository:

    @staticmethod
    async def check_key_with_raise_if_unvalid(
            session: AsyncSession = Depends(GlobalAppState.get_psql_session),
            key: Optional[str] = Header(default="TEST_KEY_1", alias=AUTH_HEADER_KEY)
    ) -> None:
        if not key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied!")

        result: Optional[bool] = await session.scalar(
            select(exists().where(AuthKeys.hash_key == EncryptorProcessor.encrypt(key)))
        )

        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied!")
