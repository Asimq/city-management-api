from typing import List, Generic, TypeVar

from pydantic import BaseModel, Field, ConfigDict


class PaginationParams(BaseModel):
    """
    Model for pagination parameters.
    """
    page: int = Field(default=1, gt=0, description="Page number")
    page_size: int = Field(default=10, gt=0, le=100, description="Page size limit")

    model_config = ConfigDict(extra='forbid')


Cities = TypeVar('Cities')


class PaginatedResponseModel(BaseModel, Generic[Cities]):
    """
    Generic model for paginated responses.
    """
    total: int
    page: int
    page_size: int
    total_pages: int
    cities: List[Cities]
