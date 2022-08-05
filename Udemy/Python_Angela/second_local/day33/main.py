import requests

res = requests.get(url="http://api.open-notify.org/iss-now.json")
res.raise_for_status()

data = res.json()

longitude = data["iss_position"]["longitude"]
latitude = data["iss_position"]["latitude"]

iss_position = (latitude, longitude)
print(iss_position)
