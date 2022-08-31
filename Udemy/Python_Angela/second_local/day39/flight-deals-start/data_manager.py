from email import header
import requests, os
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day39/flight-deals-start")
load_dotenv()


SHEETY_ENDPOINT = os.getenv("API_URL")
TOKEN = os.getenv("TOKEN")

bearer_header = {"Authorization": TOKEN}


class DataManager:
    def __init__(self) -> None:
        self.destination_data = {}

    def get_destination_data(self):
        res = requests.get(url=SHEETY_ENDPOINT, headers=bearer_header)
        data = res.json()
        return data


a = DataManager().get_destination_data()
print(a)
