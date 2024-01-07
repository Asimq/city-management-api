import logging
from math import ceil

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from repository.city_repository import CityRepository
from services.alliance_service import AllianceService
from services.alliance_validation_service import AllianceValidationService
from services.allied_power_service import AlliedPowerService


class CityService:
    """
    Static methods for city management operations.

    Includes functionality for creating, reading, updating, and deleting cities,
    along with calculating allied power and managing alliances.
    """

    @staticmethod
    def create_city(db: Session, city_data, alliances):
        """
        Create a new city along with its alliances.
        """
        success = False
        new_city = None
        try:
            if alliances:
                AllianceValidationService.validate_alliance(
                    db, city_data, alliances, include_self_alliance_check=False
                )
            new_city = CityRepository.add_city(db, city_data)
            db.commit()
            db.refresh(new_city)
            if alliances:
                AllianceService.add_city_alliances(db, new_city.city_uuid, alliances)
                db.commit()
            success = True
            return new_city
        except ValueError as ve:
            raise ve
        except Exception as e:
            if new_city and not success:
                try:
                    CityRepository.delete_city(db, new_city)
                    db.commit()
                except SQLAlchemyError as e_cleanup:
                    db.rollback()
                    logging.error(
                        f"SQLAlchemyError occurred during cleanup: {e_cleanup}"
                    )
                    raise e_cleanup
            raise e

    @staticmethod
    def read_cities(db: Session, pagination):
        """
        Read a paginated list of cities.
        """
        total_count = CityRepository.count_cities(db)
        total_pages = ceil(total_count / pagination.page_size)
        if pagination.page > total_pages and total_count > 0:
            raise ValueError(f"Page must be less than or equal to {total_pages}")
        skip = (pagination.page - 1) * pagination.page_size
        cities = CityRepository.get_cities(db, skip, pagination.page_size)
        return cities, total_count, total_pages

    @staticmethod
    def read_city(db: Session, city_uuid):
        """
        Read a single city by its UUID.
        """
        city = CityRepository.get_city_by_uuid(db, city_uuid)
        if city:
            city.allied_power = AlliedPowerService.calculate_allied_power(db, city)
            return city
        else:
            raise ValueError("City not found")

    @staticmethod
    def update_city(db: Session, city_uuid, city_update):
        """
        Update a city by its UUID.
        """
        city = CityRepository.get_city_by_uuid(db, city_uuid)
        if not city:
            raise ValueError("City not found")
        update_data = city_update.dict(exclude_unset=True)
        if update_data:
            try:
                if "alliances" in update_data:
                    AllianceValidationService.validate_alliance(
                        db,
                        city,
                        update_data["alliances"],
                        include_self_alliance_check=True,
                    )
                    AllianceService.update_city_alliances(
                        db, city, update_data.pop("alliances")
                    )
                if update_data:
                    CityRepository.update_city(db, city, update_data)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                logging.error(f"SQLAlchemyError occurred: {e}")
                raise e
        return city

    @staticmethod
    def delete_city(db: Session, city_uuid):
        """
        Delete a city by its UUID.
        """
        city = CityRepository.get_city_by_uuid(db, city_uuid)
        if city:
            try:
                AllianceService.delete_city_alliances(db, city)
                CityRepository.delete_city(db, city)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                logging.error(f"SQLAlchemyError occurred: {e}")
                raise e
        else:
            raise ValueError("City not found")
