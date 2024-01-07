import requests

# API base URL
BASE_URL = "http://localhost:8080"


def create_city(data):
    """Create a new city."""
    response = requests.post(f"{BASE_URL}/cities/", json=data)
    return response.json()


def get_city(city_uuid):
    """Retrieve a single city by UUID."""
    response = requests.get(f"{BASE_URL}/cities/{city_uuid}")
    return response.json()


def get_cities():
    """Retrieve all cities."""
    response = requests.get(f"{BASE_URL}/cities/")
    return response.json()


def update_city(city_uuid, data):
    """Update a city by UUID."""
    response = requests.patch(f"{BASE_URL}/cities/{city_uuid}", json=data)
    return response.json()


def get_city_name_by_uuid(city_uuid):
    """Get the name of a city by its UUID."""
    try:
        city = get_city(city_uuid)
        return city.get("name", "Unknown City")
    except Exception as e:
        return f"Error Fetching City: {e}"


def print_city_state():
    """Print the state of each city with alliance names."""
    cities_response = get_cities()
    cities = cities_response["cities"]
    for city in cities:
        alliance_uuids = [
            alliance["allied_city_uuid"] for alliance in city["alliances"]
        ]
        alliance_names = [get_city_name_by_uuid(uuid) for uuid in alliance_uuids]
        print(f"City: {city['name']}, Alliances: {alliance_names}")
