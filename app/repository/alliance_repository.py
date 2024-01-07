from typing import List

from sqlalchemy.orm import Session

from models.city_model import CityAlliances


class AllianceRepository:
    """
    Static methods for managing CityAlliances in the database.

    Offers functionality to add and delete alliances in bulk,
    to be used with a SQLAlchemy Session instance.
    """

    @staticmethod
    def add_city_alliances_bulk(db: Session, alliances: List[CityAlliances]):
        """Bulk add alliance records to the database."""
        db.bulk_save_objects(alliances)

    @staticmethod
    def delete_city_alliances_bulk(db: Session, city_uuid_pairs: List[tuple]):
        """Bulk delete alliance records from the database."""
        for city_uuid1, city_uuid2 in city_uuid_pairs:
            db.query(CityAlliances).filter(
                CityAlliances.city_uuid == city_uuid1,
                CityAlliances.allied_city_uuid == city_uuid2,
            ).delete(synchronize_session="fetch")
