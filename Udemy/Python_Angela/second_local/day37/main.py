import os
import requests
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day37")
load_dotenv()

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": "abcdasdf1234zxcv",
    "username": "seongryong",
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# res = requests.post(url=pixela_endpoint, json=user_params)
# print(res.text)
