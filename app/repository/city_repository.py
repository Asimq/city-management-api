import logging
from typing import Dict, List

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.city_model import City


class CityRepository:
    """
    Static methods for managing City instances in the database.

    Provides functionality to add, retrieve, update, and delete City records,
    as well as additional operations like counting and fetching allied cities.
    """

    @staticmethod
    def add_city(db: Session, city_data: Dict) -> City:
        """ Add a new city record to the database. """
        new_city = City(**city_data)
        db.add(new_city)
        return new_city

    @staticmethod
    def get_city_by_uuid(db: Session, city_uuid: str) -> City:
        """ Retrieve a city by its UUID. """
        try:
            return db.query(City).filter(City.city_uuid == city_uuid).first()
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError occurred: {e}")
            raise

    @staticmethod
    def get_cities_by_uuids(db: Session, city_uuids: List[str]) -> List[City]:
        """ Retrieve cities by a list of UUIDs. """
        try:
            return db.query(City).filter(City.city_uuid.in_(city_uuids)).all()
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError occurred: {e}")
            raise

    @staticmethod
    def update_city(db, city: City, update_data: Dict) -> City:
        """ Update a city record with new data. """
        for attr, value in update_data.items():
            setattr(city, attr, value)
        return city

    @staticmethod
    def delete_city(db: Session, city: City):
        """ Delete a city record from the database. """
        db.delete(city)

    @staticmethod
    def get_cities(db: Session, skip: int, limit: int) -> List[City]:
        """ Retrieve a list of cities with pagination. """
        try:
            return db.query(City).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError occurred: {e}")
            raise

    @staticmethod
    def count_cities(db: Session) -> int:
        """ Count the number of cities in the database. """
        try:
            return db.query(City).count()
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError occurred: {e}")
            raise

    @staticmethod
    def get_allied_cities(db: Session, allied_city_uuids: List[str]) -> List[City]:
        """ Retrieve cities that are allied to specified cities. """
        try:
            return db.query(City).filter(City.city_uuid.in_(allied_city_uuids)).all()
        except SQLAlchemyError as e:
            logging.error(f"SQLAlchemyError occurred: {e}")
            raise
