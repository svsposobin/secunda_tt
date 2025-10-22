from fastapi import Depends

from src.domains.organizations.core.dependencies import list_of_organizations_in_a_specific_building, \
    list_of_organizations_with_type_of_activity, list_of_organizations_per_radius, \
    list_of_organizations_in_rectangle_area, organization_by_id, organization_by_name
from src.domains.organizations.schemas.response import ListOrganizationsInBuildingResponse, \
    ListOrganizationsWithActivityResponse, ListOrganizationsPerRadiusResponse, ListOrganizationsPerRectangleResponse, \
    OrganizationByIdResponse, OrganizationByNameResponse


class SingleOrganizationsRoutesRepository:

    @staticmethod
    async def get_organizations_in_current_building(
            result: ListOrganizationsInBuildingResponse = Depends(list_of_organizations_in_a_specific_building)
    ):
        return result

    @staticmethod
    async def get_organizations_with_current_activity(
            result: ListOrganizationsWithActivityResponse = Depends(list_of_organizations_with_type_of_activity)
    ):
        return result

    @staticmethod
    async def get_organizations_per_radius(
            result: ListOrganizationsPerRadiusResponse = Depends(list_of_organizations_per_radius)
    ):
        return result

    @staticmethod
    async def get_organizations_in_rectange_area(
            result: ListOrganizationsPerRectangleResponse = Depends(list_of_organizations_in_rectangle_area)
    ):
        return result

    @staticmethod
    async def get_full_organization_by_id(
            result: OrganizationByIdResponse = Depends(organization_by_id)
    ):
        return result

    @staticmethod
    async def get_full_organization_by_name(
            result: OrganizationByNameResponse = Depends(organization_by_name)
    ):
        return result
