from typing import List

from sqlalchemy.orm import Session

from repository.alliance_repository import AllianceRepository
from models.city_model import City, CityAlliances


class AllianceService:
    """
    Static methods for managing city alliances.

    Provides functionality to add, delete, and update alliances
    for a city using methods from AllianceRepository.
    """

    @staticmethod
    def add_city_alliances(db: Session, city_uuid: str, alliances: List[str]):
        """
        Add alliances for a given city.
        """
        alliance_objects = [
            CityAlliances(city_uuid=city_uuid, allied_city_uuid=alliance_uuid)
            for alliance_uuid in alliances
        ]
        alliance_objects += [
            CityAlliances(city_uuid=alliance_uuid, allied_city_uuid=city_uuid)
            for alliance_uuid in alliances
        ]
        AllianceRepository.add_city_alliances_bulk(db, alliance_objects)

    @staticmethod
    def delete_city_alliances(db: Session, city: City):
        """
        Delete all alliances for a given city.
        """
        alliance_pairs = [
            (city.city_uuid, alliance.allied_city_uuid) for alliance in city.alliances
        ]
        alliance_pairs += [
            (alliance.allied_city_uuid, city.city_uuid) for alliance in city.alliances
        ]
        AllianceRepository.delete_city_alliances_bulk(db, alliance_pairs)

    @staticmethod
    def update_city_alliances(db: Session, city: City, new_alliances: List[str]):
        """
        Update the alliances for a given city.
        """
        new_alliances_set = set(new_alliances)
        existing_alliances = {alliance.allied_city_uuid for alliance in city.alliances}
        to_remove = existing_alliances - new_alliances_set
        to_add = new_alliances_set - existing_alliances

        if to_remove:
            city_alliances_to_remove = [
                CityAlliances(city_uuid=city.city_uuid, allied_city_uuid=allied_uuid)
                for allied_uuid in to_remove
            ]
            city_with_alliances_to_remove = City(
                city_uuid=city.city_uuid, alliances=city_alliances_to_remove
            )
            AllianceService.delete_city_alliances(db, city_with_alliances_to_remove)
        if to_add:
            AllianceService.add_city_alliances(db, city.city_uuid, list(to_add))
