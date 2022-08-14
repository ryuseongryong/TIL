import requests
import os
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day35")
load_dotenv()

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LATITUDE")
LONG = os.getenv("LONGITUDE")

weather_params = {"lat": LAT, "lon": LONG, "appid": API_KEY}

res = requests.get(OWN_Endpoint, params=weather_params)
print(res.json())
