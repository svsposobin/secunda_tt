from collections import deque
from typing import Any, Dict, Optional

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.domains.organizations.core.constants import MAX_NESTING_ACTIVITY_LEVEL


class BaseValidationModel(BaseModel):

    @field_validator('*', mode="before")  # noqa  # type: ignore
    @classmethod
    def empty_validator(cls, value: Any, info: ValidationInfo) -> Any:
        field: Any = info.field_name
        if value in (None, "", [], {}, ()):
            raise ValueError(f"{field} не может быть пустым")

        return value


class ActivityTreeValidationModel(BaseValidationModel):
    activities: Dict[str, Any]

    def validate_nesting_level(self, max_level: int = MAX_NESTING_ACTIVITY_LEVEL) -> bool:
        """Проверка вложенности с использованием BFS (поиска в ширину) через очередь"""
        queue = deque([(self.activities, 1)])

        while queue:
            current_dict, level = queue.popleft()

            if level > max_level:
                return False

            for value in current_dict.values():
                if isinstance(value, dict) and value:
                    queue.append((value, level + 1))

        return True


class BuildingValidationModel(BaseValidationModel):
    building: Optional[str]


class ActivityValidationModel(BaseValidationModel):
    activity: Optional[str]


class RadiusValidationModel(BaseValidationModel):
    radius_km: float
    latitude: float
    longitude: float

    @field_validator("latitude", mode="after")  # noqa
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError("Широта должна быть в диапазоне от -90 до 90")
        return value

    @field_validator("longitude", mode="after")  # noqa
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if not -180 <= value <= 180:
            raise ValueError("Долгота должна быть в диапазоне от -180 до 180")
        return value

    @field_validator("radius_km", mode="after")  # noqa
    @classmethod
    def validate_radius(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Радиус не может быть меньше или равен 0")
        return value


class RectangleAreaValidationModel(BaseValidationModel):
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float

    @field_validator("min_latitude", "max_latitude", mode="after")  # noqa
    @classmethod
    def validate_latitude_range(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError('Широта должна быть в диапазоне от -90 до 90')
        return value

    @field_validator("min_longitude", "max_longitude", mode="after")  # noqa
    @classmethod
    def validate_longitude_range(cls, value: float) -> float:
        if not -180 <= value <= 180:
            raise ValueError("Долгота должна быть в диапазоне от -180 до 180")
        return value

    def fast_validate(self) -> None:
        if self.min_latitude >= self.max_latitude:
            raise ValueError("min_latitude должна быть меньше max_latitude")
        if self.min_longitude >= self.max_longitude:
            raise ValueError("min_longitude должна быть меньше max_longitude")


class OrganizationByIDValidationModel(BaseValidationModel):
    organization_id: int

    @field_validator("organization_id", mode="after")  # noqa
    @classmethod
    def validate_id(cls, value: Any) -> Any:
        if value <= 0:
            raise ValueError("Некорректный id организации")
        return value


class OrganizationByNameValidationModel(BaseValidationModel):
    name: str
