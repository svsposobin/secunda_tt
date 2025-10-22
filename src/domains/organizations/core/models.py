from typing import List, Dict, Any

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, VARCHAR, DOUBLE_PRECISION, JSON

from src.core.databases.base_models import BaseMeta


class Organizations(BaseMeta):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), unique=True, nullable=False)

    # Relationships:
    phones: Mapped[List["Phones"]] = relationship(
        argument="Phones", back_populates="organization", cascade="all, delete-orphan"
    )
    building: Mapped["Buildings"] = relationship(
        argument="Buildings", back_populates="organization", cascade="all, delete-orphan"
    )
    activity: Mapped["Activities"] = relationship(
        argument="Activities", back_populates="organization", cascade="all, delete-orphan"
    )


class Phones(BaseMeta):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey(column="organizations.id", ondelete="CASCADE"), nullable=False
    )
    number: Mapped[str] = mapped_column(VARCHAR(25), unique=True, nullable=False)

    # Relationships:
    organization: Mapped["Organizations"] = relationship(
        argument="Organizations", back_populates="phones"
    )


class Buildings(BaseMeta):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey(column="organizations.id"), nullable=False, unique=True)
    building: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    address: Mapped[str] = mapped_column(VARCHAR(150), nullable=False)
    latitude: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)
    longitude: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False)

    # Relationships:
    organization: Mapped["Organizations"] = relationship(
        argument="Organizations", back_populates="building"
    )


class Activities(BaseMeta):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey(column="organizations.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    activity: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Relationship
    organization: Mapped["Organizations"] = relationship(
        argument="Organizations", back_populates="activity"
    )
