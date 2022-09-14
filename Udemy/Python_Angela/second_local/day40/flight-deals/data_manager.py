import requests, os
from dotenv import load_dotenv

os.chdir("./Udemy/Python_Angela/second_local/day40/flight-deals")
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
            print(city)
            new_data = {"price": {"iataCode": city["iataCode"]}}
            res = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=bearer_header,
            )
            print(res.text)

    def get_customer_emails(self):
        res = requests.get(SHEETY_ENDPOINT)
        data = res.json()
        self.customer_data = data["users"]
        return self.customer_data
