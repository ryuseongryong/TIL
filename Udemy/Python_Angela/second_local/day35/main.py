import requests
import os
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day35")
load_dotenv()

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LATITUDE")
LONG = os.getenv("LONGITUDE")

weather_params = {
    "lat": LAT,
    "lon": LONG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily",
}

res = requests.get(OWN_Endpoint, params=weather_params)
res.raise_for_status()
weather_data = res.json()
weather_slice = weather_data["hourly"][:12]


will_rain = False

for hour_data in weather_slice:
    condition_code = int(hour_data["weather"][0]["id"])
    if condition_code < 700:
        will_rain = True

if will_rain:
    print("Bring an Umbrella!!")
