import os
import requests
from dotenv import load_dotenv
from datetime import datetime

os.chdir("./Udemy/Python_Angela/second_local/day37")
load_dotenv()
TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# res = requests.post(url=pixela_endpoint, json=user_params)
# res = requests.delete(url=pixela_endpoint, headers={"X-USER-TOKEN": "abcdasdf1234zxcv"})
# print(res.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "ajisai",
}
headers = {"X-USER-TOKEN": TOKEN}

# res = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(res.text)

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

today = datetime.now()
print(today.strftime("%Y%m%d"))

pixel_data = {"date": today.strftime("%Y%m%d"), "quantity": input("How many kilometers did you cycle today? ")}

res = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
print(res.text)

# update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
# update_data = {"quantity": "27"}
# res = requests.put(url=update_endpoint, json=update_data, headers=headers)
# print(res.text)

# delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"
# res = requests.delete(url=delete_endpoint, headers=headers)
# print(res.text)
