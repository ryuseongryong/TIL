import os, requests
from dotenv import load_dotenv

load_dotenv()

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.getenv("API_KEY")
print(TEQUILA_API_KEY)


class FlightSearch:
    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        res = requests.get(url=location_endpoint, params=query, headers=headers)
        # print(res.text)
        # print(res.json())
        data = res.json()["locations"]
        iataCode = data[0]["code"]
        return iataCode
