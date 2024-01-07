from typing import List

from sqlalchemy.orm import Session

from models.city_model import City
from repository.city_repository import CityRepository


class AllianceValidationService:
    """
    Static method for validating city alliances.

    Provides functionality to validate the formation of alliances
    between cities, including checks for duplicate alliances,
    self-alliances, and the existence of alliance city UUIDs.
    """

    @staticmethod
    def validate_alliance(
        db: Session,
        city: City,
        alliances: List[str],
        include_self_alliance_check: bool = False,
    ):
        """
        Validate if an alliance can be formed with the given city and alliances.

        Raises ValueError if duplicate alliances, self-alliances,
          or non-existing city UUIDs are found.
        """
        # Check for unique alliances
        if len(alliances) != len(set(alliances)):
            raise ValueError("Duplicate alliances found")

        # Retrieve all cities that match the UUIDs in alliances
        existing_cities = CityRepository.get_cities_by_uuids(db, alliances)
        existing_city_uuids = {c.city_uuid for c in existing_cities}

        for alliance_uuid in alliances:
            # Check for self-alliance if the flag is True
            if include_self_alliance_check and city.city_uuid == alliance_uuid:
                raise ValueError("A city cannot form an alliance with itself")

            # Check if each alliance city exists
            if alliance_uuid not in existing_city_uuids:
                raise ValueError(
                    f"City UUID {alliance_uuid} does not exist for alliance"
                )
