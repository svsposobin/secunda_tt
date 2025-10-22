from src.domains.organizations.core.models import Organizations
from src.domains.organizations.schemas.models_schemas import (
    FullOrganizationInfo,
    Organization,
    Phone,
    Building,
    Activity
)


class ModelParser:

    @staticmethod
    def parse_full_organization_info(organization: Organizations) -> FullOrganizationInfo:
        return FullOrganizationInfo(
            organization=Organization(id=organization.id, name=organization.name),
            phones=[Phone(number=phone_obj.number) for phone_obj in organization.phones],
            building=Building(
                building=organization.building.building, address=organization.building.address,
                latitude=organization.building.latitude, longitude=organization.building.longitude
            ),
            activity=Activity(activity=organization.activity.activity)
        )
