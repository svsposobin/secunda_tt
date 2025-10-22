from typing import Optional, Any, List

from pydantic import BaseModel

from src.domains.organizations.schemas.models_schemas import Organization, FullOrganizationInfo


class BaseResponse(BaseModel):
    result: List[Organization] | Any = []
    error: Optional[Any] = None


class ListOrganizationsInBuildingResponse(BaseResponse):
    pass


class ListOrganizationsWithActivityResponse(BaseResponse):
    pass


class ListOrganizationsPerRadiusResponse(BaseResponse):
    pass


class ListOrganizationsPerRectangleResponse(BaseResponse):
    pass


class OrganizationByIdResponse(BaseResponse):
    result: Optional[FullOrganizationInfo] = None


class OrganizationByNameResponse(BaseResponse):
    result: Optional[FullOrganizationInfo] = None
