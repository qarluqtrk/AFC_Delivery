from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_geocoder")


def get_location(longitude, latitude):
    location = geolocator.reverse((f"{latitude}, {longitude}"))
    return location
