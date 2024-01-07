import re
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, ConfigDict, UUID4, validator, Field

class BeautyEnum(str, Enum):
    """ Enum for city beauty ratings. """
    ugly = "Ugly"
    average = "Average"
    gorgeous = "Gorgeous"

class CityBase(BaseModel):
    """
    Base model for city data.
    """
    name: str = Field(..., min_length=3, max_length=100, 
                      description="City name")
    geo_location_latitude: float = Field(..., ge=-90.0, le=90.0, 
                                         description="Latitude")
    geo_location_longitude: float = Field(..., ge=-180.0, le=180.0, 
                                          description="Longitude")
    beauty: BeautyEnum = Field(..., 
                               description="Beauty rating")
    population: int = Field(..., ge=1, le=1000000000, 
                            description="Population count")

    model_config = ConfigDict(extra='forbid')

    @validator('name')
    def validate_name(cls, v):
        """ Ensure name is alphabetic with spaces. """
        if not re.match("^[a-zA-Z ]{3,100}$", v):
            raise ValueError(
                'Name must only contain letters and spaces, up to 100 characters'
            )
        return v

    @validator('geo_location_latitude', 'geo_location_longitude')
    def validate_geo_precision(cls, v):
        """ Ensure geo-locations have at most 6 decimal places. """
        if len(str(v).split('.')[-1]) > 6:
            raise ValueError('Geo-location should not have more than 6 decimal places')
        return v

class CityCreate(CityBase):
    """
    Model for creating a new city.
    """
    alliances: Optional[List[UUID4]] = []

class CityAllianceDisplay(BaseModel):
    """
    Model for displaying city alliances.
    """
    allied_city_uuid: UUID4

    model_config = ConfigDict(from_attributes=True)

class CityDisplayPower(CityBase):
    """
    Extended city model including power metrics for display purposes.
    """
    city_uuid: UUID4
    alliances: Optional[List[CityAllianceDisplay]] = []
    allied_power: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class CityDisplay(CityBase):
    """
    City model for general display purposes.
    """
    city_uuid: UUID4
    alliances: Optional[List[CityAllianceDisplay]] = []

    model_config = ConfigDict(from_attributes=True)

class CityPatch(CityBase):
    """
    Model for patching city data.
    """
    name: Optional[str] = None
    geo_location_latitude: Optional[float] = None
    geo_location_longitude: Optional[float] = None
    beauty: Optional[BeautyEnum] = None
    population: Optional[int] = None
    alliances: Optional[List[UUID4]] = []
