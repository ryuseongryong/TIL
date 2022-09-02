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
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_iatacode(self):
        for city in self.destination_data:
            new_data = {"price": {"iataCode": city["iataCode"]}}
            res = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data)
            print(res.text)
            return res.text


print(DataManager().get_destination_data())
DataManager().update_destination_iatacode()
