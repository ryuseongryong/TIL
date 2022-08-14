import requests

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = ""

weather_params = {"lat": "", "lon": "", "appid": api_key}

requests.get(OWN_Endpoint, params=weather_params)
