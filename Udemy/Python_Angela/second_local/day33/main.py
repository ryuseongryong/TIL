import requests
import datetime

# res = requests.get(url="http://api.open-notify.org/iss-now.json")
# res.raise_for_status()

# data = res.json()

# longitude = data["iss_position"]["longitude"]
# latitude = data["iss_position"]["latitude"]

# iss_position = (latitude, longitude)
# print(iss_position)


MY_LAT = 37.450027
MY_LONG = 126.906663

url = "http://api.sunrise-sunset.org/json"
params = {"lat": MY_LAT, "long": MY_LONG, "formatted": 0}
# url = f"http://api.sunrise-sunset.org/json?lat={MY_LAT}&lng={MY_LONG}"


res = requests.get(url, params=params)
res.raise_for_status()
data = res.json()
sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
sunset = data["results"]["sunset"].split("T")[1].split(":")[0]


time_now = datetime.datetime.now()
print(sunrise, "\n", sunset, "\n", time_now)
