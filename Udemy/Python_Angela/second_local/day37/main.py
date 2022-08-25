import os
import requests
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day37")
load_dotenv()
TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")

pixela_endpoint = "https://pixe.la/v1/users/"

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
    "id": "graph1",
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "ajisai",
}
headers = {"X-USER-TOKEN": TOKEN}

res = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
print(res)
