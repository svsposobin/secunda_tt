from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload

from src.domains.organizations.core.models import Buildings, Organizations, Activities

"""
При необходимости и в масштабируемом сервисе лучше разбивать зависимости на репозитории запросов
"""


def select_list_organizations_in_current_building(building: str) -> Select:
    return (
        select(Buildings)
        .options(joinedload(Buildings.organization))
        .filter(Buildings.building == building.lower())
    )


def select_list_organizations_per_radius(latitude: float, longitude: float, radius_km: float) -> Select:
    degree_offset = radius_km / 111.0  # 1 градус примерно 111 км

    return (
        select(Organizations)
        .join(Buildings, Organizations.id == Buildings.organization_id)
        .filter(
            Buildings.latitude.between(latitude - degree_offset, latitude + degree_offset),
            Buildings.longitude.between(longitude - degree_offset, longitude + degree_offset)
        )
    )


def select_list_organizations_in_rectangle(
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float
) -> Select:
    return (
        select(Organizations)
        .join(Buildings, Organizations.id == Buildings.organization_id)
        .filter(
            Buildings.latitude.between(min_latitude, max_latitude),
            Buildings.longitude.between(min_longitude, max_longitude)
        )
    )


def select_list_organizations_with_current_activity_type(activity_type: str) -> Select:
    return (
        select(Activities)
        .options(joinedload(Activities.organization))
        .filter(Activities.activity[activity_type.lower()] != None)  # noqa
    )


def select_full_organization_by_id(organization_id: int) -> Select:
    return (
        select(Organizations)
        .options(
            joinedload(Organizations.phones),
            joinedload(Organizations.building),
            joinedload(Organizations.activity)
        )
        .filter(Organizations.id == organization_id)
    )


def select_full_organization_by_name(organization_name: str) -> Select:
    return (
        select(Organizations)
        .options(
            joinedload(Organizations.phones),
            joinedload(Organizations.building),
            joinedload(Organizations.activity)
        )
        .filter(Organizations.name == organization_name.lower())
    )
