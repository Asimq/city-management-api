import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.city_schema import CityCreate, CityDisplay, CityDisplayPower, CityPatch
from schemas.pagination_schema import PaginationParams, PaginatedResponseModel
from services.city_service import CityService

from config.db_postg import get_db

router = APIRouter()


@router.post("/", response_model=CityDisplay)
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    """
    Create a new city.
    Adds a city to the database with the provided details
    Returns the newly created city with uuid.
    """
    try:
        return CityService.create_city(
            db, city.dict(exclude={"alliances"}), city.alliances
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=PaginatedResponseModel)
async def read_cities(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    """
    Retrieve cities with pagination.
    Returns a list of cities, the total count, page size,
    total number of pages, with automatic pagination handling.
    """
    try:
        cities, total_count, total_pages = CityService.read_cities(db, pagination)
        return PaginatedResponseModel(
            total=total_count,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages,
            cities=[CityDisplay.from_orm(city) for city in cities],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{city_uuid}", response_model=CityDisplayPower)
async def read_city(city_uuid: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a single city.
    Returns details of a specific city by its UUID along with its allied power
    """
    try:
        return CityService.read_city(db, city_uuid)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{city_uuid}", response_model=CityDisplay)
async def update_city(
    city_uuid: UUID, city_update: CityPatch, db: Session = Depends(get_db)
):
    """
    Update a city. Modifies details of a specific city in the database.
    Only updates the fields provided in the request.
    """
    try:
        return CityService.update_city(db, city_uuid, city_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{city_uuid}")
async def delete_city(city_uuid: UUID, db: Session = Depends(get_db)):
    """
    Delete a city.
    Removes a specific city from the database along its alliances.
    """
    try:
        CityService.delete_city(db, city_uuid)
        return {"message": "City deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
