# from animal.dog import Dog와 같음

import ssl
import certifi
import geopy.geocoders
from geopy.geocoders import Nominatim

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

# geolocator = Nominatim(scheme='http')

geolocator = Nominatim(user_agent="seongryong")
location = geolocator.geocode("175 5th Avenue NYC")
location = geolocator.geocode("gangnamgu police")
print(location)