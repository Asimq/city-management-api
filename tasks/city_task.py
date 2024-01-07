from tasks.test_cities import berlin_data, new_york_data, munich_data
from tasks.city_api_utils import (
    create_city,
    update_city,
    print_city_state,
)


# Create Berlin
berlin = create_city(berlin_data)
berlin_uuid = berlin["city_uuid"]
print("Berlin created:", berlin)

# Create New York with Berlin as an ally
new_york_data["alliances"].append(berlin_uuid)
new_york = create_city(new_york_data)
new_york_uuid = new_york["city_uuid"]
print("New York created:", new_york)

# Create Munich allied with Berlin
munich_data["alliances"].append(berlin_uuid)
munich = create_city(munich_data)
munich_uuid = munich["city_uuid"]
print("Munich created:", munich)


print("\nState of each city after initial creation:")
print_city_state()

# Update the alliance of New York to ally it with Munich
if new_york_uuid and munich_uuid:
    update_city(new_york_uuid, {"alliances": [munich_uuid]})
    print("\nState of each city after updating New York's alliances:")
    print_city_state()
else:
    print("Error: Missing UUIDs for New York or Munich")
