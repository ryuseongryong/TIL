import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day35")
load_dotenv()

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
print(os.environ.get("API_KEY"))
API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LATITUDE")
LONG = os.getenv("LONGITUDE")
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
FROM_PHONE = os.getenv("FROM_PHONE")
TO_PHONE = os.getenv("TO_PHONE")

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
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Bring an Umbrella!!☔︎",
        from_=FROM_PHONE,
        to=TO_PHONE,
    )

    print(message.sid, message.status)
