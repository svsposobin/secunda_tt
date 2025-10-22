from fastapi import APIRouter

from src.domains.organizations.apis.v1.routes import SingleOrganizationsRoutesRepository


class OrganizationAPIRouterV1:
    router: APIRouter = APIRouter(prefix="/api/v1/organizations", tags=["ORGANIZATIONS"])

    router.get(
        path="/by-building",
        description="Получение списка организаций в конкретном здании"
    )(SingleOrganizationsRoutesRepository.get_organizations_in_current_building)

    router.get(
        path="/by-activity",
        description="Получение списка организаций с конкретным видом деятельности"
    )(SingleOrganizationsRoutesRepository.get_organizations_with_current_activity)

    router.get(
        path="/by-radius",
        description="Получение списка организаций, находящихся в заданной плоскости с радиусом разброса"
    )(SingleOrganizationsRoutesRepository.get_organizations_per_radius)

    router.get(
        path="/by-rectangle",
        description="Получение списка организаций, входящих в указанную область"
    )(SingleOrganizationsRoutesRepository.get_organizations_in_rectange_area)

    router.get(
        path="/by-id",
        description="Получение полной информации об организации по ее идентификатору"
    )(SingleOrganizationsRoutesRepository.get_full_organization_by_id)

    router.get(
        path="/by-name",
        description="Получение полной информации об организации по ее названию"
    )(SingleOrganizationsRoutesRepository.get_full_organization_by_name)
