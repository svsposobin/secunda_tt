from datetime import datetime

from sqlalchemy import DateTime, func, LargeBinary
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import VARCHAR, SmallInteger

from src.core.databases.base_models import BaseMeta


class AuthKeys(BaseMeta):
    __tablename__ = "auth_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hash_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    is_active: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Дата создания ключа в UTC"
    )
