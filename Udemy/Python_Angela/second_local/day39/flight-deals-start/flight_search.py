import os, requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flight_data import FlightData

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

    def check_flights(
        self, origin_city_code, destination_city_code, from_time, to_time
    ):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "KRW",
        }

        res = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search", params=query, headers=headers
        )
        print(res.text)

        try:
            data = res.json()["data"][0]
        except IndexError:
            print(f"No Flights found for {destination_city_code}!")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][0]["local_departure"].split("T")[0],
        )
        print(f"{flight_data.destination_city}: ₩{flight_data.price}")
        return flight_data
