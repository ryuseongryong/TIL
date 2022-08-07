from multiprocessing import connection
import smtplib
from time import sleep
import requests
import datetime


MY_EMAIL = "ryuseongryong@gmail.com"
MY_PASSWORD = ""
MY_LAT = 37.450027
MY_LONG = 126.906663


def is_iss_overhead():
    res = requests.get(url="http://api.open-notify.org/iss-now.json")
    res.raise_for_status()
    data = res.json()

    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])

    iss_position = (latitude, longitude)

    if MY_LAT - 5 <= latitude <= MY_LAT + 5 and MY_LONG - 5 <= longitude <= MY_LONG + 5:
        return True


def is_night():
    url = "http://api.sunrise-sunset.org/json"
    params = {"lat": MY_LAT, "long": MY_LONG, "formatted": 0}
    # url = f"http://api.sunrise-sunset.org/json?lat={MY_LAT}&lng={MY_LONG}"

    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.datetime.now()

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look up the Sky!\n\nThe ISS is above you in the sky.",
        )
