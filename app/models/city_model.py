import logging
import uuid
import enum
from datetime import datetime

from sqlalchemy import (Column, Integer, String, Float, Enum as SQLAlchemyEnum,
    ForeignKey, BigInteger, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError

from config.db_postg import get_engine

Base = declarative_base()


class BeautyEnum(enum.Enum):
    """ Enumeration for beauty ratings of a city. """
    Ugly = "Ugly"
    Average = "Average"
    Gorgeous = "Gorgeous"


class City(Base):
    """
    SQLAlchemy model representing a city.

    Attributes:
        city_uuid (UUID): Unique identifier for the city.
        name (String): Name of the city.
        geo_location_latitude (Float): Latitude of the city's geolocation.
        geo_location_longitude (Float): Longitude of the city's geolocation.
        beauty (BeautyEnum): Aesthetic appeal rating of the city.
        population (BigInteger): Population of the city.
        alliances (relationship): Relationships to allied cities.
        created_at (DateTime): Record creation timestamp.
        updated_at (DateTime): Record update timestamp.
    """
    __tablename__ = 'city'
    city_uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
        )
    name = Column(String, nullable=False)
    geo_location_latitude = Column(Float, nullable=False)
    geo_location_longitude = Column(Float, nullable=False)
    beauty = Column(
        SQLAlchemyEnum(BeautyEnum, name='beauty_type'),
        nullable=False
        )
    population = Column(BigInteger, nullable=False)
    alliances = relationship("CityAlliances", 
                             foreign_keys="CityAlliances.city_uuid", 
                             back_populates="city")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
        )


class CityAlliances(Base):
    """
    SQLAlchemy model representing alliances between cities.

    Attributes:
        alliance_id (Integer): Primary key of the alliance.
        city_uuid (UUID): UUID of the city forming the alliance.
        allied_city_uuid (UUID): UUID of the allied city.
        city (relationship): Relationship to the city forming the alliance.
        created_at (DateTime): Record creation timestamp.
        updated_at (DateTime): Record update timestamp.
    """
    __tablename__ = 'city_alliances'
    alliance_id = Column(Integer, primary_key=True)
    city_uuid = Column(
        UUID(as_uuid=True), ForeignKey('city.city_uuid'),
        nullable=False, index=True
        )
    allied_city_uuid = Column(
        UUID(as_uuid=True), ForeignKey('city.city_uuid'),
        nullable=False, index=True
        )
    city = relationship("City", 
                        foreign_keys=[city_uuid],
                        back_populates="alliances")
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables in the database
try:
    Base.metadata.create_all(bind=get_engine())
except SQLAlchemyError as e:
    logging.error(f"SQLAlchemyError occurred: {e}")
    raise
