from typing import Sequence, Optional

from fastapi import Depends, Query
from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.common.state import GlobalAppState
from src.domains.auth.core.dependencies import AuthDependenciesRepository
from src.domains.organizations.core.models import Buildings, Activities, Organizations
from src.domains.organizations.core.parsers import ModelParser
from src.domains.organizations.queries.select import (
    select_list_organizations_in_current_building,
    select_list_organizations_per_radius,
    select_list_organizations_in_rectangle,
    select_list_organizations_with_current_activity_type,
    select_full_organization_by_id,
    select_full_organization_by_name
)
from src.domains.organizations.schemas.models_schemas import Organization
from src.domains.organizations.schemas.response import (
    ListOrganizationsInBuildingResponse,
    ListOrganizationsWithActivityResponse,
    ListOrganizationsPerRadiusResponse,
    ListOrganizationsPerRectangleResponse,
    OrganizationByIdResponse,
    OrganizationByNameResponse,
)
from src.domains.organizations.schemas.validation import (
    BuildingValidationModel,
    ActivityValidationModel,
    RadiusValidationModel,
    RectangleAreaValidationModel,
    OrganizationByIDValidationModel,
    OrganizationByNameValidationModel,
)

"""
    Примечания:
    При необходимости и в масштабируемом сервисе лучше разбивать зависимости на доп. модули и репозитории
"""


async def list_of_organizations_in_a_specific_building(
        auth_key=Depends(AuthDependenciesRepository.check_key_with_raise_if_unvalid),  # noqa
        session: AsyncSession = Depends(GlobalAppState.get_psql_session),
        building: Optional[str] = Query(
            default=None, description="Здание, по которому будет происходить поиск. Пример: Брюхина 24/1"
        )
) -> ListOrganizationsInBuildingResponse:
    """Метод получения списка организаций в конкретном здании"""
    response = ListOrganizationsInBuildingResponse()
    BuildingValidationModel(building=building)

    result: ScalarResult[Buildings] = await session.scalars(
        select_list_organizations_in_current_building(building=building)  # type: ignore
    )
    sequence_result: Sequence[Buildings] = result.all()

    if not sequence_result:
        return response

    for obj in sequence_result:
        response.result.append(  # type: ignore
            Organization(
                id=obj.organization.id,
                name=obj.organization.name
            )
        )

    return response


async def list_of_organizations_per_radius(
        auth_key=Depends(AuthDependenciesRepository.check_key_with_raise_if_unvalid),  # noqa
        session: AsyncSession = Depends(GlobalAppState.get_psql_session),
        latitude: float = Query(
            default=None,
            description="Широта центральной точки поиска. Не меньше -90 и не больше 90", examples=[55.7558]
        ),
        longitude: float = Query(
            default=None,
            description="Долгота центральной точки поиска. Не меньше -180 и не больше 180", examples=[37.6173]
        ),
        radius_km: float = Query(
            default=None,
            description="Радиус поиска в километрах. Не меньше 0", examples=[5.0]
        )
) -> ListOrganizationsPerRadiusResponse:
    """Метод получения списка организаций в конкретном радиусе (круговой области)"""
    response = ListOrganizationsPerRadiusResponse()
    RadiusValidationModel(
        latitude=latitude, longitude=longitude, radius_km=radius_km
    )

    result: ScalarResult[Organizations] = await session.scalars(
        select_list_organizations_per_radius(
            latitude=latitude, longitude=longitude, radius_km=radius_km
        )
    )
    sequence_result: Sequence[Organizations] = result.all()

    if not sequence_result:
        return response

    for obj in sequence_result:
        response.result.append(
            Organization(
                id=obj.id,
                name=obj.name
            )
        )

    return response


async def list_of_organizations_in_rectangle_area(
        auth_key=Depends(AuthDependenciesRepository.check_key_with_raise_if_unvalid),  # noqa
        session: AsyncSession = Depends(GlobalAppState.get_psql_session),
        min_latitude: float = Query(
            default=None,
            description="Минимальная широта (южная граница). Не меньше -90 и не больше 90", examples=[55.7000]
        ),
        max_latitude: float = Query(
            default=None,
            description="Максимальная широта (северная граница). Не меньше -90 и не больше 90", examples=[55.8000]
        ),
        min_longitude: float = Query(
            default=None,
            description="Минимальная долгота (западная граница). Не меньше -180 и не больше 180", examples=[37.6000]
        ),
        max_longitude: float = Query(
            default=None,
            description="Максимальная долгота (восточная граница). Не меньше -180 и не больше 180", examples=[37.7000]
        )
) -> ListOrganizationsPerRectangleResponse:
    """Метод получения списка организаций в прямоугольной области"""
    response = ListOrganizationsPerRectangleResponse()
    RectangleAreaValidationModel(
        min_latitude=min_latitude, max_latitude=max_latitude,
        min_longitude=min_longitude, max_longitude=max_longitude
    ).fast_validate()

    result: ScalarResult[Organizations] = await session.scalars(
        select_list_organizations_in_rectangle(
            min_latitude=min_latitude, max_latitude=max_latitude,
            min_longitude=min_longitude, max_longitude=max_longitude
        )
    )
    sequence_result: Sequence[Organizations] = result.all()

    for obj in sequence_result:
        response.result.append(
            Organization(
                id=obj.id,
                name=obj.name
            )
        )

    return response


async def list_of_organizations_with_type_of_activity(
        auth_key=Depends(AuthDependenciesRepository.check_key_with_raise_if_unvalid),  # noqa
        session: AsyncSession = Depends(GlobalAppState.get_psql_session),
        activity: Optional[str] = Query(
            default=None, description="Вид деятельности организации. Пример: Еда"
        )
) -> ListOrganizationsWithActivityResponse:
    """Метод получения списка организаций по конкретному типу деятельности"""
    response = ListOrganizationsWithActivityResponse()
    ActivityValidationModel(activity=activity)

    result: ScalarResult[Activities] = await session.scalars(
        select_list_organizations_with_current_activity_type(activity_type=activity)  # type: ignore
    )
    sequence_result: Sequence[Activities] = result.all()

    if not sequence_result:
        return response

    for obj in sequence_result:
        response.result.append(  # type: ignore
            Organization(
                id=obj.organization.id,
                name=obj.organization.name
            )
        )

    return response


async def organization_by_id(
        auth_key=Depends(AuthDependenciesRepository.check_key_with_raise_if_unvalid),  # noqa
        session: AsyncSession = Depends(GlobalAppState.get_psql_session),
        organization_id: int = Query(
            default=None, description="id организации"
        )
) -> OrganizationByIdResponse:
    """Метод получения полной информации об организации по идентификатору"""
    response = OrganizationByIdResponse()
    OrganizationByIDValidationModel(organization_id=organization_id)

    result: Optional[Organizations] = await session.scalar(
        select_full_organization_by_id(organization_id=organization_id)
    )

    if not result:
        return response

    response.result = ModelParser.parse_full_organization_info(organization=result)

    return response


async def organization_by_name(
        auth_key=Depends(AuthDependenciesRepository.check_key_with_raise_if_unvalid),  # noqa
        session: AsyncSession = Depends(GlobalAppState.get_psql_session),
        organization_name: str = Query(
            default=None, description="Название организации"
        )
) -> OrganizationByNameResponse:
    """Метод получения полной информации об организации по названию"""
    response = OrganizationByNameResponse()
    OrganizationByNameValidationModel(name=organization_name)

    result: Optional[Organizations] = await session.scalar(
        select_full_organization_by_name(organization_name=organization_name)
    )

    if not result:
        return response

    response.result = ModelParser.parse_full_organization_info(organization=result)

    return response
