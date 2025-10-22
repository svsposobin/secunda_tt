from typing import List, Dict, Any

from pydantic import BaseModel


class Organization(BaseModel):
    id: int
    name: str


class Phone(BaseModel):
    number: str


class Building(BaseModel):
    building: str
    address: str
    latitude: float
    longitude: float


class Activity(BaseModel):
    activity: Dict[str, Any]


class FullOrganizationInfo(BaseModel):
    organization: Organization
    phones: List[Phone]
    building: Building
    activity: Activity
