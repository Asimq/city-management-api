import logging

from sqlalchemy.orm import Session
from geopy.distance import geodesic

from models.city_model import City
from repository.city_repository import CityRepository


class AlliedPowerService:
    """
    Static methods for calculating allied power and distances between
    cities. Calculates the distance between two geographical points and
    determines the allied power of a city based on the population of
    its allies.
    """

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
        """
        Calculate the distance between two points on Earth using geopy.

        Args:
            lat1 (float): Latitude of the first point.
            lon1 (float): Longitude of the first point.
            lat2 (float): Latitude of the second point.
            lon2 (float): Longitude of the second point.

        Returns:
            int: The distance in kilometers, rounded to the nearest integer.
        """
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)

        # Calculate the distance in kilometers
        distance = geodesic(point1, point2).kilometers
        return round(distance)

    @staticmethod
    def calculate_allied_power(db: Session, city: City) -> int:
        """
        Calculate the allied power of a city based on its population and
        the population of its allies.

        Returns:
            int: The calculated allied power of the city.
        """
        allied_power = city.population
        allied_cities = CityRepository.get_allied_cities(
            db, [alliance.allied_city_uuid for alliance in city.alliances]
        )
        for allied_city in allied_cities:
            try:
                distance = AlliedPowerService.calculate_distance(
                    city.geo_location_latitude, 
                    city.geo_location_longitude, 
                    allied_city.geo_location_latitude, 
                    allied_city.geo_location_longitude
                )
                allied_population = allied_city.population
                if distance > 10000:
                    allied_population = round(allied_population / 4)
                elif distance > 1000:
                    allied_population = round(allied_population / 2)

                allied_power += allied_population
            except Exception as e:
                logging.error(
                    f"Error in calculating distance for allied cities: {e}"
                )
                raise
        return allied_power
