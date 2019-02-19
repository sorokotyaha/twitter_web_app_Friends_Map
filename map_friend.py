import json
import folium
import twitter3
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import copy


def get_locations(path):
    geolocator = Nominatim(user_agent="film_data.py")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    locations = {}
    with open(path, encoding="UTF-8") as file:
        file = json.load(file)
        for friend in file["users"]:
            if friend["location"]:
                loc = geolocator.geocode(friend["location"])
                loc_key = str(loc.latitude) + " " + str(loc.longitude)
                if loc_key not in locations:
                    locations[loc_key] = [friend["screen_name"]]
                else:
                    locations[loc_key].append(friend["screen_name"])
    return locations


def generate_map(loc_dict):
    base_map = folium.Map()
    fm = folium.FeatureGroup(name="Friends Map")

    for loc in loc_dict:
        names = ", ".join(loc_dict[loc])
        loc_copy = copy.copy(loc)
        loc_copy = loc.split()
        lat = loc_copy[0]
        lon = loc_copy[1]
        fm.add_child(folium.Marker(location=[float(lat), float(lon)],
                                   popup=names,
                                   icon=folium.Icon()))
    base_map.add_child(fm)
    base_map.add_child(folium.LayerControl())
    base_map.save('Map_Friend.html')


if __name__ == "__main__":
    my_path = twitter3.get_twitter_json()
    locations = get_locations(path=my_path)
    generate_map(locations)

    print("Done, my master...")

